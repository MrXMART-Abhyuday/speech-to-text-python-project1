import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import messagebox, filedialog

# Initialize recognizer
recognizer = sr.Recognizer()

# Create main window
root = tk.Tk()
root.title("🎤 Text & Speech Assistant")
root.geometry("600x520")
root.configure(bg="#222831")

# Default TTS settings
voice_rate = tk.IntVar(value=170)
voice_volume = tk.DoubleVar(value=1.0)
voice_gender = tk.StringVar(value="Female")

# --- Create a single reusable engine ---
def create_engine():
    e = pyttsx3.init()
    voices = e.getProperty('voices')
    if voice_gender.get() == "Female" and len(voices) > 1:
        e.setProperty('voice', voices[1].id)
    else:
        e.setProperty('voice', voices[0].id)
    e.setProperty('rate', voice_rate.get())
    e.setProperty('volume', voice_volume.get())
    return e

# Functions
def listen_and_convert():
    try:
        with sr.Microphone() as source:
            status_label.config(text="🎙 Listening... Speak now")
            root.update()
            audio = recognizer.listen(source)
            status_label.config(text="🧠 Recognizing...")
            root.update()

        text = recognizer.recognize_google(audio)
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, text)
        status_label.config(text="✅ Done!")
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, could not understand your voice.")
        status_label.config(text="❌ Try again.")
    except sr.RequestError:
        messagebox.showerror("Error", "Network error. Please check your connection.")
        status_label.config(text="🌐 Check your internet.")

def read_text():
    text = text_box.get(1.0, tk.END).strip()
    if text:
        status_label.config(text="🔊 Speaking...")
        root.update()

        engine = create_engine()
        engine.say(text)
        engine.runAndWait()
        engine.stop()

        status_label.config(text="✅ Done speaking!")
    else:
        messagebox.showwarning("Empty", "No text to read!")

def save_text():
    text = text_box.get(1.0, tk.END).strip()
    if text:
        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")])
        if file:
            with open(file, "w") as f:
                f.write(text)
            messagebox.showinfo("Saved", f"Text saved to {file}")

def clear_text():
    text_box.delete(1.0, tk.END)
    status_label.config(text="🧹 Text cleared!")


# UI
title_label = tk.Label(root, text="🎧 Voice Fusion Assitant",
                       font=("Arial", 16, "bold"), bg="#222831", fg="#EEEEEE")
title_label.pack(pady=15)

text_box = tk.Text(root, wrap="word", width=65, height=10, font=("Arial", 12),
                   bg="#393E46", fg="#EEEEEE", insertbackground="white")
text_box.pack(padx=10, pady=10)

button_frame = tk.Frame(root, bg="#222831")
button_frame.pack(pady=10)

listen_btn = tk.Button(button_frame, text="🎤 Listen & Convert", command=listen_and_convert,
                       bg="#00ADB5", fg="white", font=("Arial", 11, "bold"), width=14)
listen_btn.grid(row=0, column=0, padx=5)

read_btn = tk.Button(button_frame, text="🔊 Read Text", command=read_text,
                     bg="#00ADB5", fg="white", font=("Arial", 11, "bold"), width=14)
read_btn.grid(row=0, column=1, padx=5)

save_btn = tk.Button(button_frame, text="💾 Save Text", command=save_text,
                     bg="#00ADB5", fg="white", font=("Arial", 11, "bold"), width=14)
save_btn.grid(row=0, column=2, padx=5)

clear_btn = tk.Button(button_frame, text="🧹 Clear Text", command=clear_text,
                      bg="#FF6B6B", fg="white", font=("Arial", 11, "bold"), width=14)
clear_btn.grid(row=0, column=3, padx=5)

# Voice customizer
custom_frame = tk.LabelFrame(root, text="🎛 Voice Customizer", bg="#222831", fg="#00FFDD",
                             font=("Arial", 12, "bold"), padx=10, pady=10)
custom_frame.pack(padx=10, pady=10, fill="x")

tk.Label(custom_frame, text="Voice:", bg="#222831", fg="#EEEEEE",
         font=("Arial", 11)).grid(row=0, column=0, sticky="w")
voice_menu = tk.OptionMenu(custom_frame, voice_gender, "Male", "Female")
voice_menu.config(bg="#00ADB5", fg="white", font=("Arial", 10, "bold"), width=10)
voice_menu.grid(row=0, column=1, padx=10)

tk.Label(custom_frame, text="Speed:", bg="#222831", fg="#EEEEEE",
         font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
speed_slider = tk.Scale(custom_frame, from_=100, to=250, orient="horizontal",
                        variable=voice_rate, bg="#393E46", fg="white", length=200)
speed_slider.grid(row=1, column=1)

tk.Label(custom_frame, text="Volume:", bg="#222831", fg="#EEEEEE",
         font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
volume_slider = tk.Scale(custom_frame, from_=0.5, to=1.0, resolution=0.1,
                         orient="horizontal", variable=voice_volume,
                         bg="#393E46", fg="white", length=200)
volume_slider.grid(row=2, column=1)

status_label = tk.Label(root, text="Ready ✅", font=("Arial", 11),
                        bg="#222831", fg="#00FFDD")
status_label.pack(pady=10)

root.mainloop()