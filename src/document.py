# -*- coding: utf-8 -*-
import util, os, pathlib, stats
from util import print_dev

# TODO: TEST it
def docs_copy_samples_into_dir_if_necessary(Prg):
    DocumentsAvailable = document_objects_collect_from_working_dir(Prg)
    if not DocumentsAvailable:
        DirTarget = os.path.join(Prg["DirDocuments"], "text_samples")
        docs_copy_samples_into_dir(Prg, DirTarget)

# Tested
def docs_copy_samples_into_dir(Prg, DirTarget):
    util.dir_create_if_necessary(Prg, DirTarget)

    # sample texts are gzipped
    for FileName in util.files_collect_from_dir(Prg["DirTextSamples"]):

        BaseName = os.path.basename(FileName).replace(".gz", "")
        print(f"Sample doc duplication... {BaseName}   {FileName}")
        ReadSuccess, TextContent = util.file_read_all(Prg, FileName, Gzipped=True)
        FileNameSaved = os.path.join(DirTarget, BaseName)
        # if a previous file exists with same name, it overwrites
        util.file_write(Prg, Fname=FileNameSaved, Content=TextContent)

# Tested
def document_objects_collect_from_working_dir(Prg, VersionSeeking="version_not_set"):
    DirDocuments = Prg["DirDocuments"]
    Files = util.files_collect_from_dir(DirDocuments)

    DocumentObjects = dict()
    ExtensionsInFuture = {".pdf":0, ".html":0, ".htm":0}

    for File in Files:
        BaseName = os.path.basename(File)
        Extension = pathlib.Path(File).suffix

        if Extension == ".txt":
            print("in documents dir - processed: ", BaseName)

            # this document object describe infos about the document
            # for example the version of index algorithm
            DocumentObj = { "PathAbs": File,
                            "FileSentences": f"{File}_sentence_separator_{VersionSeeking}",
                            "FileWordIndex": f"{File}_wordindex_{VersionSeeking}"
                          }
            DocumentObjects[BaseName] = DocumentObj  # we store the documents based on their basename

        elif Extension in ExtensionsInFuture:
            print("in documents dir - this file type will be processed in the future:", BaseName)

        else:
            print_dev(Prg, "in documents dir - not processed file type:", BaseName)

    return DocumentObjects


