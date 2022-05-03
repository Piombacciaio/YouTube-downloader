import PySimpleGUI as sg, moviepy.editor, os, pathlib, sys, ctypes
from pytube import YouTube as yt
from tkinter import filedialog

ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )

sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=0, cols=0))
sg.theme('DarkBlack')
info_tab = [

    [sg. Text('Title:'),sg.Text('', key = '-TITLE-')],
    [sg.Text('Length:'), sg.Text('', key = '-LENGTH-')],
    [sg.Text('Views:'),sg.Text('', key = '-VIEWS-')],
    [sg.Text('Author: '), sg.Text('', key = '-AUTHOR-')],
    [sg. Text('Description: '),
    sg. Multiline('', key ='-DESCRIPTION-', size = (40, 20), disabled = True)]

]

download_tab = [

    [sg.Frame('Highest Quality', 
        [[
            sg.Button('Download', key='-HIGH-'),
            sg.Text('', key='-HIGHRES-'),
            sg.Text('', key='-HIGHSIZE-')
        ]])
    ],

    [sg.Frame('Lowest Quality', 
        [[
            sg.Button('Download', key='-LOW-'),
            sg.Text('', key='-LOWRES-'),
            sg.Text('', key='-LOWSIZE-')
        ]])
    ],

    [sg.Frame('Only Audio', 
        [[
            sg.Button('Download', key='-AUDIO-'),
            sg.Text('', key='-AUDIOSIZE-')
        ]])
    ],

    [sg.VPush()],

    [sg.Progress(100, size=(10,10), expand_x=True, key='-PROGRESSBAR-')]

]

layout = [[
    sg.TabGroup([[
        sg.Tab("Video info", info_tab),
        sg.Tab("Video download", download_tab)
    ]])
]]

start_layout = [[sg.Input(key='-LINK-'), sg.Button('Search')]]
window = sg.Window("Youtube Downloader", start_layout, icon="icon.ico", titlebar_icon="icon.ico")

def progress(stream, chunk, bytes):

    progress = 100 - (bytes/stream.filesize * 100)
    window['-PROGRESSBAR-'].update(progress)

def completed(stream, filepath):
    window['-PROGRESSBAR-'].update(0)

sg.Popup('This software is for educational purposes only. The creator will not be responsible for any illegal use.', title='INFO', icon="icon.ico")

while True:

    try:

        event, values = window.read()

        if event == sg.WIN_CLOSED:

            break
        
        if event == 'Search':

            try:

                window.close()

                video = yt(values['-LINK-'], on_progress_callback= progress, on_complete_callback= completed)

                window = sg.Window("Youtube Downloader", layout, finalize=True, icon="icon.ico", titlebar_icon="icon.ico")
                window['-TITLE-'].update(video.title)
                window['-LENGTH-'].update(f'{round (video.length / 60, 2)} minutes')
                window['-VIEWS-'].update(video.views)
                window['-AUTHOR-'].update(video.author)
                window['-DESCRIPTION-'].update(video.description)
                
                window['-HIGHSIZE-'].update(f'{round(video.streams.get_highest_resolution().filesize / 1048576, 1)} MB')
                window['-HIGHRES-'].update(video.streams.get_highest_resolution().resolution)

                window['-LOWSIZE-'].update(f'{round(video.streams.get_lowest_resolution().filesize / 1048576, 1)} MB')
                window['-LOWRES-'].update(video.streams.get_lowest_resolution().resolution)

                window['-AUDIOSIZE-'].update(f'{round(video.streams.get_audio_only().filesize / 1048576, 1)} MB')

            except Exception as e:

                sg.PopupError(f"The following error caused the program to crash.\n{e}",title="Error!", icon="icon.ico")
        
        if event == '-LOW-':
                    
            video.streams.get_lowest_resolution().download(output_path=filedialog.askdirectory(initialdir=pathlib.Path.cwd()))
        
        if event == '-HIGH-':
        
            video.streams.get_highest_resolution().download(output_path=filedialog.askdirectory(initialdir=pathlib.Path.cwd()))
        
        if event == '-AUDIO-':
        
            toconvert = video.streams.get_lowest_resolution().download(output_path=filedialog.askdirectory(initialdir=pathlib.Path.cwd()))
            name = os.path.basename(toconvert)[:-4]
            vid = moviepy.editor.VideoFileClip(fr"{toconvert}")
            
            vid.audio.write_audiofile(f"{name}.mp3")
            vid.close()
            os.remove(toconvert)
    
    except Exception as e:

        sg.PopupError(f"The following error caused the program to crash.\n{e}",title="Error!", icon="icon.ico")

window.close()