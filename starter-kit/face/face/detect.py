import http.client, urllib.request, urllib.parse, urllib.error, base64, sys

headers = {
    # Request headers.
    'Content-Type': 'application/json',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '89129423e78046f6b06a5cab5666c277',
}

# The userData field is optional. The size limit for it is 16KB.
body = "{ 'url':'http://readme.lk/wp-content/uploads/2015/11/11209522_920652687983603_184068499606155678_n-e1447929525958.jpg' }"
# body = "{ 'url':'http://digit.lk/wp-content/uploads/2013/10/999379_683384365004904_1080421778_n.jpg' }" #Group of friends

try:
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

    request = "/face/v1.0/detect?returnFace=True&returnFaceAttributes=age,gender,smile,emotion,accessories"
    conn.request("POST", request, body, headers)

    response = conn.getresponse()
    data = response.read()

    print(data)

    conn.close()
except Exception as e:
    print(e.args)
