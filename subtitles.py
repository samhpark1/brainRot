import json
import pysrt


with open("output.json", "r") as f:
    data = json.load(f)["alignment"]

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
