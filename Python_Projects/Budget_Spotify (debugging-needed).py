import os
import glob
import random
from tkinter import *
from tkinter import filedialog, ttk
from pygame import mixer
from moviepy.editor import AudioFileClip
import threading
import pygame
import time

class VideoPlayer:

    def __init__(self, master):
        self.master = master
        self.master.title("MP3 Audio Player")
        
        # Initialize pygame mixer for playing audio
        mixer.init()
        # Add a new call to `check_music_end` every 1000 ms
        self.master.after(1000, self.check_music_end)

        self.loop = BooleanVar()
        self.shuffle = BooleanVar()
        self.current = 0
        self.paused = False
        self.directory = ""

        # Create control buttons
        self.dir_button = Button(master, text="Choose Directory", command=self.choose_directory)
        self.dir_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.dir_label = Label(master, text="Directory not chosen")
        self.dir_label.grid(row=0, column=0, padx=250, pady=10, sticky='w')

        self.play_pause_button = Button(master, text="Play", command=self.play_pause, state=DISABLED)
        self.play_pause_button.grid(row=4, column=2, padx=10, pady=10, sticky='nsew')

        self.prev_button = Button(master, text="Prev", command=self.prev, state=DISABLED)
        self.prev_button.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        self.next_button = Button(master, text="Next", command=self.next, state=DISABLED)
        self.next_button.grid(row=4, column=3, padx=10, pady=10)

        self.loop_button = Checkbutton(master, text="Loop", variable=self.loop, state=DISABLED)
        self.loop_button.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.shuffle_button = Checkbutton(master, text="Shuffle", variable=self.shuffle, state=DISABLED)
        self.shuffle_button.grid(row=1, column=0, padx=250, pady=10, sticky='w')

        self.volume_scale = Scale(master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(0.5)  # Set the default volume to 50%
        self.volume_scale.grid(row=2, column=0, columnspan=6, sticky='we', padx=10, pady=10)

        # Configuring the root window to expand the grid when the window is resized
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Handle window closing event
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Timer thread reference
        self.timer_thread = None
        self.timer_paused = False
        self.timer_stop_flag = False
        self.timer_condition = threading.Condition()

    def convert_to_mp3(self, mp4_path):
        mp3_path = mp4_path.replace('.mp4', '.mp3')
        if not os.path.isfile(mp3_path): # convert only if mp3 file does not exist
            audio = AudioFileClip(mp4_path)
            audio.write_audiofile(mp3_path)
        return mp3_path

    def choose_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:  # Check if a directory has been selected
            self.filelist = glob.glob(self.directory + '/*.mp4')
            self.dir_label.configure(text="Directory chosen successfully!")
            self.playlist = ttk.Treeview(self.master, columns=("Song"), show='headings')
            self.playlist.heading("Song", text="Song")
            for file in self.filelist:
                mp3_file = self.convert_to_mp3(file)
                self.playlist.insert("", 'end', text=os.path.basename(mp3_file), values=(os.path.basename(mp3_file),))
            self.playlist.bind('<Double-1>', self.select_song)
            self.playlist.grid(row=3, column=0, columnspan=6, sticky='nsew', padx=10, pady=10)

            self.play_pause_button['state'] = NORMAL
            self.prev_button['state'] = NORMAL
            self.next_button['state'] = NORMAL
            self.loop_button['state'] = NORMAL
            self.shuffle_button['state'] = NORMAL

    def set_volume(self, val):
        mixer.music.set_volume(float(val))

    def pause_timer(self):
        self.timer_paused = True

    def resume_timer(self):
        self.timer_paused = False
        with self.timer_condition:
            self.timer_condition.notify()

    def stop_timer(self):
        self.timer_stop_flag = True
        with self.timer_condition:
            self.timer_condition.notify()

    def start_timer(self, duration):
        def timer_thread_func():
            remaining_time = duration
            while remaining_time > 0 and not self.timer_stop_flag:
                if self.timer_paused:
                    with self.timer_condition:
                        self.timer_condition.wait()
                else:
                    remaining_time -= 1
                    time.sleep(1)

            if not self.timer_stop_flag:
                self.song_end()

        self.timer_thread = threading.Thread(target=timer_thread_func)
        self.timer_thread.start()

    def play_pause(self):
        if not self.filelist:
            return
        if self.paused:
            self.paused = False
            self.play_pause_button.configure(text="Pause")
            if self.timer_paused:
                self.timer_paused = False
                self.resume_timer()
                mixer.music.unpause()  # Resume audio playback
            else:
                self.play()
        else:
            if mixer.music.get_busy():
                self.paused = True
                self.play_pause_button.configure(text="Play")
                mixer.music.pause()
                self.pause_timer()
            else:
                self.paused = False
                self.play_pause_button.configure(text="Pause")
                self.play()

    def play(self):
        file = self.filelist[self.current].replace('.mp4', '.mp3')
        if mixer.music.get_busy() and self.timer_paused:
            mixer.music.unpause()  # Resume audio playback if paused
            self.resume_timer()  # Resume the timer
        else:
            mixer.music.load(file)
            mixer.music.play()
            self.playlist.selection_clear()
            self.playlist.selection_set(self.playlist.get_children()[self.current])
            
        # Set an event to automatically play the next song
        mixer.music.set_endevent(pygame.USEREVENT)

        song_length = int(mixer.Sound(file).get_length()) + 2
        print(f"Playing song {file} for {song_length} seconds")
        self.stop_timer()
        self.start_timer(song_length)

    def check_music_end(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if not self.loop.get():
                    self.next()
        self.master.after(1000, self.check_music_end)

    def song_end(self):
        if self.loop.get():
            self.play()
        else:
            self.next()

    def next(self):
        if not self.filelist:
            return
        self.current = (self.current + 1) % len(self.filelist) if not self.shuffle.get() else random.randint(0, len(self.filelist)-1)
        if self.current == 0 and not self.loop.get():
            self.play()
        else:
            self.play()


    def prev(self):
        if not self.filelist:
            return
        self.current = (self.current - 1) % len(self.filelist) if not self.shuffle.get() else random.randint(0, len(self.filelist)-1)
        self.play()

    def select_song(self, event):
        self.current = self.playlist.index(self.playlist.selection()[0])
        self.play()

    def on_closing(self):
        if self.timer_thread:
            self.stop_timer()
            self.timer_thread.join()
        if mixer.music.get_busy():
            mixer.music.stop()
        self.master.destroy()

root = Tk()
player = VideoPlayer(root)
root.mainloop()
