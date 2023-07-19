from pytube import YouTube
from urllib.error import HTTPError

save_path = r"C:\Users\Yasme\Desktop\YT_Vids_OST\Riot_Soundtracks"
links = []

from pytube import YouTube

def download_videos(url_list):
    for url in url_list:
        try:
            youtube = YouTube(url)
            video = youtube.streams.get_highest_resolution()
            video.download()

        except HTTPError as e:
            if e.code == 410:
                print("Video is no longer available (HTTP Error 410: Gone)")
            else:
                print("Error while downloading the video:", str(e))
        except Exception as e:
            print("Error while downloading the video:", str(e))

    print("Task completed!")

    
# Download the list of YouTube video links from a file
with open(r"C:\Users\Yasme\Desktop\YT_Vids_OST\Riot_Soundtracks\Riot_OST_Links.txt", "r") as links_file:
    for link in links_file:
        links.append(link)

download_videos(links)
