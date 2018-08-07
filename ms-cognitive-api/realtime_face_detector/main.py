from tkinter import *
from tkinter import filedialog
import importlib


class AnalyzerView:

    def __init__(self, master):

        self.video_analyzer = importlib.import_module('video_analyzer').getAnalyzer()

        frame = Frame(master)
        frame.pack()

        self.label_title = Label(frame, text="MS Cognitive Services - Vision")
        self.label_title.grid(row=0, column=1)

        self.label_emotion_key = Label(frame, text="Face API Key")
        self.label_emotion_key.grid(row=2, sticky=E)

        """
        Reg date: 4/18/2018
        Endpoint: https://westcentralus.api.cognitive.microsoft.com/face/v1.0
        30,000 transactions, 20 per minute.
        Key 1: df901fd6c902465987defcb712b3a558
        
        Key 2: e0bbd184a23542729510ff8a3fc9ecad
        """

        emotion_key = StringVar()
        self.entry_emotion_key = Entry(frame, textvariable=emotion_key)
        self.entry_emotion_key.grid(row=2, column=1)
        emotion_key.set('df901fd6c902465987defcb712b3a558')

        self.label_url = Label(frame, text="URL")
        self.label_url.grid(row=3, sticky=E)

        self.entry_url = Entry(frame)
        self.entry_url.grid(row=3, column=1)

        self.label_frame_rate = Label(frame, text="Frame Rate")
        self.label_frame_rate.grid(row=4, sticky=E)

        frame_rate = StringVar()
        self.entry_frame_rate = Entry(frame, textvariable=frame_rate)
        self.entry_frame_rate.grid(row=4, column=1)
        frame_rate.set('150')

        self.button_surveillance = Button(frame, text="Video Surveillance")
        self.button_surveillance.bind("<Button-1>", self.surveillance)
        self.button_surveillance.grid(row=5, column=1, sticky=E)
        self.button_surveillance.config(width=20)
        self.surveillance_emotions = IntVar()
        self.check_box_surveillance = Checkbutton(frame, text="Face Detection", variable=self.surveillance_emotions)
        self.check_box_surveillance.grid(row=5, column=2)

    def surveillance(self, event):
        emotion_status = True if self.surveillance_emotions.get() == 1 else False
        framerate = int(self.entry_frame_rate.get()) if len(self.entry_frame_rate.get()) > 0 else 150

        if len(self.entry_emotion_key.get()) > 1:
            self.video_analyzer.start_capture(framerate, self.entry_emotion_key.get(), emotion_status)
        else:
            print("Pleaes enter a valid Face API key")


# create a blank windows
root = Tk()

b = AnalyzerView(root)

# continue the display
root.mainloop()