from __future__ import print_function
import http.client, urllib.request, urllib.parse, urllib.error
import numpy as np
import cv2
import json
import os
import _thread


class WebCamAnalyzer:

    def __init__(self):
        self.started = False
        self.temp_file_name = r'temp_'
        self.temp_file_ext = r'.png'
        self.vision_api_key = ''
        self.emotion_api_key = ''
        self.enable_emotions = ''
        self.cap = ''
        self.webcam_frame = "Original View"
        self.analyze_frame = "Analyze View"

    def start_capture(self, frame_rate, vision_api_key, emotion_api_key, enable_emotions, filename):
        self.vision_api_key = vision_api_key
        self.emotion_api_key = emotion_api_key
        self.enable_emotions = enable_emotions

        if filename is None:
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(filename)

        self.webcam_frame = "Original View"
        self.analyze_frame = "Analyze View"
        cv2.namedWindow(self.webcam_frame, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.webcam_frame, 600, 400)
        cv2.namedWindow(self.analyze_frame, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.analyze_frame, 600, 400)
        # cv2.resizeWindow(self.analyze_frame, 1960, 1200)

        iteration = 1
        while True:
            ret, frame = self.cap.read()
            cv2.imshow(self.webcam_frame, frame)

            if iteration % frame_rate == 0:
                self._process_frame(frame, cv2, iteration)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            iteration += 1

        self.cap.release()
        # cv2.destroyAllWindows()

    def _render_result_on_image(self, result, img, result_emotions):

        fontScale = 0.5
        fontThickness = 2
        smallFontThickness = 2
        font_colour = (255, 153, 0)  # (0, 255, 0)

        if 'description' in result:
            caption = str(result['description']['captions'][0]['text'])
            cv2.putText(img, caption, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, fontScale, font_colour, fontThickness)
            secondary_tags = "secondary tags: " + str(result['description']['tags'])
            cv2.putText(img, secondary_tags, (30, 100), cv2.FONT_HERSHEY_SIMPLEX, fontScale, font_colour, smallFontThickness)

        if 'categories' in result:
            categoryName = sorted(result['categories'], key=lambda x: x['score'])[0]['name']
            cv2.putText(img, categoryName, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, fontScale, font_colour, fontThickness)

        if 'tags' in result:
            primary_tags = []
            for item in result['tags']: primary_tags.append(item['name'])
            primary_tags = "primary tags: " + str(primary_tags)
            cv2.putText(img, primary_tags, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, fontScale, font_colour, fontThickness)

        if 'faces' in result:
            for item in result['faces']:
                desc = item['gender'] + ", " + str(item['age'])
                left = item['faceRectangle']['left']
                top = item['faceRectangle']['top']
                height = item['faceRectangle']['height']
                width = item['faceRectangle']['width']
                cv2.rectangle(img, (left, top), (left+width, top+height), (255, 0, 0), 1)
                cv2.putText(img, desc, (left, top+height), cv2.FONT_HERSHEY_SIMPLEX, fontScale, font_colour, fontThickness)

        if result_emotions is not None:
            img = self._render_emotions_on_image(result_emotions, img, fontScale, fontThickness, font_colour)

        return img

    def _render_emotions_on_image(self, result, img, fontScale, fontThickness, font_colour):
        fontScale = 0.5
        fontThickness = 2

        for face in result:
            left = face['faceRectangle']['left']
            top = face['faceRectangle']['top']
            emotions = ""

            for emo_name, emo_score in face['faceAttributes']['emotion'].items():
                if emo_score > 0.1:
                    emotions += emo_name + ':' + str(round(emo_score, 2)) + ' '

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

    def _connect_ms_vision_api_async(self, data, is_emotion, filename_temp):

        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.vision_api_key,
        }
        params = urllib.parse.urlencode({
            'visualFeatures': 'Color,Categories,Tags,Description,Faces,ImageType,Adult',
            'language': 'en',
        })
        body = data

        def send_request(data, is_emotion, filename_temp):
            try:
                conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
                conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
                response = conn.getresponse()
                result_vision = json.loads(response.read().decode("utf-8"))
                conn.close()

                result_emotions = None
                if is_emotion:
                    result_emotions = self._connect_ms_emotion_api(data)

                if result_vision is not None:
                    data8uint = np.fromstring(data, np.uint8)
                    img = cv2.imdecode(data8uint, cv2.IMREAD_COLOR)

                    img = self._render_result_on_image(result_vision, img, result_emotions)

                    cv2.imshow(self.analyze_frame, img)

                if os.path.exists(filename_temp):
                    os.remove(filename_temp)

            except Exception as e:
                print("Error: {0}".format(str(e)))
                return -1

        _thread.start_new_thread(send_request, (data, is_emotion, filename_temp))

    def _process_frame(self, frame, cv2, iteration):
        filename_temp = self.temp_file_name + str(iteration) + self.temp_file_ext
        cv2.imwrite(filename_temp, frame)

        with open(filename_temp, 'rb') as f:
            data = f.read()

        self._connect_ms_vision_api_async(data, self.enable_emotions, filename_temp)


def getAnalyzer():
    return WebCamAnalyzer()