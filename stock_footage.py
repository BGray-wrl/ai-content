import requests
import os
from moviepy import VideoFileClip
import json

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')


# Function to download stock footage
def download_stock_footage(keyword, API_KEY, output_folder="stock_footage"):
    BASE_URL = "https://api.pexels.com/videos/search"
    headers = {"Authorization": API_KEY}
    params = {"query": keyword, "per_page": 1, "page":1}  # Fetch one video for now

    # Make the API request
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print(type(data))
        print()
        print(data)
        print()
        for key in data.keys():
            print(key)

        if data["videos"]:
            i = 0
            with open("stock_footage/footage_used.txt", "r") as f:
                checker = f.read().split(',')
                print("checker",checker)
                print("id",data['videos'][i]['id'])
                print(data['videos'])

                if data['videos'] and str(data['videos'][0]['id']) in checker and response.status_code == 200:
                    i += 1
                    params["page"]+=1
                    response = requests.get(BASE_URL, headers=headers, params=params)
                    data = response.json()

                else:
                    if response.status_code == 200:
                        print("No more videos to use")
                        return None
                    print("Failed to fetch videos. Status Code: {response.status_code}")
                    return None
                    
                with open("stock_footage/footage_used.txt", "a") as f:
                    f.write(f"{data['videos'][0]['id']},")

            video_url = data["videos"][0]["video_files"][0]["link"]
            video_id = data["videos"][0]["id"]
            video_filename = f"{output_folder}/{keyword}_{video_id}.mp4"

            # Create output folder if it doesn't exist
            os.makedirs(output_folder, exist_ok=True)

            # Download the video file
            print(f"Downloading video: {video_url}")
            video_response = requests.get(video_url, stream=True)
            with open(video_filename, "wb") as f:
                for chunk in video_response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"Downloaded video saved as {video_filename}")
            return video_filename
        else:
            print(f"No videos found for keyword: {keyword}")
            return None
    else:
        print(f"Failed to fetch videos. Status Code: {response.status_code}")
        return None

# Example usage
if __name__ == "__main__":
    keyword = "horror "
    video_file = download_stock_footage(keyword,PEXELS_API_KEY)
    pass