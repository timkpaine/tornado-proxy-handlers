import sys
import logging
import tornado.web
import tornado.ioloop
from .handlers import ProxyHandler, ProxyWSHandler


def main(proxy_url):
    app = tornado.web.Application()
    handlers = [
        (r"/(.*)", ProxyHandler, {'proxy_url': proxy_url}),
        (r"/(.*)", ProxyWSHandler, {'proxy_url': proxy_url})
    ]
    app.add_handlers('.*$', handlers)
    logging.critical('Dashboard listening on port %s.' % 8080)
    app.listen(8080)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        logging.critical('Shutting down...')


if __name__ == '__main__':
    main(sys.argv[1])
