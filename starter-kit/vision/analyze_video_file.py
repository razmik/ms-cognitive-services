from __future__ import print_function
import http.client, urllib.error
import numpy as np
import cv2
import json
import sys


def renderResultOnImage(result, img):
    fontScale = 0.5
    fontThickness = 1
    fontFace = cv2.FONT_HERSHEY_DUPLEX

    if 'description' in result:
        caption = str(result['description']['captions'][0]['text'])
        cv2.putText(img, caption, (30, 40), fontFace, fontScale, (0, 255, 0), fontThickness)
        secondary_tags = "secondary tags: " + str(result['description']['tags'])
        cv2.putText(img, secondary_tags, (30, 160), fontFace, fontScale, (0, 255, 0), fontThickness)

    if 'categories' in result:
        categoryName = sorted(result['categories'], key=lambda x: x['score'])[0]['name']
        cv2.putText(img, categoryName, (30, 80), fontFace, fontScale, (0, 255, 0), fontThickness)

    if 'tags' in result:
        primary_tags = []
        for item in result['tags']: primary_tags.append(item['name'])
        primary_tags = "primary tags: " + str(primary_tags)
        cv2.putText(img, primary_tags, (30, 120), fontFace, fontScale, (0, 255, 0), fontThickness)

    if 'faces' in result:
        for item in result['faces']:
            desc = item['gender'] + ", " + str(item['age'])
            left = item['faceRectangle']['left']
            top = item['faceRectangle']['top']
            height = item['faceRectangle']['height']
            width = item['faceRectangle']['width']
            cv2.rectangle(img, (left, top), (left+width, top+height), (255, 0, 0), 1)
            cv2.putText(img, desc, (left, top+height), fontFace, fontScale, (0, 255, 0), fontThickness)

    return img

def analyze_video(filename):

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

    # Replace the three dots below with the URL of a JPEG image of a celebrity.
    urlImage = ''
    body = ''

    cap = cv2.VideoCapture(filename)

    originalFrame = 'Original Video'
    analysisFrame = 'Analyzed Description'
    cv2.namedWindow(originalFrame, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(originalFrame, 400, 320)
    cv2.namedWindow(analysisFrame, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(analysisFrame, 800, 600)

    iteration = 1
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.imshow(originalFrame, frame)

        # Our operations on the frame come here
        if iteration % 150 == 0:

            cv2.imwrite('temp.png', frame)

            pathToFileInDisk = r'E:\Projects\ms-cognitive-api\vision\temp.png'
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
                    data8uint = np.fromstring(data, np.uint8)  # Convert string to an unsigned int array
                    img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

                    img = renderResultOnImage(result, img)

                    cv2.imshow(analysisFrame, img)

            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        iteration += 1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

analyze_video("C:/Users\pc\Downloads\Movies\Suits S03\Suits S03E03\Suits.S03E03.HDTV.x264-EVOLVE.mp4".replace('\\', '/'))