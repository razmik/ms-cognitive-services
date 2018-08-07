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

        self.label_vision_key = Label(frame, text="Vision API Key")
        self.label_vision_key.grid(row=1, sticky=E)

        self.entry_vision_key = Entry(frame)
        self.entry_vision_key.grid(row=1, column=1)

        self.label_emotion_key = Label(frame, text="Emotion API Key")
        self.label_emotion_key.grid(row=2, sticky=E)

        self.entry_emotion_key = Entry(frame)
        self.entry_emotion_key.grid(row=2, column=1)

        self.label_url = Label(frame, text="URL")
        self.label_url.grid(row=3, sticky=E)

        self.entry_url = Entry(frame)
        self.entry_url.grid(row=3, column=1)

        self.label_frame_rate = Label(frame, text="Frame Rate")
        self.label_frame_rate.grid(row=4, sticky=E)

        self.entry_frame_rate = Entry(frame)
        self.entry_frame_rate.grid(row=4, column=1)

        self.button_image_url = Button(frame, text="Analyze Image from URL")
        self.button_image_url.bind("<Button-1>", self.analyze_image_url)
        self.button_image_url.grid(row=5, column=1, sticky=E)
        self.button_image_url.config(width=20)

        self.button_image_file = Button(frame, text="Analyze Image from File")
        self.button_image_file.bind("<Button-1>", self.analyze_image_file)
        self.button_image_file.grid(row=6, column=1, sticky=E)
        self.button_image_file.config(width=20)

        self.button_surveillance = Button(frame, text="Video Surveillance")
        self.button_surveillance.bind("<Button-1>", self.surveillance)
        self.button_surveillance.grid(row=7, column=1, sticky=E)
        self.button_surveillance.config(width=20)
        self.surveillance_emotions = IntVar()
        self.check_box_surveillance = Checkbutton(frame, text="Enable Emotions", variable=self.surveillance_emotions)
        self.check_box_surveillance.grid(row=7, column=2)

        self.button_video_analysis = Button(frame, text="Video Analyze")
        self.button_video_analysis.bind("<Button-1>", self.video_analyze)
        self.button_video_analysis.grid(row=8, column=1, sticky=E)
        self.button_video_analysis.config(width=20)
        self.video_emotions = IntVar()
        self.check_box_video = Checkbutton(frame, text="Enable Emotions", variable=self.video_emotions)
        self.check_box_video.grid(row=8, column=2)

    def analyze_image_url(self, event):
        image_analyzer_object = importlib.import_module('image_analyzer')
        analyzer = image_analyzer_object.getAnalyzer(self.entry_vision_key.get())
        analyzer.analyze_url(self.entry_url.get())

    def analyze_image_file(self, event):
        filename = filedialog.askopenfilename()
        image_analyzer_object = importlib.import_module('image_analyzer')
        analyzer = image_analyzer_object.getAnalyzer(self.entry_vision_key.get())
        analyzer.analyze_file(filename)

    def surveillance(self, event):
        emotion_status = True if self.surveillance_emotions.get() == 1 else False
        framerate = int(self.entry_frame_rate.get()) if len(self.entry_frame_rate.get()) > 0 else 150

        if len(self.entry_vision_key.get()) > 1:
            if emotion_status and len(self.entry_emotion_key.get()) > 0:
                self.video_analyzer.start_capture(framerate, self.entry_vision_key.get(), self.entry_emotion_key.get(),
                                                  emotion_status, None)
            elif emotion_status and len(self.entry_emotion_key.get()) <= 0:
                print("Pleaes enter the Emotion API key")
            else:
                self.video_analyzer.start_capture(framerate, self.entry_vision_key.get(), self.entry_emotion_key.get(),
                                                  emotion_status, None)
        else:
            print("Pleaes enter the Vision API key")

    def video_analyze(self, event):
        filename = filedialog.askopenfilename()
        framerate = int(self.entry_frame_rate.get()) if len(self.entry_frame_rate.get()) > 0 else 150
        emotion_status = True if self.video_emotions.get() == 1 else False

        if len(self.entry_vision_key.get()) > 1:
            if emotion_status and len(self.entry_emotion_key.get()) > 0:
                self.video_analyzer.start_capture(framerate, self.entry_vision_key.get(), self.entry_emotion_key.get(),
                                                  emotion_status, filename)
            elif emotion_status and len(self.entry_emotion_key.get()) <= 0:
                print("Pleaes enter the Emotion API key")
            else:
                self.video_analyzer.start_capture(framerate, self.entry_vision_key.get(), self.entry_emotion_key.get(),
                                                  emotion_status, filename)
        else:
            print("Pleaes enter the API key")


# create a blank windows
root = Tk()

b = AnalyzerView(root)

# continue the display
root.mainloop()