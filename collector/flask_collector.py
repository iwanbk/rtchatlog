import datetime
import sys
import os, errno

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, escape
from flaskext.xmlrpc import XMLRPCHandler, Fault

import messager

app = Flask(__name__)
app.config.from_object(__name__)

handler = XMLRPCHandler('api')
handler.connect(app, '/xr')

archive_path = "./raw_archive/"

@app.route("/")
def index():
    return "hai"
@handler.register
def hello(name):
    if not name:
        raise Fault("unknown_recipient", "I need someone to greet!")
    return "Hello, %s!" % name

def get_real_nick(long_nick):
    sep = long_nick.find("!")
    nick = long_nick[:sep]
    return nick

def create_dir(dir):
    try:
        os.makedirs(dir)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
        
def save_chan_msg_to_disk(server, chan, nick, msg):
    print "save to disk"
    #open file
    #get date
    tgl = datetime.date.today()
    
    #get time
    tgl = datetime.datetime.now()
    str_wkt = str(tgl.hour) + ":" + str(tgl.minute) + ":" + str(tgl.second)
    
    to_write = "[" + str_wkt + "]" + nick + ":" + msg
    save_chan = chan[1:]
    full_dir = archive_path + server + "/" + save_chan + "/" + str(tgl.year) + "/" + str(tgl.month)
    full_path = full_dir + "/" + str(tgl.day) + ".txt"
  
    create_dir(full_dir)
  
    f = open(full_path, "a+")
    f.write(to_write)
    f.write("\n")
    f.close()
    
    messager.post_message(server, chan, to_write)
    
@handler.register
def add_chan_msg(server, chan, long_nick, msg):
    nick = get_real_nick(long_nick)
    print "------- add_chan_msg------"
    print "server = ", server
    print "chan = ", chan
    print "nick = ", nick
    print "msg = ", msg
    
    save_chan_msg_to_disk(server, chan, nick, msg)
    
    return True

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(port = port, debug = True)