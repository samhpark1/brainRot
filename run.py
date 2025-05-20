import os
from dotenv import load_dotenv

from module import *


# load env vars
load_dotenv()

reddit_client = os.getenv("REDDIT_CLIENT")
reddit_secret = os.getenv("REDDIT_SECRET")
elevenlabs_key = os.getenv("ELEVENLABS_KEY")



# Get alignment info and tts audio
payload_text = "this is a test, astagfarella!"

#tts(elevenlabs_key, payload_text)

# produce srt
#make_srt()

# build video
build_video('videoplayback.mp4', 'output.mp3', 'font/Comic Sans MS.ttf', 'white', 'red')

