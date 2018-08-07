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

    if 'categories' in result:
        categoryName = sorted(result['categories'], key=lambda x: x['score'])[0]['name']
        cv2.putText(img, categoryName, (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

    return img

headers = {
    # Request headers.
    'Content-Type': 'application/json',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '52b05c830201461da09688253629ecd3',
}

params = urllib.parse.urlencode({
    # Request parameters. All of them are optional.
    'visualFeatures': 'Color,Categories',
    'language': 'en',
})

# Replace the three dots below with the URL of a JPEG image of a celebrity.
urlImage = 'http://www.thephotoargus.com/wp-content/uploads/2013/01/mountain-02.jpg'
body = "{'url':'"+urlImage+"'}"

try:
    # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    result = json.loads(response.read().decode("utf-8"))
    conn.close()

    if result is not None:
        # Load the original image, fetched from the URL
        arr = np.asarray(bytearray(requests.get(urlImage).content), dtype=np.uint8)
        img = cv2.cvtColor(cv2.imdecode(arr, -1), cv2.COLOR_BGR2RGB)

        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        img = renderResultOnImage(result, img)
        cv2.resizeWindow('image', 600, 600)

        cv2.imshow("image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # ig, ax = plt.subplots(figsize=(15, 20))
        # ax.imshow(img)



except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))