import time
import xmlrpclib

from oyoyo.client import IRCClient
from oyoyo.cmdhandler import DefaultCommandHandler, BotCommandHandler
from oyoyo import helpers
import botconf


RPC_SERVER = "http://localhost:5252/xr"
rpc_server = xmlrpclib.ServerProxy(RPC_SERVER)

chan_list = [
    '#rtchatlog',
    '#gevent',
    '#pocoo',
    '#django',
    '#go-nuts',
    "#python",
    "#diesel",
]

def save_log_chat(chan, nick, msg):
    res = rpc_server.add_chan_msg("irc.freenode.net", chan, nick, msg)
    print res

def connect_callback(cli):
    # Identify to nickserv
    print "connected"
    helpers.msg(cli, "NickServ", "IDENTIFY " + botconf.password)
    print "password sent"
    
    for c in chan_list:
        time.sleep(20)
        print "joining channel = ", c
        helpers.join(cli, c)

class MyHandler(DefaultCommandHandler):
    # Handle messages (the PRIVMSG command, note lower case)
    def privmsg(self, nick, chan, msg):
        print "[privmsg][%s]%s:%s" % (chan, nick, msg)
        save_log_chat(chan, nick, msg)

def main():
    cli = IRCClient(MyHandler, host="irc.freenode.net", port=6667, nick=botconf.nick,
                connect_cb=connect_callback)
    
    conn = cli.connect()
    while True:
        conn.next()

if __name__ == '__main__':
    main()
    