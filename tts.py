import requests
import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()
elevenlabs_key = os.getenv("ELEVENLABS_KEY")

headers = {
    "xi-api-key": elevenlabs_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

voice_id = "nPczCjzI2devNBz1zQrb"



text = '''Why is my partner frequently pretending I’m having nightmares so he can wake me up? 34F, 37M
I (34F) have been dating my partner (37M, BPD) for 8 months and I cant figure out why he lies about seemingly inconsequential things. We are long distance right now but we hang out through discord and we keep discord on overnight, as well. I always go to bed before he does because of different work/sleep schedules.

He will frequently wake me up by calling out my name repeatedly, then tell me I was having a nightmare and begin “comforting” me. Now, there was a period of time where I was having intense night terrors because of medication I was on, and when he’d wake me from those, I knew it was legitimate. But the other times (before and after the period of time I was on medication and actually having night terrors), I would be in either a light sleep/half awake state and knew I had not been having a nightmare and certainly not to the extent of audibly or visually indicating that I was having a nightmare or in distress. After this kept happening, and because I frequently gaslight myself, I thought- what if I’m having nightmares and just don’t remember or realize it? So, I put it to the test. I would lay with my eyes closed and let it appear that I had fallen asleep- and sure enough he has “woken me up” from nightmares that aren’t happening.

I don’t understand what he’s getting out of this? Is it for attention? Is it some twisted way of making me feel cared for? Because it just makes me feel manipulated and honestly angry because I don’t get restful sleep as it is so I don’t want to be woken up repeatedly for imaginary nightmares.

He has also made up other random white lies that just have no purpose?? Like one morning he told me that my cat laid in front of my laptop and watched the entire movie he had playing from beginning to end and how cute it was- even though I explicitly heard him turn the movie off about 15 minutes in when he thought I had fallen asleep. 

TLDR: why does my boyfriend repeatedly pretend I am having nightmares so he can wake me up and tell other white lies that serve no purpose?

EDIT TO ADD: a lot of you are taking my desire to want to understand a person’s behavior and interpreting that to mean I don’t know the behavior is wrong and need to be told how [psychotic, cringe, and weird] I am for not realizing what was happening sooner/immediately. I’ll partially take the blame for that since I posted in a subreddit called relationship advice- in hindsight, that wasn’t the best move since I wasn’t really looking for advice on what to do and was more so looking for other people’s perspectives from possible similar experiences. More “what makes a person do things like this” vs “what do I do??”. As I mentioned to someone in the comments- part of my neurodivergence is having the need or desire to understand the “why” behind things- behaviors, rules, processes, etc. And that isn’t always possible or productive but that doesn’t remove my desire to want to understand.

For the people who think it’s the craziest thing they’ve ever heard of to stay on discord over night in a LDR- I don’t have the energy to calm down the dramatics over that. Totally cool that it’s not your cup of tea. As others have shared- it can be a way to bridge the gap and feel like you’re with each other when you can’t physically be. We had not always been long-distance. He isn’t just some random dude on the internet I had some fantasy relationship with.

To answer the many variations of asking why I’ve entertained this/put up with this/didn’t break up and block him the first time it happened: when you’ve been in abusive relationships and have a history of questioning your own reality/perspective/intuition, it can be easy to undermine yourself and think, “is this what really happened? people wake up and forget their dreams all the time- maybe I really was dreaming and just didn’t realize it at the time”. Couple that with having memory recall issues and the thought of- why the hell would someone do something weird and manipulative so obviously I must be off base here- and it’s a lot easier than some of you may realize to fall into that trap. Hence the reason I pretended to be asleep last night to see if it would happen and therefore I could prove to myself that I’m not crazy or misconstruing things. A lot of you pointed out that I’m being gaslit but then stopped short of acknowledging that it’s common for people who have been manipulated this way to need to write occurrences down or “collect evidence” so to speak, to affirm our reality that we are questioning.

“Why are you asking strangers on Reddit instead of talking to him and getting therapy for being such a cringe 34 year old grown woman?” - again, I don’t exist in a vacuum. This last incident literally just happened late last night. I got off discord after it happened, made this post in part to try to further process everything and in part to hear other peoples’ insight/similar experiences or even just affirming feedback (I don’t understand the phenomenon of people who engage in an online forum only to ask people why they have posted as if that’s not entirely the point). Then I was up all night unable to sleep, getting only an hour of sleep before working today, then going to therapy because yes- I am in therapy, and am just now settling in for the evening. I haven’t confronted the issue with him yet because of all this and because I am intentionally taking space to myself today to process everything and emotionally regulate which will allow me to more clearly articulate what I need to say.

Anyway, thank you to the people who didn’t just jump on to tell me how cringe I am and instead provided resources, your experiences, or a simple affirmation. And to those of you who did jump on to let me know how cringe you think I am, thank you for reminding me why I don’t typically engage in online forums.'''

payload = {
    "text": text,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "speed": 1.25
    },
    "output_format": "json"
}

url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
response = requests.post(url, headers=headers, json=payload)

data = response.json()

print(data["alignment"])
print(data["normalized_alignment"])


# Save audio file
audio = data["audio_base64"]
with open("output.mp3", "wb") as f:
    f.write(base64.b64decode(audio))

# Save the alignment info
alignment = data["normalized_alignment"]
with open("output.json", "wb") as f:
    f.write(alignment)