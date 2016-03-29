import requests
import simplejson as json

payload = {"to": "/topics/global",
           "data":
               {"message": "Seizure Alert !!!"}
           }

body = {}
body['data'] = payload

headers = {'Authorization': 'key=AIzaSyCaUM7t_HY69IXWwisTmLCWm_mxxJmHGvw',
           'Content-Type': 'application/json'}


def send():
    print "Sending notification"
    url = "https://android.googleapis.com/gcm/send"

    for x in range(0, 1):
        r = requests.post(url, data=json.dumps(payload), headers=headers)

if __name__ == "__main__":
    send()
