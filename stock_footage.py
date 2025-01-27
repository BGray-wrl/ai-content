import requests
import os
from moviepy import VideoFileClip

# Function to download stock footage
def download_stock_footage(keyword, API_KEY, output_folder="stock_footage"):
    BASE_URL = "https://api.pexels.com/videos/search"
    headers = {"Authorization": API_KEY}
    params = {"query": keyword, "per_page": 1}  # Fetch one video for now

    # Make the API request
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["videos"]:
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
    # keyword = "creepy forest"
    # video_file = download_stock_footage(keyword)
    pass