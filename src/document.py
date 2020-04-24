# -*- coding: utf-8 -*-
import util, os

def collect_docs_from_working_dir(Prg):
    DirDocuments = Prg["DirDocuments"]
    Files = util.files_collect_from_dir(DirDocuments)

    Docs = dict()
    for File in Files:
        BaseName = os.path.basename(File)

        # this document object describe infos about the document
        # for example the version of index algorithm
        DocumentObj = {""}
        Docs[BaseName] = DocumentObj

    return Docs


