from tkinter import *
import math
from tkinter import messagebox
from tkinter.ttk import Progressbar
import pygame
import sys
import os

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Segoe UI"
work_dur = 25
short_break_dur = 5
long_break_dur = 20
reps = 0
timer = None
paused = False
remaining_time = 0

pygame.mixer.init()
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder when bundled
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file=resource_path("tomato.png"))
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)
progress = Progressbar(window, orient="horizontal", length=200, mode="determinate")
progress.grid(column=1, row=2, pady=10)


def count_down(count):
    if paused:
        global remaining_time
        remaining_time = count
        return

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    # Update progress bar
    total_time = work_dur * 60 if reps % 2 != 0 else short_break_dur * 60
    if reps % 8 == 0:
        total_time = long_break_dur * 60
    progress['maximum'] = total_time
    progress['value'] = total_time - count

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        if reps % 2 != 0: # Work session ended
            play_sound(resource_path("sounds/work_end.mp3"))
        else: # Break session ended
            play_sound(resource_path("sounds/break_end.mp3"))
        start_timer()
        checks = ""
        for _ in range(math.floor(reps / 2)):
            checks += "✔"
        checks_label.config(text=checks)

def start_timer():
    global reps
    reps += 1

    work_sec = work_dur * 60
    short_break_sec = short_break_dur * 60
    long_break_sec = long_break_dur * 60

    if reps % 8 == 0:
        main_label.config(text="Break", fg=GREEN)
        count_down(long_break_sec)
    elif reps % 2 == 0:
        main_label.config(text="Break", fg=PINK)
        count_down(short_break_sec)
    else:
        main_label.config(text="Work", fg=RED)
        count_down(work_sec)

def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    main_label.config(text="Timer")
    checks_label.config(text="")
    progress['value'] = 0
    global reps
    reps = 0

def pause():
    global paused
    paused = not paused
    if paused:
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")
        count_down(remaining_time)

def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def open_settings():
    settings_win = Toplevel(window)
    settings_win.title("Settings")
    settings_win.config(padx=20, pady=20, bg=YELLOW)

    # Work duration
    Label(settings_win, text="Work Duration (min):", bg=YELLOW).grid(row=0, column=0, sticky="w")
    work_entry = Entry(settings_win, width=5)
    work_entry.insert(0, str(work_dur))
    work_entry.grid(row=0, column=1)

    # Short break
    Label(settings_win, text="Short Break (min):", bg=YELLOW).grid(row=1, column=0, sticky="w")
    short_entry = Entry(settings_win, width=5)
    short_entry.insert(0, str(short_break_dur))
    short_entry.grid(row=1, column=1)

    # Long break
    Label(settings_win, text="Long Break (min):", bg=YELLOW).grid(row=2, column=0, sticky="w")
    long_entry = Entry(settings_win, width=5)
    long_entry.insert(0, str(long_break_dur))
    long_entry.grid(row=2, column=1)

    def save_settings():
        global work_dur, short_break_dur, long_break_dur
        try:
            work_dur = int(work_entry.get())
            short_break_dur = int(short_entry.get())
            long_break_dur = int(long_entry.get())
            settings_win.destroy()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for all durations.")

    Button(settings_win, text="Save", command=save_settings).grid(row=3, column=0, columnspan=2, pady=10)


main_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 40, "bold"))
main_label.grid(column=1, row=0)

checks_label = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 10))
checks_label.grid(column=1, row=3)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2, padx=5, pady=5)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2, padx=5, pady=5)

pause_button = Button(text="Pause", highlightthickness=0, command=pause)
pause_button.grid(column=1, row=4, pady=5)

settings_button = Button(text="Settings", highlightthickness=0, command=open_settings)
settings_button.grid(column=1, row=5, pady=10)






window.mainloop()