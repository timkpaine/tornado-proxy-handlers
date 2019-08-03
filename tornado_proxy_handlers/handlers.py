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
    def initialize(self, proxy_url='/', **kwargs):
        super(ProxyHandler, self).initialize(**kwargs)
        self.proxy_url = proxy_url

    @tornado.gen.coroutine
    def get(self, url=None):
        '''Get the login page'''
        url = url or self.proxy_url
        if url is None:
            if self.request.uri.startswith('/'):
                url = self.request.uri[1:]
            else:
                url = self.request.uri

        req = tornado.httpclient.HTTPRequest(url)
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield client.fetch(req, raise_error=False)

        # websocket upgrade
        if response.code == 599:
            self.set_status(200)  # switching protocols
            return

        self.set_status(response.code)
        if response.code != 200:
            self.finish()
        else:
            if response.body:
                for header in response.headers:
                    if header.lower() == 'content-length':
                        self.set_header(header, str(max(len(response.body), int(response.headers.get(header)))))
                    else:
                        self.set_header(header, response.headers.get(header))

            self.write(response.body)
            self.finish()


class ProxyWSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, proxy_url='/', **kwargs):
        super(ProxyWSHandler, self).initialize(**kwargs)
        self.proxy_url = proxy_url
        self.ws = None
        self.closed = True

    @tornado.gen.coroutine
    def open(self, url=None):
        self.closed = False
        url = url or self.proxy_url
        if url is None:
            if self.request.uri.startswith('/'):
                url = self.request.uri[1:]
            else:
                url = self.request.uri

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
