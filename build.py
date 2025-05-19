import json
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip, file_to_subtitles

# Load alignment data
with open("output.json", "r") as f:
    data = json.load(f)["normalized_alignment"]

clip_start = data["character_start_times_seconds"][0]
clip_end = data["character_end_times_seconds"][-1]

# Load video and audio
video = VideoFileClip("videoplayback.mp4").subclipped(clip_start, clip_end)
audio = AudioFileClip("output.mp3")
video = video.with_audio(audio)

sub_list = file_to_subtitles("output.srt", encoding='utf-8')


subtitles = SubtitlesClip(subtitles=sub_list, font='./font/Comic Sans MS.ttf')

final = CompositeVideoClip([video, subtitles.with_position(('center', 'center'))])
final.write_videofile("final.mp4", fps=video.fps)

