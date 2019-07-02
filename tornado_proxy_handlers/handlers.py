import os
import os.path
import tornado
import tornado.gen
import tornado.web
import tornado.websocket
import tornado.httpclient

ap = os.path.abspath
join = os.path.join


class ProxyHandler(tornado.web.RequestHandler):
    def initialize(self, proxy_path='', **kwargs):
        super(ProxyHandler, self).initialize(**kwargs)
        self.proxy_path = proxy_path

    @tornado.gen.coroutine
    def get(self, url=None):
        '''Get the login page'''
        req = tornado.httpclient.HTTPRequest(url)
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield client.fetch(req, raise_error=False)

        # websocket upgrade
        if response.code == 599:
            self.set_status(200)  # switching protocols
            return

        self.set_status(response.code)
        if response.body:
            for header in response.headers:
                self.set_header(header, response.headers.get(header))
            self.write(response.body)
        self.finish()


class ProxyWSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, proxy_path='', **kwargs):
        super(ProxyWSHandler, self).initialize(**kwargs)
        self.proxy_path = proxy_path
        self.ws = None
        self.closed = True

    @tornado.gen.coroutine
    def open(self, url=None):
        self.closed = False

        def write(msg):
            if self.closed:
                if self.ws:
                    self.ws.close()
                    self.ws = None
            else:
                if self.ws:
                    self.write_message(msg, binary=isinstance(msg, bytes))
        self.ws = yield tornado.websocket.websocket_connect(url,
                                                            on_message_callback=write)

    def on_message(self, message):
        if self.ws:
            self.ws.write_message(message)

    def on_close(self):
        if self.ws:
            self.ws.close()
            self.ws = None
            self.closed = True
