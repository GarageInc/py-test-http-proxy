#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer
import webbrowser

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/site/index.html'

        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

PORT=3003
Handler = MyRequestHandler
server = SocketServer.TCPServer(('', PORT), Handler)

print("loading...")
#server.serve_forever()
print("end")


new = 2 # open in a new tab, if possible
url="http://127.0.0.1:{0}/".format(PORT)
webbrowser.open(url=url,new=new)

server.serve_forever()
