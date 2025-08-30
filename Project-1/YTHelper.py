import os
import socket
from pytube import YouTube, request
from pytube.exceptions import VideoUnavailable, RegexMatchError

# ⏱️ Increase global timeout for all socket operations
socket.setdefaulttimeout(30)

# 🛠️ Patch pytube's request.get to include timeout
original_get = request.get
def patched_get(url, *args, **kwargs):
    kwargs.setdefault("timeout", 30)
    return original_get(url, *args, **kwargs)
request.get = patched_get

def download_youtube_video(url, output_folder):
    try:
        yt = YouTube(url)
    except RegexMatchError:
        print("❌ Invalid YouTube URL format.")
        return
    except VideoUnavailable:
        print("🚫 Video is unavailable.")
        return
    except Exception as e:
        print(f"⚠️ Failed to initialize YouTube object: {e}")
        return

    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not stream:
        print("⚠️ No suitable video stream found.")
        return

    title_safe = "".join([c if c.isalnum() or c in " ._-" else "_" for c in yt.title])
    video_path = os.path.join(output_folder, f"{title_safe}.mp4")
    info_path = os.path.join(output_folder, f"{title_safe}.txt")

    try:
        print(f"⬇️ Downloading video: {yt.title}")
        stream.download(output_path=output_folder, filename=f"{title_safe}.mp4")
        with open(info_path, "w", encoding="utf-8") as f:
            f.write(f"Title: {yt.title}\n\n")
            f.write(f"Description:\n{yt.description}")
        print(f"✅ Video saved to: {video_path}")
        print(f"📝 Info saved to: {info_path}")
    except Exception as e:
        print(f"❌ Download failed: {e}")

if __name__ == "__main__":
    url = input("🔗 Enter YouTube video URL: ").strip()
    output_folder = input("📁 Enter output folder path: ").strip()
    os.makedirs(output_folder, exist_ok=True)
    download_youtube_video(url, output_folder)