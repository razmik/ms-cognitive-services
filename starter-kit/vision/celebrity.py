from __future__ import print_function
import http.client, urllib.request, urllib.parse, urllib.error, base64
import time
import requests
import cv2
import operator
import numpy as np
import matplotlib.pyplot as plt

"""
https://docs.microsoft.com/en-gb/azure/cognitive-services/computer-vision/quickstarts/python
"""

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
urlImage = 'https://oxfordportal.blob.core.windows.net/vision/Analysis/3.jpg'
body = "{'url':'"+urlImage+"'}"

try:
    # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))