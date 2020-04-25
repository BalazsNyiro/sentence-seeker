# -*- coding: utf-8 -*-
import util, os, pathlib, sys
from util import print_dev

def docs_load_all_to_be_ready_to_seeking(Prg):
    DocumentsAvailable = docs_collect_filenames_from_working_dir(Prg)

    if not DocumentsAvailable:
        print("Load sample docs into 'documents' because it's empty")
        DirSamplesInDocuments = os.path.join(Prg["DirDocuments"], "text_samples")
        util.dir_create_if_necessary(Prg, DirSamplesInDocuments)

        # sample texts are gzipped
        for FileName in util.files_collect_from_dir(Prg["DirTextSamples"]):

            BaseName = os.path.basename(FileName).replace(".gz", "")

            print(f"Sample doc duplication... {BaseName}   {FileName}")
            ReadSuccess, TextContent = util.file_read_all(Prg, FileName, Gzipped=True)
            print("TextContent type:", type(TextContent))
            print("len content:", len(TextContent))
            FileNameSaved = os.path.join(DirSamplesInDocuments, BaseName)
            print(f"FileNameSaved: {FileNameSaved}")
            util.file_write(Prg, Fname=FileNameSaved, Content=TextContent)

        DocumentsAvailable = docs_collect_filenames_from_working_dir(Prg)

    for Doc in DocumentsAvailable:
        print_dev(Prg, "available>>", Doc)
        # indexed file created?
        #


# Tested
def docs_collect_filenames_from_working_dir(Prg):
    DirDocuments = Prg["DirDocuments"]
    Files = util.files_collect_from_dir(DirDocuments)

    Docs = dict()
    ExtensionsInFuture = {".pdf":0, ".html":0, ".htm":0}

    for File in Files:
        BaseName = os.path.basename(File)
        Extension = pathlib.Path(File).suffix

        if Extension == ".txt":
            print("in documents dir - processed: ", BaseName)

            # this document object describe infos about the document
            # for example the version of index algorithm
            DocumentObj = {""}
            Docs[BaseName] = DocumentObj

        elif Extension in ExtensionsInFuture:
            print("in documents dir - this file type will be processed in the future:", BaseName)

        else:
            print_dev(Prg, "in documents dir - not processed file type:", BaseName)

    return Docs


