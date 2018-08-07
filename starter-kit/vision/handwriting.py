import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, time

requestHeaders = {
    # Request headers.
    # Another valid content type is "application/octet-stream".
    'Content-Type': 'application/json',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '52b05c830201461da09688253629ecd3',
}

# Replace the three dots below with the URL of a JPEG image containing text.
body = {'url':'https://i.stack.imgur.com/WiDpa.jpg'}

# NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
#   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
#   URL below with "westus".
serviceUrl = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'

# For printed text, set "handwriting" to false.
params = {'handwriting' : 'true'}


try:
    response = requests.request('post', serviceUrl, json=body, data=None, headers=requestHeaders, params=params)

    if response.status_code == 202:
        print("Success. Await for the response.")
    else:
        print("Bad request.")

    # This is the URI where you can get the text recognition operation result.
    operationLocation = response.headers['Operation-Location']

    # Note: The response may not be immediately available. Handwriting recognition is an
    # async operation that can take a variable amount of time depending on the length
    # of the text you want to recognize. You may need to wait or retry this GET operation.

    time.sleep(10)
    response = requests.request('get', operationLocation, json=None, data=None, headers=requestHeaders, params=None)
    data = response.json()
    print(data)
except Exception as e:
    print(e)