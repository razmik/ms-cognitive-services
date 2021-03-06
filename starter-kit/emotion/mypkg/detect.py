import http.client, urllib.request, urllib.parse, urllib.error, base64, sys


def run():
    return ("I am running")

headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'e9b3a0491efc46a8b29a3c48ab098f07',
}

params = urllib.parse.urlencode({
})

# Replace the example URL below with the URL of the image you want to analyze.
body = "{ 'url': 'http://www.menshealth.com/sites/menshealth.com/files/2014/03/angry-man.jpg' }"

try:
    # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
    #   URL below with "westcentralus".
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print(e.args)