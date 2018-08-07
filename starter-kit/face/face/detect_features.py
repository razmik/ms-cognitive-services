import http.client, urllib.request, urllib.parse, urllib.error, base64

"""
To read: https://social.msdn.microsoft.com/Forums/en-US/e5d72a95-3a44-48bb-b5c9-b261e811d4d9/using-face-api-with-python-and-local-image-files?forum=mlapi
"""

headers = {
    # Request headers
    'Content-Type': 'application/json',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '89129423e78046f6b06a5cab5666c277',
}

params = urllib.parse.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender',
})

# Replace the three dots below with the URL of a JPEG image of a celebrity.
body = "{'url':'http://all4desktop.com/data_images/original/4242435-face.jpg'}"
body_rashmika = "{'url':'https://sites.google.com/a/cse.mrt.ac.lk/dmcse/_/rsrc/1373266647925/members/rashmika/Rashmika.png'}"
body_damminda = "{'url':'http://www.latrobe.edu.au/staff-profiles/data/images/photos/dalahakoon.jpg'}"
body_daswin = "{'url':'http://analytics.science.latrobe.edu.au/people/~daswin/id.jpg'}"

try:
    # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body_daswin, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))