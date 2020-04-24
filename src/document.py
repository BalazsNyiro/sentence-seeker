# -*- coding: utf-8 -*-
import util, os, pathlib

def collect_docs_from_working_dir(Prg):
    DirDocuments = Prg["DirDocuments"]
    Files = util.files_collect_from_dir(DirDocuments)

    Docs = dict()
    ExtensionsInFuture = {".pdf":0, ".html":0, ".htm":0}

    for File in Files:
        BaseName = os.path.basename(File)
        Extension = pathlib.Path(File).suffix

        if Extension == ".txt":
            print("in documents dir: ", BaseName)

            # this document object describe infos about the document
            # for example the version of index algorithm
            DocumentObj = {""}
            Docs[BaseName] = DocumentObj

        elif Extension in ExtensionsInFuture:
            print("in documents dir - this file type will be processed in the future:", BaseName)

        else:
            pass
            print("in documents dir - not processed file type:", BaseName)

    return Docs


