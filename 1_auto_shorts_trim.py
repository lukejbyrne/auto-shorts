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

# Replace the values with your desired link, start time, and duration
yt_link = "https://www.youtube.com/watch?v=JJoWNhKWe7I"
start_time = "00:01:23"
duration = 30

# Convert start time to seconds
start_time_sec = sum(x * int(t) for x, t in zip([3600, 60, 1], start_time.split(":")))

# Download the video
yt = YouTube(yt_link)
stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
stream.download(output_path="./", filename="original_vid.mp4")

# Download the audio
audio = yt.streams.filter(only_audio=True).first()
audio.download(output_path="./", filename="original_audio.mp4")

# Use moviepy to set the audio to the video
video = VideoFileClip("./original_vid.mp4")
audio = AudioFileClip("./original_audio.mp4")
final = video.set_audio(audio)

# Use moviepy to trim the video
trimmed = final.subclip(start_time_sec, start_time_sec + duration)
trimmed.write_videofile("./trimmed.mp4")

# Cleanup the temporary files
import os
os.remove("./original_vid.mp4")
os.remove("./original_audio.mp4")
