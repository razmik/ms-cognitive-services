from __future__ import print_function
import http.client, urllib.error
import numpy as np
import cv2
import json
from time import gmtime, strftime


class WebCamAnalyzer:

    def __init__(self):
        self.started = False

    def start_capture(self, frame_rate, vision_api_key, emotion_api_key, enable_emotions, filename):
        self.vision_api_key = vision_api_key
        self.emotion_api_key = emotion_api_key
        self.started = True
        self.enable_emotions = enable_emotions

        if filename is None:
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(filename)


        self.webcam_frame = "Camera View"
        self.analyze_frame = "Analyze View"
        cv2.namedWindow(self.webcam_frame, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.webcam_frame, 400, 320)
        cv2.namedWindow(self.analyze_frame, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.analyze_frame, 600, 400)

        iteration = 1
        while True:
            ret, frame = self.cap.read()
            cv2.imshow(self.webcam_frame, frame)

            if iteration % frame_rate == 0:
                self._process_frame(frame, cv2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            iteration += 1

        self.cap.release()
        cv2.destroyAllWindows()

    def _render_result_on_image(self, result, img, result_emotions):

        fontScale = 0.5
        fontThickness = 2

        if 'description' in result:
            caption = str(result['description']['captions'][0]['text'])
            cv2.putText(img, caption, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)
            secondary_tags = "secondary tags: " + str(result['description']['tags'])
            cv2.putText(img, secondary_tags, (30, 160), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)

        if 'categories' in result:
            categoryName = sorted(result['categories'], key=lambda x: x['score'])[0]['name']
            cv2.putText(img, categoryName, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)

        if 'tags' in result:
            primary_tags = []
            for item in result['tags']: primary_tags.append(item['name'])
            primary_tags = "primary tags: " + str(primary_tags)
            cv2.putText(img, primary_tags, (30, 120), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)

        if 'faces' in result:
            for item in result['faces']:
                desc = item['gender'] + ", " + str(item['age'])
                left = item['faceRectangle']['left']
                top = item['faceRectangle']['top']
                height = item['faceRectangle']['height']
                width = item['faceRectangle']['width']
                cv2.rectangle(img, (left, top), (left+width, top+height), (255, 0, 0), 1)
                cv2.putText(img, desc, (left, top+height), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)

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

            for emo in face['scores']:
                if float(face['scores'][emo]) > 0.1:
                    emotions += emo + ' '

            cv2.putText(img, emotions, (left, top), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), fontThickness)

        return img

    def _connect_ms_emotion_api(self, data):
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.emotion_api_key,
        }

        params = urllib.parse.urlencode({
        })

        body = data

        try:
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
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

    def _process_frame(self, frame, cv2):
        cv2.imwrite('temp.png', frame)

        pathToFileInDisk = r'E:\Projects\ms-cognitive-api\surveillance\temp.png'.replace('\\', '/')
        with open(pathToFileInDisk, 'rb') as f:
            data = f.read()

        result_vision = self._connect_ms_vision_api(data)
        print(strftime("%a, %d %b %Y %H:%M:%S +1030", gmtime()), result_vision)

        result_emotions = None
        if self.enable_emotions:
            result_emotions = self._connect_ms_emotion_api(data)
            print(strftime("%a, %d %b %Y %H:%M:%S +1030", gmtime()), result_emotions)


        if result_vision is not None:
            data8uint = np.fromstring(data, np.uint8)  # Convert string to an unsigned int array
            img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

            img = self._render_result_on_image(result_vision, img, result_emotions)

            cv2.imshow(self.analyze_frame, img)

    def is_running(self):
        return self.started

    def toggle(self):
        self.started = not self.started

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()


def getAnalyzer():
    return WebCamAnalyzer()