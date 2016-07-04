#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'habrahabr.ru'
	print(SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self))
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler
server = SocketServer.TCPServer(('', 3000), Handler)

server.serve_forever()
