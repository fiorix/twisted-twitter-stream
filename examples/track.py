#!/usr/bin/env python
# coding: utf-8

import TwistedTwitterStream
from twisted.internet import reactor

def consumer(status):
    print status

def success(status):
    print "ready!"

def failure(why):
    status, message = why.getErrorMessage()
    print "HTTP error %d: %s" % (status, message)
    reactor.stop()

if __name__ == "__main__":
    d = TwistedTwitterStream.filter("username", "password", consumer,
            track=["football", "soccer", "world cup", "palmeiras"])
    d.addCallbacks(success, failure)
    reactor.run()
