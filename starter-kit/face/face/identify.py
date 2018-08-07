import http.client, urllib.request, urllib.parse, urllib.error, base64, sys

headers = {
    # Request headers.
    'Content-Type': 'application/json',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '89129423e78046f6b06a5cab5666c277',
}

# Replace 'examplegroupid' with an ID you haven't used for creating a group before.
# The valid characters for the ID include numbers, English letters in lower case, '-' and '_'.
# The maximum length of the ID is 64.
personGroupId = 'family_group'

# The userData field is optional. The size limit for it is 16KB.
body = "{ 'personGroupId':'family_group', " \
       "'faceIds':['8c8a4d12-8fc4-447e-a22d-a6d68b1e1fbd']," \
       "'maxNumOfCandidatesReturned':2," \
       "'confidenceThreshold': 0.5 }"

try:
    # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

    request = "/face/v1.0/identify"
    conn.request("POST", request, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)

    conn.close()
except Exception as e:
    print(e.args)