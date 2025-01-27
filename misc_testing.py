import requests
import json
import shutil
import re

# api_key = "sk_0450317123f76dedacc28fa33b8a76ace49efea14b55a941"
# headers = {"xi-api-key": api_key}
# response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)

import re

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
    # Define abbreviations to preserve (common titles and abbreviations with periods)
    abbreviations = ["Mr.", "Mrs.", "Dr.", "Ms.", "Jr.", "Sr.", "etc.",".\"","!\"","?\""]

    # Temporarily replace abbreviations with placeholders to prevent splitting them
    for i, abbr in enumerate(abbreviations):
        text = text.replace(abbr, f"__ABBR{i}__")
    
    text = text.replace(".",".\n").replace("?","?\n").replace("!","!\n")


    # Split text into sentences based on common sentence delimiters
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


# Example inputs
texts = [
    "\"How to hide bodies\"\n\n\"how to clean up blood\"\n\n\"Penalty for homicide.\"\n\n&#x200B;\n\nMy entire search history is filled with this crap.\n\nIt must be my wife, I know for sure.\n\nI had deleted my entire search history two years ago but she keeps putting them back in.\n\nShe still isn't over the fact I killed her.",
    "I remember the old days, when post would get thousands of upvotes.\n\nIt was a glorious era. But now, stories barely get over the 500 mark.\n\nThis subreddit is dying but no one has asked why people have stopped reading and posting?\n\nThey keep browsing and lurking, slowly but surely noticing that there are less and less people on this subreddit.\n\n\nI am so proud of myself for accomplishing this.\nAnd I'm coming for you too.",
    "Mommy and Daddy both cry. They say it’s ok, they don’t mind who I pick, that they understand it’s such a difficult choice to make.\n\nDaddy says I should go with him, it’ll be much easier that way.\n\nMommy talks over him and insists that I should pick her, it’s ok if I pick her.\n\nDaddy says it’ll be less painful for me to go with him. Mommy says that’s not true, it should be her.\n\nThey both say they love me and it’s ok, I can go with whoever I want, it’ll all be ok and they won’t love me any less.\n\nThe scary masked man says he doesn’t care who I pick, but I have to choose quickly. He says I have to pick, or he’ll shoot both of them.",
    "“Daddy, are we nearly there?” She asked groggily. “I’m so cold”\n\n“Nearly there princess, just a few more minutes.” \n\n“I love you daddy.”\n\n“I love you too princess, I’ll be with you soon.” I cried, knowing she wouldn’t make it. I still carried her out the wreckage. I knew it was gonna be the only thing that would keep me warm in the mountains for a while, as well as my sole source of food.",
    "I love my husband. I know he isn’t cheating on me. \n\nNow, other women might be suspicious if their husband started coming home in different clothes than he left in. But not me. I trust him. I know he’s not cheating on me. \n\nOther women might be suspicious if their husband started spending longer hours at the office. \n\nOther women would jump to conclusions seeing their husband with so many younger girls. “Friends from work” he calls them. \n\nOther women might be upset constantly seeing the girls that take up so much of their husbands time. Reminders of the fact he’s never home. \n\nBut not me. \n\nWhen I watch the news and I see the pictures their families chose for the missing posters I can’t help but smile. \n\nMy husband isn’t cheating on me."
]

# # Process each text and print the results
# for idx, text in enumerate(texts, start=1):
#     print(f"Processed sentences from text {idx}:")


with open("sourced_content/ShortScaryStories.json", "r") as f:
    text_temp = json.load(f)
    for story in text_temp:
        print(story["title"])
        sentences = process_text(story['text'])
        for sentence in sentences:
            print(f"- {sentence}")
        print(story["url"])
        print()

    