import ffmpeg
import os
from datetime import datetime

os.chdir("C:\\Users\\zflee\\Desktop")

ts = datetime.strftime(datetime.now(),"%Y-%m-%d_%H-%M-%S")
elgato = "video=Game Capture HD60 Pro:audio=Game Capture HD60 Pro Audio"
output_file = f"{ts}_capture.mp4|[f=flv]rtmp://192.168.1.7/live"

stream = ffmpeg.input(elgato, format='dshow', rtbufsize='2048M')
a1 = stream.audio
v1 = stream.video.crop(x=255, y=0, width=1410, height=1080)
stream = ffmpeg.output(v1, a1, output_file, format='tee', vcodec='libx264',  video_bitrate='6000k', acodec='aac', pix_fmt='yuv420p')
print(stream.compile())
ffmpeg.run(stream)