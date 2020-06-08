# -*- coding: utf-8 -*-
import time, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import seeker

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        # default reply
        Reply = {'time': int(time.time()) }

        o = urllib.parse.urlparse(self.path)
        print("\n=== query ===")
        print(o.query)
        print("\n=== pars ====")
        QueryParams = urllib.parse.parse_qs(o.query)
        print(QueryParams)
        if "words" in QueryParams:
            _WordsWanted, MatchNums__ResultInfo, ResultsTotalNum = seeker.seek(self.Prg, QueryParams["words"][0])
            Reply = MatchNums__ResultInfo

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(Reply).encode('UTF-8'))

