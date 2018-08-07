import http.client, urllib.request, urllib.parse, urllib.error, base64, json

headers = {
    # Request headers.
    'Content-Type': 'application/json',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': '52b05c830201461da09688253629ecd3',
}

params = urllib.parse.urlencode({
    # Request parameters. Use "model": "celebrities" to use the Celebrity model.
    'model': 'landmarks',
})

# The URL of a JEPG image containing text.
# body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Opera_House_and_ferry._Sydney.jpg/220px-Opera_House_and_ferry._Sydney.jpg'}"
body = "{'url':'http://sportsbusinessinsider.com.au/wp-content/uploads/2016/08/La-Trobe-University.jpg'}"

try:
    # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/models/landmarks/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    # 'data' contains the JSON data. The following formats the JSON data for display.
    encoding = response.headers.get_content_charset()
    parsed = json.loads(data.decode(encoding))
    print ("REST Response:")
    print (json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))