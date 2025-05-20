import praw
import requests
import base64
import json
import pysrt
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip, file_to_subtitles


### Reddit Scraping ###

def scrape_stories(client_id, client_secret, subs: list[str], lim=10):
    """
    top (lim = 10) hottest stories of subreddits passed (subs) 
    """

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="apple:reddit.scraper:v1.0 (by /u/samhpark)"
    )

    for name in subs:
        print(f"_________{name}__________")
        subreddit = reddit.subreddit(name)
        for post in subreddit.hot(limit=lim):
            #ifnore if pinned
            if post.stickied:
                continue
            #ignore if moderator post
            if post.author and post.author.name.lower() in ["automoderator"]:
                continue
            #ignore if content is not text
            if not post.selftext:
                continue

            print(f"* {post.title}")
            print(f"{post.selftext}")


### TTS ###

def tts(elevenlabs_key, text, voice_id="nPczCjzI2devNBz1zQrb", stability=0.5, similarity_boost=0.75, speed=1.1):
    """
        takes (text) and produces audio file with voice: (voice_id) and alignment info for make_srt()
        elevenlabs model parameters can also be changed (stability, similarity_boost, speed)
    """
    headers = {
        "xi-api-key": elevenlabs_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }   
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "speed": speed
        },
        "output_format": "json"
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print("HTTP error occurred:", http_err)
        if http_err.response is not None:
            print("Status code:", http_err.response.status_code)
            print("Response body:", http_err.response.text)  # <-- This shows you *why* the API rejected your input
    except Exception as err:
        print("Other error occurred:", err)
    else:
        print("Request succeeded with status", response.status_code)

    data = response.json()

    # Save audio file
    audio = data["audio_base64"]
    with open("output.mp3", "wb") as f:
        f.write(base64.b64decode(audio))

    # Save the alignment info
    alignment = data["normalized_alignment"]
    with open("output.json", "w") as f:
        json.dump(alignment, f, indent=2)


### Subtitles ###

def make_srt():
    """
        Produces srt given alignment data created by tts()
    """
    with open("output.json", "r") as f:
        data = json.load(f)

    chars = data['characters']
    starts = data['character_start_times_seconds']
    ends = data['character_end_times_seconds']

    subtitles = pysrt.SubRipFile()
    curr_line = ""
    curr_start = starts[0]
    line_index = 1

    for i in range(len(chars)):
        char = chars[i]
        if char == '\n':
            curr_line += ' '
            continue
        curr_line += char

        is_end = char in '?!.'
        long_enough = len(curr_line.strip()) > 4 and (ends[i] - curr_start > .25 and char == ' ')

        if is_end or long_enough:
            subtitles.append(
                pysrt.SubRipItem(
                    index=line_index,
                    start=pysrt.SubRipTime(seconds=curr_start),
                    end=pysrt.SubRipTime(seconds=ends[i]),
                    text=curr_line.strip()
                )
            )
            line_index += 1
            curr_line = ""
            # Avoid index error if we're at the end
            if i + 1 < len(starts):
                curr_start = starts[i + 1]

    # Append any remaining line
    if curr_line.strip():
        subtitles.append(
            pysrt.SubRipItem(
                index=line_index,
                start=pysrt.SubRipTime(seconds=curr_start),
                end=pysrt.SubRipTime(seconds=ends[-1]),
                text=curr_line.strip()
            )
        )

    subtitles.save("output.srt", encoding='utf-8')


### Build ###

def build_video(video_path, audio_path, font_path, font_color, stroke_color):
    """
        Using output.mp3 from tts(), output.srt from srt(),
        and video_path compiles the final video
        font and related parameters can also be changed
    """

    # Load alignment data
    with open("output.json", "r") as f:
        data = json.load(f)

    clip_start = data["character_start_times_seconds"][0]
    clip_end = data["character_end_times_seconds"][-1]

    # Load video and audio
    video = VideoFileClip(video_path).subclipped(clip_start, clip_end)
    audio = AudioFileClip(audio_path)
    video = video.with_audio(audio)

    sub_list = file_to_subtitles("output.srt", encoding='utf-8')

    def make_textclip(txt):
        return TextClip(
            font=font_path,
            font_size=24,
            size=(500, 100),
            text=txt,
            color=font_color,
            stroke_color=stroke_color,
            stroke_width=1,
            method='caption'
        )

    subtitles = SubtitlesClip(subtitles=sub_list, make_textclip=make_textclip)

    final = CompositeVideoClip([video, subtitles.with_position(('center', 'center'))])
    final.write_videofile(
        "final.mp4",
        fps=video.fps,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True
    )

### Upload ###

