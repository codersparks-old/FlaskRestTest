
import requests

HOSTNAME = "192.168.0.111"
PORT = 9080
PATH = "/testrest/data"

def store_result(data):
    # We are now going to upload the data to our object store
    store_headers = { "Content-Type": "application/json" }
    url = "http://%s:%s%s" % (HOSTNAME,PORT,PATH)
    store_response = requests.post(url, data=data, auth=("a", "a"), headers=store_headers)

    if store_response.status_code != 201:
        raise ValueError("Response from store upload is not 201 (created) it is: %s" % store_response.status_code)

    store_location = store_response.headers["Location"]

    return store_location