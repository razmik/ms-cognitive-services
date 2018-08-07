from __future__ import print_function
import http.client, urllib.error
import numpy as np
import cv2
import json
from time import gmtime, strftime, sleep
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import sys


class ImageAnalyzer:
    def __init__(self):
        self.summary_vision = []
        self.summary_emotions = []
        self.display_video = False
        self.enable_emotions = False
        self.vision_api_key = None
        self.emotion_api_key = None
        self.original = "Original View"
        self.analyze_frame = "Analyzed View"
        self.data_folder = 'data/'
        self.data_folder_singles = 'data/'

    def start_process(self, frame_id, filenames, vision_api_key, emotion_api_key, enable_emotions=False, display=False):
        self.vision_api_key = vision_api_key
        self.emotion_api_key = emotion_api_key
        self.enable_emotions = enable_emotions
        self.display_video = display

        iteration = 1
        for file in filenames:

            if not isfile(file):
                return False

            if iteration % 15 == 0:
                print('Sleeping for 25 seconds.')
                sleep(25)

            with open(file, 'rb') as img:
                img_data = img.read()
                data8uint = np.fromstring(img_data, np.uint8)
                image = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
                self._process_frame(iteration, image, img_data)
            iteration += 1

        with open(self.data_folder + frame_id + '_vision.json', "w", encoding="utf8") as outfile:
            json.dump(self.summary_vision, outfile)
            self.summary_vision = []
            print('Dumping json for', frame_id)

        if enable_emotions:
            with open(self.data_folder + frame_id + '_emotion.json', "w", encoding="utf8") as outfile:
                json.dump(self.summary_emotions, outfile)
                self.summary_emotions = []

        return True

    def analyze_single(self, frame_id, filename, vision_api_key, emotion_api_key, enable_emotions=False, display=False):
        self.vision_api_key = vision_api_key
        self.emotion_api_key = emotion_api_key
        self.enable_emotions = enable_emotions
        self.display_video = display

        if not isfile(filename):
            return False

        with open(filename, 'rb') as img:
            img_data = img.read()
            data8uint = np.fromstring(img_data, np.uint8)
            image = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
            self._process_frame(1, image, img_data)

        with open(self.data_folder_singles + frame_id + '_vision.json', "w", encoding="utf8") as outfile:
            json.dump(self.summary_vision, outfile)
            self.summary_vision = []
            print('Dumping json for', frame_id)

        if enable_emotions:
            with open(self.data_folder_singles + frame_id + '_emotion.json', "w", encoding="utf8") as outfile:
                json.dump(self.summary_emotions, outfile)
                self.summary_emotions = []

        return True

    def _render_result_on_image(self, result, img, result_emotions):

        fontScale = 0.5
        fontThickness = 2

        if 'description' in result:
            caption = str(result['description']['captions'][0]['text'])
            cv2.putText(img, caption, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)
            secondary_tags = "secondary tags: " + str(result['description']['tags'])
            # cv2.putText(img, secondary_tags, (30, 160), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)

        if 'categories' in result:
            categoryName = sorted(result['categories'], key=lambda x: x['score'])[0]['name']
            # cv2.putText(img, categoryName, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)

        if 'tags' in result:
            primary_tags = []
            for item in result['tags']: primary_tags.append(item['name'])
            primary_tags = "primary tags: " + str(primary_tags)
            # cv2.putText(img, primary_tags, (30, 120), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)

        if 'faces' in result:
            for item in result['faces']:
                desc = item['gender'] + ", " + str(item['age'])
                left = item['faceRectangle']['left']
                top = item['faceRectangle']['top']
                height = item['faceRectangle']['height']
                width = item['faceRectangle']['width']
                cv2.rectangle(img, (left, top), (left + width, top + height), (255, 0, 0), 1)
                cv2.putText(img, desc, (left, top + height), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0),
                            fontThickness)

        if result_emotions is not None:
            img = self._render_emotions_on_image(result_emotions, img)

        return img

    def _render_emotions_on_image(self, result, img):
        fontScale = 0.5
        fontThickness = 2

        for face in result:
            left = face['faceRectangle']['left']
            top = face['faceRectangle']['top']
            emotions = ""

            for emo_name, emo_score in face['faceAttributes']['emotion'].items():
                if emo_score > 0.1:
                    emotions += emo_name + ':' + str(emo_score) + ' '

            cv2.putText(img, emotions, (left, top), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)

        return img

    def _connect_ms_emotion_api(self, data):
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.emotion_api_key,
        }

        params = urllib.parse.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        })

        body = data
        # https://westcentralus.api.cognitive.microsoft.com/face/v1.0
        try:
            conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
            conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
            response = conn.getresponse()
            result = json.loads(response.read().decode("utf-8"))
            conn.close()

            return result

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return -1

    def _connect_ms_vision_api(self, data):

        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.vision_api_key,
        }
        params = urllib.parse.urlencode({
            'visualFeatures': 'Color,Categories,Tags,Description,Faces,ImageType,Adult',
            'language': 'en',
        })
        body = data
        # westcentralus.api.cognitive.microsoft.com/vision/v1.0
        try:
            conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
            conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
            response = conn.getresponse()
            result = json.loads(response.read().decode("utf-8"))
            conn.close()

            return result

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return -1

    def _process_frame(self, iteration, image, image_data):

        result_vision = self._connect_ms_vision_api(image_data)
        self.summary_vision.append(result_vision)
        print(iteration, strftime("%a, %d %b %Y %H:%M:%S +1030", gmtime()), result_vision)

        result_emotions = None
        if self.enable_emotions:
            result_emotions = self._connect_ms_emotion_api(image_data)
            self.summary_emotions.append(result_emotions)
            print(iteration, strftime("%a, %d %b %Y %H:%M:%S +1030", gmtime()), result_emotions)

        if result_vision is not None:
            processed_img = self._render_result_on_image(result_vision, image, result_emotions)

            if self.display_video:
                plt.imshow(processed_img)
                plt.show()


def getAnalyzer():
    return ImageAnalyzer()
