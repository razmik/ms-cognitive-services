import http.client, urllib.request, urllib.parse, urllib.error, base64
from PIL import Image
import json

headers = {
    # Request headers.
    'Content-Type': 'application/json',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '52b05c830201461da09688253629ecd3',
}

params = urllib.parse.urlencode({
    # Request parameters. The smartCropping flag is optional.
    'width': '150',
    'height': '100',
    'smartCropping': 'true',
})

# Replace the three dots below with the URL of the JPEG image for which you want a thumbnail.
body = "{'url':'https://serendivus.com/wp-content/uploads/st_uploadfont/Sigiriya-SriLanka1-800x600.jpg'}"

try:
    # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/generateThumbnail?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    print(data)

    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))