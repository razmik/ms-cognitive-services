from __future__ import print_function
import http.client, urllib.request, urllib.parse, urllib.error, base64
import time
import requests
import cv2
import operator
import json
import numpy as np
import matplotlib.pyplot as plt
import sys

"""
https://docs.microsoft.com/en-gb/azure/cognitive-services/computer-vision/quickstarts/python
"""

def renderResultOnImage(result, img):
    """Display the obtained results onto the input image"""

    R = int(result['color']['accentColor'][:2], 16)
    G = int(result['color']['accentColor'][2:4], 16)
    B = int(result['color']['accentColor'][4:], 16)

    cv2.rectangle(img, (0, 0), (img.shape[1], img.shape[0]), color=(R, G, B), thickness=25)

    if 'description' in result:
        caption = str(result['description']['captions'][0]['text'])
        cv2.putText(img, caption, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        secondary_tags = "secondary tags: " + str(result['description']['tags'])
        cv2.putText(img, secondary_tags, (30, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    if 'categories' in result:
        categoryName = sorted(result['categories'], key=lambda x: x['score'])[0]['name']
        cv2.putText(img, categoryName, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    if 'tags' in result:
        primary_tags = []
        for item in result['tags']: primary_tags.append(item['name'])
        primary_tags = "primary tags: " + str(primary_tags)
        cv2.putText(img, primary_tags, (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    return img

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
body = "{'url':'"+urlImage+"'}"

pathToFileInDisk = r'E:\Projects\ms-cognitive-api\vision\tv4.PNG'
with open( pathToFileInDisk, 'rb' ) as f:
    data = f.read()
body = data

# print(body)

# sys.exit(0)

try:
    # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    result = json.loads(response.read().decode("utf-8"))
    print(result)
    conn.close()
    # sys.exit(0)
    if result is not None:
        # Load the original image, fetched from the URL
        data8uint = np.fromstring(data, np.uint8)  # Convert string to an unsigned int array
        img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        img = renderResultOnImage(result, img)
        cv2.resizeWindow('image', 600, 400)

        cv2.imshow("image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))