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

    def initialize(self, dashboard=None, proxy_path='', **kwargs):
        self.dashboard = dashboard
        self.proxy_path = proxy_path
        super(ProxyHandler, self).initialize(**kwargs)

    @tornado.gen.coroutine
    def get(self, *args):
        '''Get the login page'''
        path = self.request.uri.replace(self.proxy_path, '', 1)
        splits = path.split('/')
        id = splits[0]

        if id not in self.dashboard.subprocesses:
            return

        p, nbdir, nbpath, port = self.dashboard.subprocesses[id]

        req = tornado.httpclient.HTTPRequest('http://localhost:{port}/{url}'.format(port=port, url='/'.join(splits[1:])))
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield client.fetch(req, raise_error=False)
        self.set_status(response.code)
        if response.body:
            for header in response.headers:
                self.set_header(header, response.headers.get(header))
            self.write(response.body)
        self.finish()


class ProxyWSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, dashboard=None, proxy_path='', **kwargs):
        super(ProxyWSHandler, self).initialize(**kwargs)
        self.dashboard = dashboard
        self.proxy_path = proxy_path
        self.ws = None
        self.closed = True

    @tornado.gen.coroutine
    def open(self, *args):
        path = self.request.uri.replace(self.proxy_path, '', 1)
        splits = path.split('/')
        id = splits[0]
        if id not in self.dashboard.subprocesses:
            return

        p, nbdir, nbpath, port = self.dashboard.subprocesses[id]
        url = '/'.join(splits[1:])
        self.closed = False

        def write(msg):
            if self.closed:
                if self.ws:
                    self.ws.close()
                    self.ws = None
            else:
                if self.ws:
                    self.write_message(msg, binary=isinstance(msg, bytes))
        self.ws = yield tornado.websocket.websocket_connect('ws://localhost:{port}/{url}'.format(port=port, url=url),
                                                            on_message_callback=write)

    def on_message(self, message):
        if self.ws:
            self.ws.write_message(message)

    def on_close(self):
        if self.ws:
            self.ws.close()
            self.ws = None
            self.closed = True
