import pathlib
from pytube import YouTube
from tkinter import *
from tkinter import messagebox, filedialog



rt = Tk()
rt.geometry("500x110")
rt.title("YT Downloader")
rt.resizable(0,0)
rt.config(background="#FFF")

vid_link = StringVar()
dw_path = StringVar()

def bw():
    dw_dir=filedialog.askdirectory(initialdir=pathlib.Path.cwd())
    dw_path.set(dw_dir)

def dw():
    link= vid_link.get()
    dw_folder = dw_path.get()
    vid = YouTube(link)
    stream = vid.streams.get_highest_resolution()
    stream.download(dw_folder)
    messagebox.showinfo("Success!","Downloaded to:"+dw_folder)

def window():
    link_lbl = Label(rt, text="Video link", width=20)
    link_lbl.grid(row=1,column=0,padx=5,pady=5)
    link_txt = Entry(rt,width=55,textvariable=vid_link)
    link_txt.grid(row=1,column=1,padx=5,pady=5,columnspan=2)

    dest_lbl = Label(rt, text="Destination", width=20)
    dest_lbl.grid(row=2,column=0,padx=5,pady=5)
    dest_txt = Entry(rt,width=40,textvariable=dw_path)
    dest_txt.grid(row=2,column=1,padx=5,pady=5)

    browse = Button(rt, text="Browse", command=bw,width=10,bg="#E3242B")
    browse.grid(row=2,column=2,padx=1,pady=1)

    download = Button(rt, text="Download", command=dw,width=20,bg="#E3242B")
    download.grid(row=3, column=1,padx=3, pady=3)

window()
rt.mainloop()