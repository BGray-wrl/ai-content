## Author: Benjamin Grayzel
## Date: 1/26/2025
## Description: This script generates a video from a Reddit story, uploads it to YouTube, and (hopefully) sends me SMS notification w/link.
## TODO:
##  - make reddit_stories fetch a single story and feed it into the function, not from sourced_content
##  - make the _used files a json file or dict
##  - set up online hosting to run this script daily/biweekly/whatever
##  - add api to image gen for thumbnails
##  - add api to text for better description
##  - find better background vids
##  - add background music?


import json
from dotenv import load_dotenv
import os
import shutil
import re

from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText

from create_video import create_video
from stock_footage import download_stock_footage
from text_to_speech import text_to_speech_by_sentence
from upload_to_yt import upload_to_youtube
# from reddit_stories import fetch_stories

input_file = "ShortScaryStories.json" #current.json
checkfile_path = "ShortScaryStories_used.txt"
audio_dir = "output_audio"
output_file = f"output_video/current.mp4"
current_video_file = "output_video/current.mp4"

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
MAIL_APP_PASSWORD = os.getenv('MAIL_APP_PASSWORD')

def send_sms(video_id, video_title, message, act_sid = TWILIO_ACCOUNT_SID, auth_token = TWILIO_AUTH_TOKEN, twilio_phone = TWILIO_PHONE_NUMBER, my_phone = PHONE_NUMBER):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your video '{video_title}' has been uploaded to YouTube! Watch it here: https://youtu.be/{video_id}",
        from_=TWILIO_PHONE_NUMBER,
        to=PHONE_NUMBER
    )
    print(f"SMS sent: {message.sid}")

def send_sms_via_email(phone_number, message, carrier_domain='tmomail.net'):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = "benjamingrayzel@gmail.com"  # Replace with your email
    app_password = MAIL_APP_PASSWORD  # App-specific password for Gmail

    to_email = f"{phone_number}@{carrier_domain}"
    msg = MIMEText(message)
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(msg)
        print(f"SMS sent to {phone_number}")

def process_text(text):
    """
    Processes the input text to extract distinct sentences or long phrases.

    Args:
        text (str): The input text.

    Returns:
        list: A list of cleaned, distinct sentences or long phrases.
    """
    # Normalize the text by replacing non-breaking spaces and other similar entities
    text = text.replace("\u200B", "").replace("&#x200B;", "").replace("\u2019", "\'").replace("\u201c", "\"").replace("\u201d", "\"").replace("\u2014", "-").replace("\u2013", "-").replace("\u2026", "...").replace("\u00a0", " ")
    text = text.replace(".\"", ".\"\n").replace("!\"", "!\"\n").replace("!\"", "!\"\n")
    abbreviations = ["Mr.", "Mrs.", "Dr.", "Ms.", "Jr.", "Sr.", "etc.",".\"","!\"","?\""]

    for i, abbr in enumerate(abbreviations):
        text = text.replace(abbr, f"__ABBR{i}__")
    
    text = text.replace(".",".\n").replace("?","?\n").replace("!","!\n")

    sentences = re.split(r'[\n]+|\n+', text)

    # Restore abbreviations from placeholders
    restored_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        for i, abbr in enumerate(abbreviations):
            sentence = sentence.replace(f"__ABBR{i}__", abbr)
        if sentence:  # Add only non-empty sentences
            if len(sentence) > 1:
                restored_sentences.append(sentence)

    # Clean up each sentence by removing unwanted characters but preserving common symbols
    cleaned_sentences = [
        re.sub(r'[^\w\s\'\",.?!-]', '', sentence) for sentence in restored_sentences
    ]

    return cleaned_sentences

def main():
    checker = []
    with open("sourced_content/"+checkfile_path, "r") as f:
        checker = f.read().split(',')

    text = ""
    title = ""
    with open("sourced_content/"+input_file, "r") as f:
        text_temp = json.load(f)

        i = 0
        story = text_temp[i]
        while story["id"] in checker:
            i += 1
            story = text_temp[i]
        
        with open("sourced_content/"+checkfile_path, "a") as f:
            f.write(f"{story['id']},")

        text = story["text"]
        title = story["title"]

    if os.path.exists('output_audio'):
        shutil.copy('output_audio', 'archive/output_audio')
        shutil.rmtree('output_audio', ignore_errors=True)

    # print(text)
    sentences = process_text(text)
    text_to_speech_by_sentence(sentences, audio_dir, ELEVENLABS_API_KEY)
    # print(f"Generated (Really reused) audio for {title}")

    search_phrase = "horror "+title
    video_file = download_stock_footage(search_phrase, PEXELS_API_KEY)

    if video_file is None:
        print(f"Failed to download video for {title}")
        return
    
    video = create_video(sentences, audio_dir, video_file, output_file, font_size=10,font="Baskerville") #Georgia, Baskerville, Courier New NOT Helvetica Tahoma
    tosave_filename = f"output_vids/{title}.mp4"
    video.write_videofile(tosave_filename, fps=24, codec="libx264", audio_codec="aac")
    shutil.copy(tosave_filename, current_video_file)
    print(f"Video content written to {tosave_filename}")

    description = "" 
    tags = ["shorts", "horror", "creepy", "story", "storytime", "entertainment", "reddit", "creepypasta"]
    title = title + " #shorts #horror #reddit"
    title = title if len(title)<100 else title[:99]

    response = upload_to_youtube(current_video_file, title, description, tags, privacy_status="private")
    print(response)
    send_sms_via_email(phone_number=PHONE_NUMBER,message=response)

if __name__ == "__main__":
    main()