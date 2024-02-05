# Overview
Motivational videos on Youtube were at an all time high with the uptake in shorts consumption. However, there were a variety of styles behind utilised. I selected the below as they were simple (in theory) to create and for AB/split testing, simple changes are best as they differ across minimal variables allowing for comparison.

[TODO: Analyise results?]

To test the validity of this Youtube automation strategy I developed a script which given a Youtube video link and timecode, creates 6 short form pieces of content and uploads them to Youtube (this was then expended to triple upload to Youtube, Tiktok, Instagram).

The 6 pieces of content are for purpose of split testing:
1. Colour - with music and captions
2. Colour - No music and captions
3. Black and White - with music and captions
4. Black and White - No music and captions
5. Black screen - with music and captions
6. Black screen - No music and captions

Examples can be found within folders 1 through 16.

I selected to split test the same clip across 6 channels, each with the above seperate criteria as the style / branding. For this I created branding in Canva and set up the below channels:

1. [DareTo Motivate](https://www.youtube.com/@dareto_motivate)
2. [Absolute Motivation](https://www.youtube.com/@Absolute-Motivation)
3. [DareTo Inspire](https://www.youtube.com/@dareto_inspire)
4. [Measured Motivation](https://www.youtube.com/@measuredmotivation)
5. [DareTo Succeed](https://www.youtube.com/@dareto_succeed)
6. [Raw Motivation](https://www.youtube.com/@rawmotivation_)

# To Run

1. Update the below in auto_shorts.py with the Youtube video ID 
 - video_id
 - start_time
 - duration
2. Run auto_shorts.py to create the video files
3. Run upload_shorts.py for Youtube upload OR triple_upload.py for Youtube, Tiktok, and Instagram

## Code

Code leverages python libraries to:
- Download YT video
- Modify aspect ratio and duration of the video
- Transcribe video using AWS
- Add captions to modified video versions