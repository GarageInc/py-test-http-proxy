#!/usr/bin/python
    
import SimpleHTTPServer
import SocketServer
    
PORT = 8000
    
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
Handler.extensions_map.update({
    '.webapp': 'application/x-web-app-manifest+json',
});
    
httpd = SocketServer.TCPServer(("127.0.0.1", PORT), Handler)

print("Port: " + str(PORT))    
httpd.serve_forever()
