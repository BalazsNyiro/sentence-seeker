# -*- coding: utf-8 -*-
import os, urllib.parse, util, seeker, json
from http.server import BaseHTTPRequestHandler

DirHtml = os.path.join("ui", "html")

Cache = {}
TypesAllowed = ["jpg", "png", "html", "js"]
def file_local_read(File, EncodeUtf8=True, Mode="r"):

    # security: you can read only these file types
    if File.split(".")[-1] not in TypesAllowed:
        return ""

    Path = os.path.join(DirHtml, File)

    global Cache
    if Path in Cache:
        return Cache[Path]
    else:
        Content = util.file_read_all_simple(Path, Mode=Mode)
        if EncodeUtf8:
            Content = Content.encode("UTF-8")

        Cache[Path] = Content

        return Content


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        Req = urllib.parse.urlparse(self.path)
        QueryParams = urllib.parse.parse_qs(Req.query)
        if True:
            print("\n=== Request Object ===")
            print(Req)
            print("\n=== Path ===")
            print(self.path)
            print("\n=== query ===")
            print(Req.query)
            print("\n=== pars ====")
            print(QueryParams)
            print("\n=== Wanted Path ====")
            print("\n=== create response ====")

        # # I don't want to reach the file system so limited file acces is defined here
        # User can read only these files
        FilesHtml = {"/": "index.html",
                     "/index.html": "index.html"}
        FilesJs = {"/hilitor.js": "hilitor.js"}
        FilesJpg = {"/img/bg.jpg": "img/bg.jpg", "/favicon.ico": "img/bg.jpg"}

        if Req.path.split("?")[0] == "/seek":
            if "words" in QueryParams:
                _WordsWanted, MatchNums__ResultInfo, ResultsTotalNum = seeker.seek(self.Prg, QueryParams["words"][0])
                Reply = MatchNums__ResultInfo[:self.Prg["LimitDisplayedSampleSentences"]]
                Reply = json.dumps(Reply).encode('UTF-8')

                self.send_response(200)
                self.content_type("text/plain")

        elif Req.path in FilesHtml:
            #if "index.html" in File:

            File = FilesHtml[Req.path]
            Reply = file_local_read(File, EncodeUtf8=False)
            if "index.html" in File:
                Reply = Reply.replace("PLACEHOLDER_DOCUMENT_JSON", self.Prg["FileDocumentsDbContent"])
                Reply = Reply.replace("PLACEHOLDER_HOST", self.Prg["ServerHost"])
                Reply = Reply.replace("PLACEHOLDER_PORT", str(self.Prg["ServerPort"]))

            Reply = Reply.encode("UTF-8")
            self.send_response(200)
            self.content_type("html")

        elif Req.path in FilesJs:
            Reply = file_local_read(FilesJs[Req.path])
            self.send_response(200)
            self.content_type("javascript")

        elif Req.path in FilesJpg:
            Reply = file_local_read(FilesJpg[Req.path], EncodeUtf8=False, Mode="rb")
            self.send_response(200)
            self.content_type("jpg")

        else:
            Reply = "unknown request".encode("UTF-8")
            print("unknown Req.path", Req.path)
            self.send_response(200)
            self.content_type("html")

        self.end_headers()
        self.wfile.write(Reply)

    def content_type(self, Type):
        if Type == "html":
            self.send_header("Content-type", "text/html; charset=UTF-8")
        elif Type == "javascript":
            self.send_header("Content-type", "text/javascript; charset=UTF-8")
        elif Type == "jpg":
            self.send_header("Content-type", "img/jpg")
        elif Type == "json":
            self.send_header('Content-type', 'application/json')
        elif Type == "text":
            self.send_header('Content-type', 'text/plain')

