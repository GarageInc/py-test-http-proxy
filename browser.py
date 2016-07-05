#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer
import webbrowser

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/site/index.html'
        else:
            self.path = '/site/' + self.path

        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

def Run():    
    Handler = MyRequestHandler
    
    PORT=3018
    server = SocketServer.TCPServer(('', PORT), Handler)
    
    webbrowser.open(url="http://127.0.0.1:{0}/".format(PORT), new=1)
    
    server.serve_forever()
