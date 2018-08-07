import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

headers = {
    # Request headers.
    'Content-Type': 'application/json',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '52b05c830201461da09688253629ecd3',
}

params = urllib.parse.urlencode({
    # Request parameters. The language setting "unk" means automatically detect the language.
    'language': 'unk',
    'detectOrientation ': 'true',
})

# Replace the three dots below with the URL of a JPEG image containing text.
body = "{'url':'https://i.stack.imgur.com/WiDpa.jpg'}"

try:
    # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    data = json.loads(data.decode("utf-8"))
    # print(data['regions'])

    for word_box in data['regions'][0]['lines']:
        for words in word_box['words']:
            print(words['text'], end=" ")


    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))