#!/usr/bin/env python
# coding: utf-8

import TwistedTwitterStream
from twisted.internet import reactor

class consumer(TwistedTwitterStream.TweetReceiver):
    def connectionMade(self):
        print "connected..."

    def connectionFailed(self, why):
        print "cannot connect:", why
        reactor.stop()

    def tweetReceived(self, tweet):
        print "new tweet:", repr(tweet)
        
        # you may call self.disconnect() anytime to
        # permanently disconnect from the Twitter Stream

if __name__ == "__main__":
    TwistedTwitterStream.filter("username", "password", consumer(),
            track=["football", "soccer", "world cup", "palmeiras"])
    reactor.run()
