import sys

import requests

URL = "http://localhost:8080/new/"

def post_message(server, chan, body):
    payload = {"body":body}
    post_url = "http://localhost:8080/new_msg_chan/"+server+"/"+chan[1:]+"/"
    r = requests.post(post_url, data = payload)
    print r.text
    
if __name__ == '__main__':
    msg = sys.argv[1]
    
    payload = {"server":"irc.localhost", "chan":"pribadi",
               "body":msg}
    
    #to front
    post_message(payload)