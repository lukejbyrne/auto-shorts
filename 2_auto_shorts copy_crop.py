import io
import os
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2.credentials import Credentials
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/local/bin/ffmpeg"
os.environ["FFMPEG_BINARY"] = "/opt/homebrew/bin/ffmpeg"
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from pytube import YouTube
import ffmpeg
import subprocess

# Replace the values with your desired link, start time, and duration
yt_link = "www.youtube.com/watch?v=JJoWNhKWe7I"
start_time = "00:01:23"
duration = 30

# Convert start time to seconds
start_time_sec = sum(x * int(t) for x, t in zip([3600, 60, 1], start_time.split(":")))

# Download the video
yt = YouTube(yt_link)
stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution='720p').order_by('resolution').desc().first()
stream.download(output_path="./", filename="original_vid.mp4")

# Download the audio
audio = yt.streams.filter(only_audio=True).first()
audio.download(output_path="./", filename="original_audio.mp3")

# Use moviepy to set the audio to the video
video = VideoFileClip("./original_vid.mp4")
audio = AudioFileClip("./original_audio.mp3")
final = video.set_audio(audio)

# Use moviepy to trim the video
trimmed = final.subclip(start_time_sec, start_time_sec + duration)

# Write the resized video to a new file
trimmed.write_videofile('my_video_cut.mp4')

# Set input and output file names
input_file = "my_video_cut.mp4"
output_file = "output.mp4"

# Define crop size and position
width, height = 1280, 720
x, y = (1280 - width) // 2, (720 - height) // 2

# Define ffmpeg command
ffmpeg_cmd = f"ffmpeg -i {input_file} -filter:v 'crop=ih*9/16:ih,scale=720:1280' -c:a copy {output_file}"

# Run ffmpeg command
subprocess.run(ffmpeg_cmd, shell=True, check=True)

# Cleanup the temporary files
import os
os.remove("./original_vid.mp4")
os.remove("./original_audio.mp3")
