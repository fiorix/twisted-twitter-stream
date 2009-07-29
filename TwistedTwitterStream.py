# coding: utf-8
#
# Copyright 2009 Alexandre Fiori
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

__author__ = "Alexandre Fiori"
__version__ = "0.0.1"

"""Twisted client library for the Twitter Streaming API:
http://apiwiki.twitter.com/Streaming-API-Documentation"""

import base64, urllib
from twisted.protocols import basic
from twisted.internet import defer, reactor, protocol

try:
    import simplejson as _json
except ImportError:
    try:
        import json as _json
    except ImportError:
        raise RuntimeError("A JSON parser is required, e.g., simplejson at "
                           "http://pypi.python.org/pypi/simplejson/")


class _TwitterStreamProtocol(basic.LineReceiver):
    delimiter = "\r\n"
    def __init__(self):
        self.in_header = True
        self.header_data = []
        self.status_data = ""
        self.status_size = None

    def connectionMade(self):
        self.transport.write(self.factory.header)

    def lineReceived(self, line):
        while self.in_header:
            if line:
                self.header_data.append(line)
            else:
                http, status, message = self.header_data[0].split(" ", 2)
                status = int(status)
                if status == 200:
                    if getattr(self.factory, "deferred"):
                        self.factory.deferred.callback(status)
                else:
                    self.factory.continueTrying = 0
                    self.transport.loseConnection()
                    if getattr(self.factory, "deferred"):
                        self.factory.deferred.errback(RuntimeError(status, message))

                del self.factory.deferred
                self.in_header = False
            break
        else:
            try:
                self.status_size = int(line, 16)
                self.setRawMode()
            except:
                pass

    def rawDataReceived(self, data):
        if self.status_size is not None:
            data, extra = data[:self.status_size], data[self.status_size:]
            self.status_size -= len(data)
        else:
            extra = ""

        self.status_data += data
        if self.status_size == 0:
            if callable(self.factory.consumer):
                try:
                    # ignore newline keep-alive
                    status = _json.loads(self.status_data)
                except:
                    pass
                else:
                    rv = self.factory.consumer(status)
                    if rv is False:
                        self.factory.continueTrying = 0
                        self.transport.loseConnection()
            self.status_data = ""
            self.status_size = None
            self.setLineMode(extra)


class _TwitterStreamFactory(protocol.ReconnectingClientFactory):
    protocol = _TwitterStreamProtocol

    def __init__(self, consumer):
        self.consumer = consumer
        self.deferred = defer.Deferred()

    def make_header(self, username, password, method, uri, postdata=""):
        auth = base64.encodestring("%s:%s" % (username, password)).strip()
        header = [
            "%s %s HTTP/1.1" % (method, uri),
            "Authorization: Basic %s" % auth,
            "User-Agent: twisted twitter radio",
            "Host: stream.twitter.com",
        ]

        if method == "GET":
            self.header = "\r\n".join(header) + "\r\n\r\n"

        elif method == "POST":
            header += [
                "Content-Type: application/x-www-form-urlencoded",
                "Content-Length: %d" % len(postdata),
            ]
            self.header = "\r\n".join(header) + "\r\n\r\n" + postdata

 
def firehose(username, password, consumer):
    tw = _TwitterStreamFactory(consumer)
    tw.make_header(username, password, "GET", "/1/statuses/firehose.json")
    reactor.connectTCP("stream.twitter.com", 80, tw)
    return tw.deferred

def retweet(username, password, consumer):
    tw = _TwitterStreamFactory(consumer)
    tw.make_header(username, password, "GET", "/1/statuses/retweet.json")
    reactor.connectTCP("stream.twitter.com", 80, tw)
    return tw.deferred

def sample(username, password, consumer):
    tw = _TwitterStreamFactory(consumer)
    tw.make_header(username, password, "GET", "/1/statuses/sample.json")
    reactor.connectTCP("stream.twitter.com", 80, tw)
    return tw.deferred

def filter(username, password, consumer, count=0, delimited=0, track=[], follow=[]):
    qs = []
    if count:
        qs.append("count=%s" % urllib.quote(count))
    if delimited:
        qs.append("delimited=%d" % delimited)
    if follow:
        qs.append("follow=%s" % ",".join(follow))
    if track:
        qs.append("track=%s" % ",".join([urllib.quote(s) for s in track]))

    if not (track or follow):
        raise RuntimeError("At least one parameter is required: track or follow")

    tw = _TwitterStreamFactory(consumer)
    tw.make_header(username, password, "POST", "/1/statuses/filter.json", "&".join(qs))
    reactor.connectTCP("stream.twitter.com", 80, tw)
    return tw.deferred
