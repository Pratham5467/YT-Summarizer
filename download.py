from yt_dlp import YoutubeDL

def download_audio_from_url(url):
    video_info=YoutubeDL().extract_info(url=url,download=False)
    length=video_info["duration"]
    filename=f"./audio/youtube/{video_info['id']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }
    with YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
    return filename,length

if __name__=="__main__":
    url="https://www.youtube.com/watch?v=q_eMJiOPZMU"
    filename,length=download_audio_from_url(url)
    print(f"Audio file:{filename}with length{length}seconds")
    print("Done!")
    