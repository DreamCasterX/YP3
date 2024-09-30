import yt_dlp
import os
import subprocess
import sys
from tqdm import tqdm

# ANSI 顏色代碼
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def install_ffmpeg_instructions():
    print("請先安裝 ffmpeg 才能繼續操作。")
    print("安裝說明：")
    if sys.platform.startswith('win'):
        print("Windows: 使用 Chocolatey 安裝，執行命令：choco install ffmpeg")
    elif sys.platform.startswith('darwin'):
        print("macOS: 使用 Homebrew 安裝，執行命令：brew install ffmpeg")
    elif sys.platform.startswith('linux'):
        print("Linux: 使用包管理器安裝，例如 Ubuntu 執行命令：sudo apt-get install ffmpeg")
    print("安裝完成後，請重新運行此程式。")

def progress_hook(d):
    if d['status'] == 'downloading':
        pbar.update(d['downloaded_bytes'] - pbar.n)
    elif d['status'] == 'finished':
        pbar.close()
        print("下載完成，正在轉換為 MP3...")

def download_youtube_audio(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            global pbar
            pbar = tqdm(total=info.get('filesize', 0), unit='B', unit_scale=True, desc=f"下載進度 - {info['title']}")
            
            ydl.download([url])
            
            base, ext = os.path.splitext(filename)
            new_file = base + '.mp3'
        
        print(f"成功下載並轉換為MP3: {GREEN}{new_file}{RESET}")
    except yt_dlp.utils.DownloadError as e:
        print(f"{RED}下載錯誤{RESET}")
    except Exception as e:
        print(f"{RED}發生未知錯誤{RESET}")
    finally:
        if 'pbar' in globals():
            pbar.close()

# 主程序
if __name__ == "__main__":
    if not check_ffmpeg():
        install_ffmpeg_instructions()
    else:
        youtube_urls = input("請輸入YouTube影片網址（多個網址請用空格分隔）: \n").split()
        for url in youtube_urls:
            print(f"\n正在處理: {url}")
            download_youtube_audio(url)
            
print("\n(按Enter結束)")
input()            
