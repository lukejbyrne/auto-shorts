import subprocess
import sys
import os
from pytube import YouTube
import moviepy.editor as mp
import json
from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.video.fx.all as vfx
from moviepy.video.fx.all import *
import boto3
import random
import time
import re
from moviepy.config import change_settings


# Install dependencies with pip
dependencies = ["google-cloud-speech", "moviepy", "pytube", "ffmpeg-python", "assemblyai", "pygame"]
subprocess.run(["pip", "install", *dependencies], check=True)

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install additional dependencies
additional_dependencies = ["moviepy"]
for dep in additional_dependencies:
    install(dep)

os.environ["IMAGEIO_CONVERTER_EXE"] = "/opt/homebrew/bin/convert"
os.environ["IMAGEIO_CONVERTER"] = "/opt/homebrew/bin/convert"
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/local/bin/ffmpeg"
os.environ["FFMPEG_BINARY"] = "/opt/homebrew/bin/ffmpeg"
change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/convert"})

# Replace the values with your desired link, start time, and duration
video_id = "fINWIDv6-ig"
yt_link = "www.youtube.com/watch?v=" + video_id
start_time = "00:43:02.0"
duration = 25.0

# Convert start time to seconds
start_time_sec = sum(x * float(t) for x, t in zip([3600, 60, 1], start_time.split(":")))

# create a YouTube object and extract the video and audio streams
# yt = YouTube(yt_link)
# video_stream = yt.streams.filter(file_extension='mp4').first()
# audio_stream = yt.streams.filter(only_audio=True).first()

# download the video and audio streams to the current directory
# video_stream.download(filename="temp/original_vid.mp4")
# audio_stream.download(filename="temp/original_audio.mp3")

# Use moviepy to set the audio to the video
video = VideoFileClip("temp/original_vid.mp4")
print("setting yt vid...")
audio = AudioFileClip("temp/original_audio.mp3")
print("setting yt audio...")
final = video.set_audio(audio)
print("syncing yt vid and audio...")

# Use moviepy to trim the video
trimmed = final.subclip(start_time_sec, start_time_sec + duration)

# Write the resized video to a new file
trimmed.write_videofile('temp/my_video_cut.mp4')

# Set input and output file names
input_file = "temp/my_video_cut.mp4"
output_file = "temp/my_video_crop.mp4"

# Define crop size and position
width, height = 1080, 720
x, y = (1080 - width) // 2, (720 - height) // 2

# Define ffmpeg command
ffmpeg_cmd = f"ffmpeg -i {input_file} -filter:v 'crop=ih*9/16:ih,scale=720:1280' -c:a copy {output_file}"

# Run ffmpeg command
subprocess.run(ffmpeg_cmd, shell=True, check=True)

# Set your AWS credentials here
aws_access_key_id = 'AKIAW6WAIBUV6MQCILS2'
aws_secret_access_key = 'GfUKSciu2e2aBsHgjqFgANqHsldM1HOQhB0Ogbeb'
region_name = 'eu-west-1'

# Set the path to your audio file here
audio_path = "temp/my_video_crop.mp4"

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
job_name = f"{video_id}_{start_time}_-{duration}_".replace(":", "_")
job_name = re.sub(r"[^0-9a-zA-Z._-]+", "", job_name)

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

filename = job_name + ".json"

# Load the AWS Transcribe output JSON file
with open(filename, 'r') as f:
    transcribe_output = json.load(f)



# Extract the words and their start and end times from the JSON
words = []
for item in transcribe_output['results']['items']:
    if item['type'] == 'pronunciation':
        word = item['alternatives'][0]['content']
        start_time = float(item['start_time']) - 0.1
        end_time = float(item['end_time']) - 0.1
        words.append((word, start_time, end_time))

# Load the video file using MoviePy
video = mp.VideoFileClip('temp/my_video_crop.mp4')

# Create a black clip with the same duration and size as the original clip
black = mp.ColorClip(size=video.size, color=(0, 0, 0), duration=video.duration)

# Set the audio of the black clip to the audio of the original clip
black = black.set_audio(video.audio)

# Set the 'fps' attribute of the clip object
black.fps = video.fps

# Replace the original clip with the black clip
video_black = black

# Split the words into chunks based on capitalization
max_words_per_chunk = 2
chunks = []
chunk = []
for word, start_time, end_time in words:
    if word[0].isupper() and chunk:
        chunks.append(chunk)
        chunk = [(word, start_time, end_time)]
    else:
        chunk.append((word, start_time, end_time))
    if len(chunk) == max_words_per_chunk:
        chunks.append(chunk)
        chunk = []

if chunk:
    chunks.append(chunk)

# Create a list of TextClips, one for each chunk
clips1 = []
clips2 = []
chunk_count = 0
for chunk in chunks:
    chunk_count += 1
    # Extract the words and timestamps for the current chunk
    chunk_words = [word[0] for word in chunk]
    start_time = chunk[0][1]
    end_time = chunk[-1][2]
    # Create a TextClip object for the current chunk, with the words, duration, and position
    caption_text = ' '.join(chunk_words)
    caption_text2 = ' '.join(chunk_words).upper()
    caption_duration = end_time - start_time
    # Create the first TextClip with the existing font settings
    caption1 = mp.TextClip(caption_text, fontsize=40, color='white').set_duration(caption_duration).set_start(start_time).set_pos(('center'))
    # Append the TextClip to the list of clips for the first video
    clips1.append(caption1)
    # Create the second TextClip with a different font
    caption2 = mp.TextClip(caption_text2, fontsize=50, color='white', font='impact.ttf', stroke_color='black', stroke_width=2).set_duration(caption_duration).set_start(start_time).set_pos(('center'))
    # Append the TextClip to the list of clips for the second video
    clips2.append(caption2)
    # Print the chunk words and start/end times for the current chunk
    print(f"Chunk {chunk_count} words:", chunk_words, "Start time:", start_time, "End time:", end_time)
    # Review chunk on screen
    while True:
        # Ask the user to confirm whether the chunk is correct, to revise it, or to create a new chunk
        print("Is this chunk correct? Press enter to continue, enter the corrected chunk or enter 'q' to quit: ")
        response = input()
        if response == '':
            # If the user wants to continue with the current chunk, break out of the while loop and proceed to the next chunk
            break
        elif response.lower() == 'q':
            # If the user wants to quit, break out of the while loop and stop processing chunks
            break
        else:
            # If the user wants to correct the chunk, update the last TextClip in the list with the corrected chunk
            caption_text = response
            caption1 = mp.TextClip(caption_text, fontsize=40, color='white').set_duration(caption_duration).set_start(start_time).set_pos(('center'))
            caption2 = mp.TextClip(caption_text, fontsize=40, color='white', shadow=True, shadow_color='black', shadow_opacity=1).set_duration(caption_duration).set_start(start_time).set_pos(('center').upper())
            clips1[-1] = caption1
            clips2[-1] = caption2
            # Print the updated chunk and continue to the next chunk
            print(f"Updated chunk {chunk_count}:", caption_text)

from moviepy.editor import *

# Load the video file
video_gameplay = VideoFileClip("BeamNG.mp4")
# Remove the audio from video_gameplay
video_gameplay = video_gameplay.without_audio()

# Crop the video_gameplay to 720x640
x1, y1 = (video_gameplay.w - 720) // 2, (video_gameplay.h - 640) // 2
x2, y2 = x1 + 720, y1 + 640
cropped_video = video_gameplay.crop(x1=x1, y1=y1, x2=x2, y2=y2)

# Choose a random start time
t_start = random.uniform(0, video.duration - cropped_video.duration)
# Extract a subclip with the chosen start time
subclip = cropped_video.subclip(t_start, t_start + video.duration)
# Get the minimum duration between both videos
min_duration = min(video.duration, video_gameplay.duration)
# Overlay the cropped video on top of the second video
result_temp = CompositeVideoClip([video, subclip.set_position(("center", "bottom"))]).set_duration(min_duration)


# Combine the video and the captions for the first video
result_black = mp.CompositeVideoClip([black, *clips1])
# Combine the video and the captions for the second video
result = mp.CompositeVideoClip([result_temp, *clips2])


# Write the output video to file
result.write_videofile('temp/my_video_default.mp4')
result_black.write_videofile('temp/my_video_black.mp4')

# Create black and white version
bw_clip = result.fx(vfx.blackwhite)
bw_clip.write_videofile('temp/my_video_bw.mp4')


# # Load the audio file
# audio = mp.AudioFileClip("diedlonely - avenoir (320 kbps).mp3").volumex(0.35)
# # Get the duration of the audio file
# music_duration = audio.duration
# # Choose a random start time
# t_start = random.uniform(0, music_duration - music_duration)
# # Extract a subclip with the chosen duration
# subclip = audio.subclip(t_start, duration)

# Load the audio file
audio = mp.AudioFileClip("Motivational Background Music.mp3").volumex(0.25)
# Extract a subclip with the chosen duration
subclip = audio.subclip(0, duration)

# Load the video clips
clip1 = mp.VideoFileClip("temp/my_video_default.mp4")
clip2 = mp.VideoFileClip("temp/my_video_bw.mp4")
clip3 = mp.VideoFileClip("temp/my_video_black.mp4")

# Extract the audio tracks from each clip
audio1 = clip1.audio
audio2 = clip2.audio
audio3 = clip3.audio

# Combine the audio tracks
combined_audio1 = mp.CompositeAudioClip([subclip, audio1.volumex(1.5)])
combined_audio2 = mp.CompositeAudioClip([subclip, audio2.volumex(1.5)])
combined_audio3 = mp.CompositeAudioClip([subclip, audio3.volumex(1.5)])

# Set the audio tracks for each clip to the combined audio
clip4 = clip1.set_audio(combined_audio1)
clip5 = clip2.set_audio(combined_audio2)
clip6 = clip3.set_audio(combined_audio3)

# Write the output videos with the combined audio tracks
# clip4.write_videofile("temp/my_video_default_music.mp4")
# clip5.write_videofile("temp/my_video_bw_music.mp4")
# clip6.write_videofile("temp/my_video_black_music.mp4")

# Define a list of logo image file names
logo_files = ["logos/absolute.png", "logos/measured.png", "logos/raw.png", "logos/motivate.png", "logos/inspire.png", "logos/succeed.png"]

# Loop through each video clip and add a logo to it
for i, clip in enumerate([clip1, clip2, clip3, clip4, clip5, clip6]):

    # Load the logo image
    logo = (mp.ImageClip(logo_files[i])
            .set_duration(clip.duration)
            .set_opacity(1))

    # Resize the logo to a width of 200 pixels
    logo = logo.resize(width=150)

    # Set the position of the logo on the video
    logo_pos = ("center", clip.size[1]*0.65)

    # Add the logo to the video as an overlay
    video_with_logo = mp.CompositeVideoClip([clip, logo.set_pos(logo_pos)])

    # Write the output video to a file with the logo file name included
    video_with_logo.write_videofile(f"final/my_video_with_{logo_files[i].split('/')[1]}_logo.mp4", audio=True)

# Cleanup the temporary files
import os
os.remove("temp/original_vid.mp4")
os.remove("temp/original_audio.mp3")
os.remove("temp/my_video_cut.mp4")
os.remove("temp/my_video_crop.mp4")
os.remove("temp/my_video_black.mp4")
os.remove("temp/my_video_bw.mp4")
os.remove("temp/my_video_default.mp4")