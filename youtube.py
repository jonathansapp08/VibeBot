import youtube_dl


def stream(url):
    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_title = info.get('title', None)
        video_id = info.get("id", None)
        video_url = info.get("url", None)
        return (video_title, video_id, video_url)


def download(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        video_id = info_dict.get("id", None)
        video_url = info_dict.get("url", None)
        return (video_title, video_id, video_url)
