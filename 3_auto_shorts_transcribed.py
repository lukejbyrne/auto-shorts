import subprocess

import pycaption

# Install dependencies with pip
subprocess.run(["pip", "install", "google-cloud-speech", "moviepy", "pytube", "ffmpeg-python", "assemblyai", "pygame"], check=True)

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install dependencies
dependencies = ['moviepy']
for dep in dependencies:
    install(dep)

import os
import json
import moviepy.editor as mp
os.environ["IMAGEIO_CONVERTER_EXE"] = "/opt/homebrew/bin/convert"
os.environ["IMAGEIO_CONVERTER"] = "/opt/homebrew/bin/convert"
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2.credentials import Credentials
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/local/bin/ffmpeg"
os.environ["FFMPEG_BINARY"] = "/opt/homebrew/bin/ffmpeg"
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from pytube import YouTube
import subprocess

from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/convert"})

# Replace the values with your desired link, start time, and duration
video_id = "JJoWNhKWe7I"
yt_link = "www.youtube.com/watch?v=" + video_id
start_time = "00:00:47"
duration = 12

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
output_file = "my_video_crop.mp4"

# Define crop size and position
width, height = 1280, 720
x, y = (1280 - width) // 2, (720 - height) // 2

# Define ffmpeg command
ffmpeg_cmd = f"ffmpeg -i {input_file} -filter:v 'crop=ih*9/16:ih,scale=720:1280' -c:a copy {output_file}"

# Run ffmpeg command
subprocess.run(ffmpeg_cmd, shell=True, check=True)

import os
import time
import json
import moviepy.editor as mp
import boto3

# Set your AWS credentials here
aws_access_key_id = 'AKIAW6WAIBUV6MQCILS2'
aws_secret_access_key = 'GfUKSciu2e2aBsHgjqFgANqHsldM1HOQhB0Ogbeb'
region_name = 'eu-west-1'

# Set the path to your audio file here
audio_path = "my_video_crop.mp4"

# Initialize S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name=region_name)

# Set the name of the S3 bucket where you want to upload the file
bucket_name = 'autoshortss3bucket'

# Upload the audio file to S3
s3.upload_file(audio_path, bucket_name, audio_path)

# Set the S3 URI for the uploaded audio file
job_uri = f's3://{bucket_name}/{audio_path}'

# Initialize AWS client
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)
client = session.client('transcribe')

# Define the parameters for the transcription job
# Replace special characters with underscores
job_name = f"{video_id}_{start_time}_{duration}".replace(":", "_")

transcription_job = {
    'TranscriptionJobName': job_name,
    'Media': {'MediaFileUri': job_uri},
    'MediaFormat': 'mp4',
    'LanguageCode': 'en-US',
    'OutputBucketName': bucket_name
}

# Start the transcription job
client.start_transcription_job(**transcription_job)

# Wait for the job to complete
while True:
    status = client.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    time.sleep(5)

job_status = client.get_transcription_job(TranscriptionJobName=job_name)
if job_status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
    s3 = boto3.resource('s3',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)
    bucket = s3.Bucket(bucket_name)
    object_key = f"{job_name}.json"
    bucket.download_file(object_key, object_key)
    with open(object_key, "r") as f:
        transcript = json.load(f)
else:
    transcript = None

filename = job_name+".json"

# Load the AWS Transcribe output JSON file
with open(filename, 'r') as f:
    transcribe_output = json.load(f)

# Extract the transcript from the JSON
transcript = transcribe_output['results']['transcripts'][0]['transcript']

# Load the video file using MoviePy
video = mp.VideoFileClip('my_video_crop.mp4')

# Add the captions using MoviePy's TextClip function
captions = mp.TextClip(transcript, fontsize=24, color='white', bg_color='black').set_duration(duration).set_position(('center', 'bottom'))

# Combine the video and the captions
result = mp.CompositeVideoClip([video, captions])

# Write the output video to file
result.write_videofile('my_video_with_captions.mp4')









# Cleanup the temporary files
import os
os.remove("./my_video_cut.mp4")
