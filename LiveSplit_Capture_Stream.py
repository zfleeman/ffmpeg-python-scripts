import ffmpeg
import os
from datetime import datetime

# Outputs local video to Desktop.
# The output_file string also points the video to an rtmp ingest for live-streaming purposes. This could
# even be a Twitch ingest point with your stream key.
os.chdir("C:\\Users\\zflee\\Desktop")
ts = datetime.strftime(datetime.now(),"%Y-%m-%d_%H-%M-%S")
output_file = f"{ts}_capture.mp4|[f=flv]rtmp://192.168.1.7/live"

# This is the Windows dshow input string to capture the LIVE audio and video from my capture card
# TODO Need to learn what the rtbufsize and thread_queue_size parameters are doing.
# TODO I set the frameerate on this input stream with r=60. Unsure if that is necessary.
dshow_cap = "video=Game Capture HD60 Pro:audio=Game Capture HD60 Pro Audio"
elgato = ffmpeg.input(dshow_cap, format='dshow', rtbufsize='2048M', thread_queue_size=5096, r=60)

# LiveSplit (speedrunning software) window capture. Setting this at r=30 with thread_queue_size made the encode smoother. idk why
# TODO Need to learn more about thread_queue_size on this one
# TODO This is not synced up with the elgato. It's about 3 seconds ahead.
livesplit = ffmpeg.input('title=LiveSplit', format='gdigrab', r=30, draw_mouse=0, thread_queue_size=5096)

# Black background to layer things on. framerate set to 60, and loop=1 because it's an image file
bg = ffmpeg.input('bg.png', r=60, loop=1)

# strip out the audio into a different object to prevent it from being damaged by ffmpeg video filter errors
a1 = elgato.audio

# Crop the 1920x1080 input from my MiSTer to a SNES resolution
v1 = elgato.video.crop(x=255, y=0, width=1410, height=1080)

# overlay the elgato and livesplit feed onto the black background. scale the video to a lower resolution. 
# Don't forget shortest=1 on the elgato overlay. That's a requirement for the image file layering, aparently.
v2 = bg.overlay(v1, x=510, y=0, shortest=1).overlay(livesplit, x=0, y=65).filter('scale', '960x540')

# Take the layered video with the original audio, and use "format=tee" to allow for multiple outputs (local file AND rtmp). 
# Changing the pix_fmt to yuv420p to play nice with operating systems
# TODO is framerate necessary here?
stream = ffmpeg.output(v2, a1, output_file, framerate=60, format='tee', vcodec='libx264',  video_bitrate='1500k', acodec='aac', pix_fmt='yuv420p')

# print the actual ffmpeg command for logging
print(stream.compile())

# do work!
ffmpeg.run(stream)