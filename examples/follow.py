#!/usr/bin/env python
# coding: utf-8
#
# follow is a list of user IDs, not screen names
# use something like this to get user IDs:
#
#    screen_name = "BarackObama"
#    fd = urllib.urlopen("http://twitter.com/users/show/%s.json" % screen_name)
#    doc = simplejson.loads(fd.read())
#    fd.close()
#    print doc.get("id")

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
            follow=["101010", "202020", "303030", "404040"])
    d.addCallbacks(success, failure)
    reactor.run()
