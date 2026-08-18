"""
Python Voice Recorder with GUI

Features:
- Start Recording
- Stop Recording
- Play Recording
- Save Recording
- Recording Timer
- Microphone input using sounddevice
- WAV audio file
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading
import time
import os
import subprocess
import platform


# ============================================================
# Settings
# ============================================================

SAMPLE_RATE = 44100
CHANNELS = 2

recording = None
is_recording = False
recording_thread = None
start_time = None


# ============================================================
# Start Recording
# ============================================================

def start_recording():
    global recording, is_recording, recording_thread, start_time

    if is_recording:
        return

    try:
        is_recording = True
        start_time = time.time()

        status_label.config(
            text="● Recording...",
            fg="red"
        )

        start_button.config(state="disabled")
        stop_button.config(state="normal")
        play_button.config(state="disabled")
        save_button.config(state="disabled")

        recording_thread = threading.Thread(
            target=record_audio,
            daemon=True
        )

        recording_thread.start()

        update_timer()

    except Exception as e:
        is_recording = False
        messagebox.showerror(
            "Recording Error",
            str(e)
        )


def record_audio():
    global recording

    try:
        recording = sd.rec(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16"
        )

        # Wait while recording
        while is_recording:
            time.sleep(0.1)

        sd.stop()

    except Exception as e:
        print("Recording error:", e)


# ============================================================
# Stop Recording
# ============================================================

def stop_recording():
    global is_recording

    if not is_recording:
        return

    is_recording = False

    sd.stop()

    status_label.config(
        text="Recording stopped",
        fg="green"
    )

    start_button.config(state="normal")
    stop_button.config(state="disabled")
    play_button.config(state="normal")
    save_button.config(state="normal")

    timer_label.config(text="00:00")


# ============================================================
# Timer
# ============================================================

def update_timer():
    if is_recording:
        elapsed = int(time.time() - start_time)

        minutes = elapsed // 60
        seconds = elapsed % 60

        timer_label.config(
            text=f"{minutes:02d}:{seconds:02d}"
        )

        root.after(1000, update_timer)


# ============================================================
# Save Recording
# ============================================================

def save_recording():
    global recording

    if recording is None:
        messagebox.showwarning(
            "No Recording",
            "Please record something first."
        )
        return

    filename = filedialog.asksaveasfilename(
        title="Save Recording",
        defaultextension=".wav",
        filetypes=[
            ("WAV Audio", "*.wav"),
            ("All Files", "*.*")
        ]
    )

    if filename:
        try:
            write(
                filename,
                SAMPLE_RATE,
                recording
            )

            status_label.config(
                text="Recording saved!",
                fg="green"
            )

            messagebox.showinfo(
                "Success",
                f"Recording saved successfully:\n\n{filename}"
            )

        except Exception as e:
            messagebox.showerror(
                "Save Error",
                str(e)
            )


# ============================================================
# Play Recording
# ============================================================

def play_recording():
    global recording

    if recording is None:
        messagebox.showwarning(
            "No Recording",
            "Please record something first."
        )
        return

    try:
        status_label.config(
            text="▶ Playing...",
            fg="blue"
        )

        sd.play(recording, SAMPLE_RATE)
        sd.wait()

        status_label.config(
            text="Playback finished",
            fg="green"
        )

    except Exception as e:
        messagebox.showerror(
            "Playback Error",
            str(e)
        )


# ============================================================
# Clear Recording
# ============================================================

def clear_recording():
    global recording

    sd.stop()

    recording = None

    status_label.config(
        text="Ready to record",
        fg="black"
    )

    timer_label.config(
        text="00:00"
    )

    play_button.config(
        state="disabled"
    )

    save_button.config(
        state="disabled"
    )


# ============================================================
# Exit Application
# ============================================================

def close_application():
    global is_recording

    is_recording = False
    sd.stop()

    root.destroy()


# ============================================================
# GUI
# ============================================================

root = tk.Tk()

root.title("Python Voice Recorder")
root.geometry("500x400")
root.resizable(False, False)

# Background
root.configure(bg="#f2f2f2")


# ============================================================
# Title
# ============================================================

title_label = tk.Label(
    root,
    text="🎙 Voice Recorder",
    font=("Arial", 26, "bold"),
    bg="#f2f2f2",
    fg="#222222"
)

title_label.pack(pady=(25, 10))


# ============================================================
# Subtitle
# ============================================================

subtitle_label = tk.Label(
    root,
    text="Record audio from your microphone",
    font=("Arial", 12),
    bg="#f2f2f2",
    fg="#666666"
)

subtitle_label.pack()


# ============================================================
# Timer
# ============================================================

timer_label = tk.Label(
    root,
    text="00:00",
    font=("Arial", 42, "bold"),
    bg="#f2f2f2",
    fg="#222222"
)

timer_label.pack(pady=25)


# ============================================================
# Status
# ============================================================

status_label = tk.Label(
    root,
    text="Ready to record",
    font=("Arial", 12, "bold"),
    bg="#f2f2f2",
    fg="black"
)

status_label.pack(pady=5)


# ============================================================
# Button Frame
# ============================================================

button_frame = tk.Frame(
    root,
    bg="#f2f2f2"
)

button_frame.pack(pady=20)


# ============================================================
# Start Button
# ============================================================

start_button = tk.Button(
    button_frame,
    text="● Start",
    command=start_recording,
    font=("Arial", 12, "bold"),
    width=10,
    height=2,
    bg="#4CAF50",
    fg="white",
    cursor="hand2"
)

start_button.grid(
    row=0,
    column=0,
    padx=5
)


# ============================================================
# Stop Button
# ============================================================

stop_button = tk.Button(
    button_frame,
    text="■ Stop",
    command=stop_recording,
    font=("Arial", 12, "bold"),
    width=10,
    height=2,
    bg="#f44336",
    fg="white",
    state="disabled",
    cursor="hand2"
)

stop_button.grid(
    row=0,
    column=1,
    padx=5
)


# ============================================================
# Play Button
# ============================================================

play_button = tk.Button(
    button_frame,
    text="▶ Play",
    command=play_recording,
    font=("Arial", 12, "bold"),
    width=10,
    height=2,
    bg="#2196F3",
    fg="white",
    state="disabled",
    cursor="hand2"
)

play_button.grid(
    row=0,
    column=2,
    padx=5
)


# ============================================================
# Save Button
# ============================================================

save_button = tk.Button(
    root,
    text="💾 Save Recording",
    command=save_recording,
    font=("Arial", 12, "bold"),
    width=20,
    height=2,
    bg="#673AB7",
    fg="white",
    state="disabled",
    cursor="hand2"
)

save_button.pack(pady=5)


# ============================================================
# Clear Button
# ============================================================

clear_button = tk.Button(
    root,
    text="Clear",
    command=clear_recording,
    font=("Arial", 10),
    width=10,
    cursor="hand2"
)

clear_button.pack(pady=5)


# ============================================================
# Close Window
# ============================================================

root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)


# ============================================================
# Start GUI
# ============================================================

root.mainloop()