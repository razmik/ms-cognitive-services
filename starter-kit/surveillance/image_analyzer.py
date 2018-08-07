from __future__ import print_function
import http.client, urllib.request, urllib.parse, urllib.error
import requests
import cv2
import json
import numpy as np
import sys


class ImageAnalyzer:

    def __init__(self, api_key):
        self.api_key = api_key
        return

    def ia_test(self):
        print("ImageAnalyzer")

    def analyze_url(self, data):
        self._connect_ms_vision_api_url(data)

    def analyze_file(self, filename):
        self._connect_ms_vision_api_file(filename)

    def renderResultOnImage(self, result, img):

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

        return img


    def _connect_ms_vision_api_url(self, url):

        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({
            'visualFeatures': 'Color,Categories,Tags,Description,Faces,ImageType,Adult',
            'language': 'en',
        })

        urlImage = url
        body = "{'url':'"+urlImage+"'}"

        try:
            conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
            conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
            response = conn.getresponse()
            result = json.loads(response.read().decode("utf-8"))
            print(result)
            conn.close()

            if result is not None:
                # Load the original image, fetched from the URL
                arr = np.asarray(bytearray(requests.get(urlImage).content), dtype=np.uint8)
                img = cv2.cvtColor(cv2.imdecode(arr, -1), cv2.COLOR_BGR2RGB)

                cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                img = self.renderResultOnImage(result, img)
                cv2.resizeWindow('image', 600, 600)

                cv2.imshow("image", img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def _connect_ms_vision_api_file(self, filepath):
        headers = {
            # Request headers.
            'Content-Type': 'application/octet-stream',

            # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
            'Ocp-Apim-Subscription-Key': '52b05c830201461da09688253629ecd3',
        }

        params = urllib.parse.urlencode({
            # Request parameters. All of them are optional.
            'visualFeatures': 'Color,Categories,Tags,Description,Faces,ImageType,Adult',
            'language': 'en',
        })

        pathToFileInDisk = filepath
        with open(pathToFileInDisk, 'rb') as f:
            data = f.read()
        body = data

        try:
            conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
            conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
            response = conn.getresponse()
            result = json.loads(response.read().decode("utf-8"))
            print(result)
            conn.close()

            if result is not None:
                # Load the original image, fetched from the URL
                data8uint = np.fromstring(data, np.uint8)  # Convert string to an unsigned int array
                img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

                cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                img = self.renderResultOnImage(result, img)
                cv2.resizeWindow('image', 600, 400)

                cv2.imshow("image", img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))


def getAnalyzer(key):
    return ImageAnalyzer(key)

a = ImageAnalyzer('52b05c830201461da09688253629ecd3')
a.analyze_url('https://i.ytimg.com/vi/FKa0h1f8JR8/maxresdefault.jpg')

# r'E:\Projects\ms-cognitive-api\vision\tv4.PNG'