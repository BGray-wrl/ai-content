# sk_0450317123f76dedacc28fa33b8a76ace49efea14b55a941

import os
import requests
from pydub import AudioSegment
import json


def text_to_speech_by_sentence(sentences, output_folder, api_key, voice="onwK4e9ZLuTAKqWW03F9", stability=0.75, similarity_boost=0.75):
    os.makedirs(output_folder, exist_ok=True)
    # sentences = [s.strip() for s in text.split(r";.\n") if s.strip()]
    audio_clips = []

    base_url = "https://api.elevenlabs.io/v1"
    headers = {
        "Accept": "application/json",
        "xi-api-key": api_key,
    }
    print(sentences)

    for i, sentence in enumerate(sentences):
        # Prepare the request payload
        payload = {
            "text": sentence,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }

        # Perform the text-to-speech request
        response = requests.post(f"{base_url}/text-to-speech/{voice}", json=payload, headers=headers)

        if response.status_code == 200:
            audio_content = response.content

            # Save each sentence audio
            sentence_file = os.path.join(output_folder, f"sentence_{i}.mp3")
            with open(sentence_file, "wb") as out:
                out.write(audio_content)
            print(f"Generated audio for sentence {i}: {sentence}")
            audio_clips.append(sentence_file)
        else:
            print(f"Error generating audio for sentence {i}: {response.status_code} {response.text}")

    # Combine all audio files into one
    # combined_audio = AudioSegment.empty()
    # for clip in audio_clips:
    #     combined_audio += AudioSegment.from_file(clip)

    # Save the combined audio
    # combined_audio_file = os.path.join(output_folder, "combined_audio.mp3")
    # combined_audio.export(combined_audio_file, format="mp3")
    # print(f"Combined audio saved to {combined_audio_file}")
    return sentences


# Example usage
if __name__ == "__main__":
    # text = ""
    # with open("testing_story.json", "r") as f:
    #     text_temp = json.load(f)
    #     text = text_temp[0]["text"]

    # # print(text)
    # output_folder = "output_audio"
    # elevenlabs_api_key = "sk_0450317123f76dedacc28fa33b8a76ace49efea14b55a941"  # Replace with your API key

    # text_to_speech_by_sentence(text, output_folder, elevenlabs_api_key)
    pass
