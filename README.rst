====================
TwistedTwitterStream
====================
:Info: See `Twitter Streaming API <http://apiwiki.twitter.com/Streaming-API-Documentation>`_ for more information. See `github <http://github.com/fiorix/twisted-twitter-stream/>`_ for the latest source.
:Author: Alexandre Fiori <fiorix@gmail.com>

About
=====
The ``TwistedTwitterStream`` package provides an event-driven API for receiving `Twitter <http://twitter.com>`_ status updates through the asynchronous `Twitter Streaming API <http://apiwiki.twitter.com/Streaming-API-Documentation>`_.

The following methods are supported:
 - `firehose <http://apiwiki.twitter.com/Streaming-API-Documentation#statuses/firehose>`_
 - `retweet <http://apiwiki.twitter.com/Streaming-API-Documentation#statuses/retweet>`_
 - `sample <http://apiwiki.twitter.com/Streaming-API-Documentation#statuses/sample>`_
 - `filter <http://apiwiki.twitter.com/Streaming-API-Documentation#statuses/filter>`_

Notes
=====
 - A JSON parser is required. Like `json <http://docs.python.org/library/json.html>`_ or `simplejson <http://pypi.python.org/pypi/simplejson/>`_.
 - All methods will automatically reconnect to the server with an exponential back-off. See `t.i.p.ReconnectingClientFactory <http://twistedmatrix.com/documents/8.2.0/api/twisted.internet.protocol.ReconnectingClientFactory.html>`_ for details.
 - All methods must be initialized with a *consumer* function, which will be fired on every status update.
 - In order to stop the stream and disconnect from the server, the *consumer* function must return *False*.
 - The *consumer* function will always receive statuses in the JSON format.
 - No proxy support.

Examples
========
Examples are available in the *examples/* directory.
