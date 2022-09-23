import os
import time
import wave
import threading
import tkinter as tk
import pyaudio


class VoiceRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False,False)
        self.root.geometry("200x100")
        self.button = tk.Button(text="Mic Off!",font=["sans-serif",20,"bold"],command=self.runMic)
        self.button.pack()
        self.label = tk.Label(text="00:00:00",font=["sans-serif",20,"bold"])
        self.label.pack()
        self.recording = False 
        self.root.mainloop()

    def runMic(self):
        self.btnText = self.button.cget("text")
        if(self.btnText == "Mic Off!"):
            self.button["text"] = "Mic On!"
            self.recording = True
            threading.Thread(target=self.record).start()

        else:
            self.button["text"] = "Mic Off!"
            self.recording = False


    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
        frames = []
        start = time.time()
        while self.recording:
            data = stream.read(1024)
            frames.append(data)
            passed = time.time() - start
            secs,minutes = passed % 60,passed // 60
            hours = minutes // 60
            self.label.config(text=f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        i =1 

        while exists:
            if(os.path.exists(f"recording{i}.wav")):
                i +=1
            else:
                exists = False

        
        sound_file = wave.open(f"recording{i}.wav","wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()

VoiceRecorder()