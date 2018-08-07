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
# personId = "a5be42cd-e3e1-41c7-81cc-580f01541a0a" #Rashmika
# personId = "36899c49-2d56-40b0-a4f4-95953ed6de8e" #Achini
personId = "0de83117-7bef-4380-be62-1da38d829989" #Tharindu

# The userData field is optional. The size limit for it is 16KB.
body = "{ 'url':'https://media.licdn.com/mpr/mpr/shrinknp_200_200/AAEAAQAAAAAAAAYdAAAAJDcxY2Q0MzFhLWI2YTYtNDQyZC1hMjJiLTllZDJjMmM3MjU5Nw.jpg' }"

try:
    # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

    request = "/face/v1.0/persongroups/" + personGroupId + "/persons/" + personId + "/persistedFaces"
    conn.request("POST", request, body, headers)
    response = conn.getresponse()

    # 'OK' indicates success. 'Conflict' means a group with this ID already exists.
    # If you get 'Conflict', change the value of personGroupId above and try again.
    # If you get 'Access Denied', verify the validity of the subscription key above and try again.
    print(response.reason)

    conn.close()
except Exception as e:
    print(e.args)
