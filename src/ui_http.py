# -*- coding: utf-8 -*-
import time, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        o = urllib.parse.urlparse(self.path)
        print(o.query)
        print(urllib.parse.parse_qs(o.query))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'time': int(time.time()) }).encode('UTF-8'))

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
