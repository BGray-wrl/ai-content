## NOTE have yet to test this code TODO test this code

from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from pydub import AudioSegment, silence
import json
from pathlib import Path

def crop_to_youtube_shorts_dims(video_file):
    video = VideoFileClip(video_file)
    
    # Calculate cropping parameters for 9:16 aspect ratio
    target_aspect_ratio = 9 / 16
    video_aspect_ratio = video.w / video.h

    if video_aspect_ratio > target_aspect_ratio:
        # Crop width to match the target aspect ratio
        new_width = int(video.h * target_aspect_ratio)
        crop_x = (video.w - new_width) // 2
        cropped_video = video.cropped(x1=crop_x, x2=crop_x + new_width)
    else:
        # Crop height to match the target aspect ratio
        new_height = int(video.w / target_aspect_ratio)
        crop_y = (video.h - new_height) // 2
        cropped_video = video.cropped(y1=crop_y, y2=crop_y + new_height)

    return cropped_video

def combine_audio_files(audio_directory, combined_audio_file):
    # Convert the string to a Path object
    audio_dir = Path(audio_directory)
    combined = AudioSegment.empty()
    sentence_durations = []
    
    for file in sorted(audio_dir.iterdir()):  # Ensure files are processed in sorted order
        if file.suffix == ".mp3":
            sentence_audio = AudioSegment.from_file(file)
            sentence_durations.append(len(sentence_audio) / 1000)  # Duration in seconds
            combined += sentence_audio

    combined.export(combined_audio_file, format="mp3")
    return sentence_durations

def create_video(sentences, audio_file, video_file, output_file, font="Courier New", font_size=35, color="white"):
    # Load the stock video
    video_clip = VideoFileClip(video_file)
    video_clip = crop_to_youtube_shorts_dims(video_file)

    # Load the audio file
    sentence_durations = combine_audio_files(audio_file,"combined_audio.mp3")
    audio_clip = AudioFileClip("combined_audio.mp3")
    video_duration = audio_clip.duration

    # Loop the video if it is shorter than the audio
    if video_clip.duration < video_duration:
        loop_count = int(video_duration // video_clip.duration) + 1
        video_clip = concatenate_videoclips([video_clip] * loop_count).subclipped(0, video_duration)

    font_size = int(video_clip.h * font_size / 200)  # Convert font size to video dimensions
    print(f"Font size: {font_size}")

    # Split the text into sentences
    # sentences = [s.strip() for s in text.split(r";.\n") if s.strip()]


    # Create sentence timings
    sentence_timings = []
    start_time = 0
    for duration in sentence_durations:
        end_time = start_time + duration
        sentence_timings.append((start_time, end_time))
        start_time = end_time

    wrapped_clips = []

    for (start, end), sentence in zip(sentence_timings, sentences):

        # Create the black text overlay
        subtitle_clip = TextClip(
            text=sentence,
            font_size=font_size,
            font=font,
            color="white",
            size=(int(video_clip.w * 0.75), None),  # Same width as shadow
            method="caption",
            text_align="center"
        ).with_position(("center", "center")).with_start(start).with_duration(end - start)

        # Add the styled subtitle to the list
        wrapped_clips.append(subtitle_clip)

    # Combine video with subtitles
    video_with_audio = video_clip.with_audio(audio_clip).subclipped(0, video_duration)
    final_clip = CompositeVideoClip([video_with_audio] + wrapped_clips)

    # Write the final video to a file
    # final_clip.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")
    # print(f"Video content written to {output_file}")
    return final_clip

# Example usage
if __name__ == "__main__":
    # text = ""
    # with open("testing_story.json", "r") as f:
    #     text_temp = json.load(f)
    #     text = text_temp[0]["text"]

    # audio_file = "output_audio"
    # video_file = "stock_footage/creepy forest_3427514.mp4"  # Replace with your stock footage file
    # output_file = "creepy_story_video.mp4"

    # create_video(text, audio_file, video_file, output_file)
    
    pass

