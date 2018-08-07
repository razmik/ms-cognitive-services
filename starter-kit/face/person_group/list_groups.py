import http.client, urllib.request, urllib.parse, urllib.error, base64, sys

headers = {
    # Request headers.
    'Content-Type': 'application/json',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '89129423e78046f6b06a5cab5666c277',
}

body = "{ }"

try:
    # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

    request = "/face/v1.0/persongroups"
    conn.request("GET", request, body, headers)
    response = conn.getresponse()

    data = response.read()
    print(data)

    conn.close()
except Exception as e:
    print(e.args)
