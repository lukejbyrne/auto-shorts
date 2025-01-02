# Overview
Motivational videos on YouTube were at an all-time high with the uptake in shorts consumption. However, there were a variety of styles behind utilised. I selected the below as they were simple (in theory) to create and for AB/split testing, simple changes are best as they differ across minimal variables allowing for comparison.

# Results
Colour and black-and-white formats with music and captions perform best due to their emotional appeal and engagement, while black screen styles, especially without music or captions, significantly underperform and lack viewer retention. Adding music and visually engaging elements boosts performance across all styles.

# Methodology
To test the validity of this YouTube automation strategy I developed a script which gives a YouTube video link and timecode, creates 6 short-form pieces of content and uploads them to YouTube (this was then expended to triple upload to YouTube, Tiktok, and Instagram).

The 6 pieces of content are for the purpose of split testing:
1. Colour - with music and captions
2. Colour - No music and captions
3. Black and White - with music and captions
4. Black and White - No music and captions
5. Black screen - with music and captions
6. Black screen - No music and captions

Examples can be found within folders 1 through 16.

I selected to split test the same clip across 6 channels, each with the above separate criteria as the style/branding. For this, I created branding in Canva and set up the channels below:

1. [DareTo Motivate](https://www.youtube.com/@dareto_motivate)
2. [Absolute Motivation](https://www.youtube.com/@Absolute-Motivation)
3. [DareTo Inspire](https://www.youtube.com/@dareto_inspire)
4. [Measured Motivation](https://www.youtube.com/@measuredmotivation)
5. [DareTo Succeed](https://www.youtube.com/@dareto_succeed)
6. [Raw Motivation](https://www.youtube.com/@rawmotivation_)

# To Run

1. Update the below in auto_shorts.py with the YouTube video ID 
 - video_id
 - start_time
 - duration
2. Run auto_shorts.py to create the video files
3. Run upload_shorts.py for YouTube upload OR triple_upload.py for YouTube, Tiktok, and Instagram

# Code

Code leverages Python libraries to:
- Download YT video
- Modify the aspect ratio and duration of the video
- Transcribe video using AWS
- Add captions to modified video versions

# Analysis

1. **Colour - with music and captions (Dare to Motivate):**
   - Relatively consistent performance with some spikes in views (e.g., "Goggins's Secret Power").
   - Captions and music might contribute to a higher engagement rate.
   - More visually appealing and engaging, leading to better audience retention.

2. **Colour - No music and captions (Absolute Motivation):**
   - Good performance in views, especially for topics with high relatability (e.g., "The Importance of Pack Mentality").
   - Absence of music may affect emotional engagement.
   - Captions help with accessibility, and maintaining steady audience retention.

3. **Black and White - with music and captions (Dare to Inspire):**
   - High-performing with standout videos (e.g., "He Does Not Stop | Joe Rogan").
   - Black-and-white visuals with music create a dramatic tone that likely resonates well with a motivational audience.
   - Captions enhance clarity and appeal for international or multitasking viewers.

4. **Black and White - No music and captions (Measured Motivation):**
   - Lower performance compared to other styles, suggesting less emotional connection.
   - Black-and-white visuals without music might feel flat or less engaging for the target audience.

5. **Black screen - with music and captions (Dare to Succeed):**
   - Mixed results; some topics perform better due to strong storytelling (e.g., "David Goggins' Secret Enemies").
   - Black screen relies heavily on audio and captions, which might limit visual appeal.

6. **Black screen - No music and captions (Raw Motivation):**
   - Lowest performance overall. The lack of music and visuals might fail to capture or retain attention.
   - Captions alone are not enough to drive engagement in the absence of strong audio and visuals.

## Observations:
- **Engagement Boosters:**
  - Music and captions generally enhance performance.
  - Black-and-white with music creates a strong emotional tone and performs well in motivational content.

- **Underperforming Styles:**
  - Black screens without music or captions lack appeal and should likely be avoided or reworked with visual elements.

- **Best Practices:**
  - Combine visually engaging elements (e.g., colour or dramatic black-and-white visuals) with captions and music.
  - Tailor content to match the audience's preference for emotionally engaging, impactful storytelling.
