package main

import (
	"fmt"
	irc "github.com/reynir/Go-IRC-Client-Library"
	"log"
	"net/http"
	"net/url"
	"time"
)

func main() {
	ircCon := irc.IRC("nick", "user")
	ircCon.Password = "password"

	err := ircCon.Connect("irc.freenode.net:6667")
	if err != nil {
		log.Fatal("can't connect:", err)
	}

	ircCon.AddCallback("001", func(e *irc.Event) { ircCon.Join("#rtchatlog") })
	ircCon.AddCallback("001", func(e *irc.Event) { ircCon.Join("#gevent") })
	ircCon.AddCallback("001", func(e *irc.Event) { ircCon.Join("#django") })
	ircCon.AddCallback("001", func(e *irc.Event) { ircCon.Join("#pocoo") })
	ircCon.AddCallback("001", func(e *irc.Event) { ircCon.Join("#python") })
	ircCon.AddCallback("001", func(e *irc.Event) { ircCon.Join("#go-nuts") })
	ircCon.AddCallback("PRIVMSG", func(e *irc.Event) {
		channel := e.Arguments[0]
		fmt.Println("[", channel, "]", "[", e.Nick, "]:", e.Message)
		go sendLog("irc.freenode.net", channel, e.Nick, e.Message)
	})
	ircCon.Loop()
}

func buildMessage(nick, message string) string {
	now := time.Now()
	m := "[" + now.Format(time.RFC822Z) + "]["+nick+"]"+message
	return m
}

func sendLog(server, channel, nick, message string) {
	postUrl := "http://localhost:8080/new_msg_chan/" + server + "/" + channel[1:] + "/"
	m := buildMessage(nick, message)
	resp, err := http.PostForm(postUrl, url.Values{"key": {"Value"}, "body": {m}})
	if err != nil {
		log.Fatal("can't send log:", err)
	}
	defer resp.Body.Close()
}
