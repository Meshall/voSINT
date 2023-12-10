import sys
import os
import cv2
import requests
import configparser
from pathlib import Path
from modules.video_search import serpapi_reverse_image_search
from modules.upload import upload_image
from modules.html_generator import generate_html
from tqdm import tqdm
import time
import subprocess


def main(video_path):
    # Load the ASCII art header and word
    ASCII_Header = """
    #               _____ _____   ________
    #   _   ______ / ___//  _/ | / /_  __/
    #  | | / / __ \\__ \ / //  |/ / / /   
    #  | |/ / /_/ /__/ // // /|  / / /    
    #  |___/\____/____/___/_/ |_/ /_/     
    #                                     
    """
    initi = "ᴹᵉˢʰᵃˡ ᴬˡᵒᵗᵃᶦᵇᶦ"

    logo_file = "ascii.txt"

    with open(logo_file, 'r') as ASCII_logo_file:
        ASCII_logo = ASCII_logo_file.read()

    # Print the ASCII art header, word, and logo
    print(ASCII_logo)
    print(initi)
    print(ASCII_Header)

    print()  

    
    print("Searching... Please wait.")

    ellipsis = ""
    for _ in range(20):
        print(f"\rSearching{ellipsis}", end="")
        ellipsis = ellipsis + ":.'.:"
        time.sleep(0.5)

    print()  # a newline after animation

    #  directory path of the script
    
    script_dir = Path(__file__).parent.absolute()
    config_file = script_dir / "config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)
    api_key = config.get('API', 'API_KEY')
    video_capture = cv2.VideoCapture(video_path)
    success, frame = video_capture.read()
    video_capture.release()
    screenshot_path = script_dir / "screenshot.jpg"
    cv2.imwrite(str(screenshot_path), frame)

    ##Upload the frame to 0x0.st and get the URL
    img_url = upload_image(str(screenshot_path))

    # hitserpapi_reverse_image_search
    inline_images = serpapi_reverse_image_search(img_url, api_key, 0)

    # Extract vid file name w/ extension
    video_file_name = os.path.splitext(video_path)[0]
    html_content = generate_html(inline_images, video_file_name)
    results_dir = script_dir / "Results"
    results_dir.mkdir(parents=True, exist_ok=True)
    html_file_path = results_dir / f"{video_file_name}_sources.html"
    with open(html_file_path, 'w') as f:
        f.write(html_content)

   
    print(f'The results are saved into HTML file created as {html_file_path}')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python voSINT.py <video_path> or python voSINT.py <videos_dir>")
        sys.exit(1)

    path = sys.argv[1]
    if os.path.isfile(path):
        main(path)
    elif os.path.isdir(path):
        video_files = []
        for file in os.listdir(path):
            if file.lower().endswith(('.mp4', '.mov', '.avi')):
                video_files.append(os.path.join(path, file))
        if not video_files:
            print(f"No video files found in the specified directory: {path}")
        else:
            for video_file in video_files:
                # Get the directory path of the script
                script_dir = Path(__file__).parent.absolute()

                # Extract the video file name without extension
                video_file_name = os.path.splitext(os.path.basename(video_file))[0]

                # Specify the HTML file path
                html_file_path = script_dir / "Results" / f"{video_file_name}_sources.html"

                main(video_file)

                #Construct the system-specific command to open the HTML file
                if os.path.exists(html_file_path):
                    if os.name == 'posix':
                        # Linux/macOS
                        subprocess.run(['xdg-open', html_file_path])
                    elif os.name == 'nt':
                        # Windows
                        subprocess.run(['start', html_file_path], shell=True)
    else:
        print(f"Error: Invalid path - {path}")

