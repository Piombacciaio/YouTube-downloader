try:
    import colorama, ctypes, moviepy.editor ,os, pathlib
    from pytube import YouTube as yt
    from colorama import Fore
    from tkinter import filedialog

except Exception as m:

    print("Something Went Wrong\n")
    print(m)
    input()

ctypes.windll.kernel32.SetConsoleTitleW(f'Video Downloader | made by piombacciaio')
colorama.init()

logo = """ _   _ _     _                                          
| | | (_)   | |                                         
| | | |_  __| | ___  ___                                
| | | | |/ _` |/ _ \/ _ \                               
\ \_/ / | (_| |  __/ (_) |                              
 \___/|_|\__,_|\___|\___/                               
                                                        
______                    _                 _           
|  _  \                  | |               | |          
| | | |_____      ___ __ | | ___   __ _  __| | ___ _ __ 
| | | / _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
| |/ / (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
|___/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
                                                        
"""

def progress_bar(stream, chunk, bytes, color=Fore.CYAN):
    
    percent = bytes/stream.filesize * 100
    bar = "█" * (100 - int(percent)) + "-" * int(percent)
    print(f"\r|{color + bar + Fore.RESET}| {color}{100 - int(percent):.2f}{Fore.RESET}%", end="\r")

def progress_bar_completed(stream, file_path):
    bar = "█" * 100
    print(f"\r|{Fore.GREEN + bar + Fore.RESET}| {Fore.GREEN}100{Fore.RESET}%   ", end="\n")

def youtube(link = None):
    
    if link == None:
        link = input("YouTube link: ")
    
    video = yt(link, on_progress_callback= progress_bar, on_complete_callback= progress_bar_completed)
    print(f"\n[{Fore.GREEN}+{Fore.RESET}] Video Info:")
    print("    Title: ",video.title)
    print("    Number of views: ",video.views)
    print("    Length of video: ",video.length)
    print("    Rating of video: ",video.rating)

    quality_choice = input(f"""\n    Available video downloads:
        [{Fore.GREEN}1{Fore.RESET}] Highest ({video.streams.get_highest_resolution().resolution} / {round(video.streams.get_highest_resolution().filesize / 1048576, 1)} MB)
        [{Fore.GREEN}2{Fore.RESET}] Lowest ({video.streams.get_lowest_resolution().resolution} / {round(video.streams.get_lowest_resolution().filesize / 1048576, 1)} MB)
        [{Fore.GREEN}3{Fore.RESET}] Audio only (.mp3 / {round(video.streams.get_audio_only().filesize / 1048576, 1)} MB)
        [{Fore.GREEN}>{Fore.RESET}] """)
    
    if quality_choice == "1" or quality_choice.lower() == "highest":

        video.streams.get_highest_resolution().download(output_path=filedialog.askdirectory(initialdir=pathlib.Path.cwd()))
    
    elif quality_choice == "2" or quality_choice.lower() == "lowest":

        video.streams.get_lowest_resolution().download(output_path=filedialog.askdirectory(initialdir=pathlib.Path.cwd()))
    
    elif quality_choice == "3" or quality_choice.lower() == "audio only":

        toconvert = video.streams.get_lowest_resolution().download(output_path=filedialog.askdirectory(initialdir=pathlib.Path.cwd()))
        name = os.path.basename(toconvert)[:-4]
        vid = moviepy.editor.VideoFileClip(fr"{toconvert}")
        print(f"[{Fore.GREEN}+{Fore.RESET}] Creating MP3...")
        vid.audio.write_audiofile(f"{name}.mp3")
        vid.close()
        os.remove(toconvert)
    
    print(f"[{Fore.GREEN}+{Fore.RESET}] Downloaded")
    print(f"[{Fore.GREEN}+{Fore.RESET}] Press [ENTER] to continue...")
    input()
    os.system("cls")

def menu(print_logo = True):

    while True:

        if print_logo == True:

            print(Fore.BLUE + logo + Fore.RESET)

        print(f"[{Fore.GREEN}1{Fore.RESET}] YouTube\n[{Fore.GREEN}E{Fore.RESET}] Exit")
        choice = input(f"[{Fore.GREEN}>{Fore.RESET}] ")
        
        if choice == "1":

            youtube()
        
        elif choice.lower() == "e":

            exit(1)
        
        else:

            os.system("cls")
            menu()

input(f"[{Fore.GREEN}INFO{Fore.RESET}] This software is for educational purposes only. The creator will not be responsible for any illegal use.")
os.system("cls")
menu()