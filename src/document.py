# -*- coding: utf-8 -*-
import util, os, pathlib, stats
from util import print_dev
import util_json_obj
from os.path import isfile

# Tested
def document_objects_collect_from_working_dir(Prg,
                                              VersionSeeking="version_not_set",
                                              FunSentenceCreate=None,
                                              FunIndexCreate=None,
                                              Verbose=True
                                              ):
    def info(Txt):
        if Verbose: print(Txt)

    Files = util.files_collect_from_dir(Prg["DirDocuments"])

    DocumentObjects = dict()
    ExtensionsInFuture = {".pdf": 0, ".html": 0, ".htm": 0}

    for File in Files:
        BaseName = os.path.basename(File)
        Extension = pathlib.Path(File).suffix.lower()

        if Extension == ".pdf":
            info(f"in documents dir - pdf -> txt conversion: {BaseName}")
            FilePathWithoutExtension = File.rsplit(".", 1)[0]
            FilePathTxt = f"{FilePathWithoutExtension}.txt"
            if not os.path.isfile(FilePathTxt):
                ConversionExecuted = Prg["PdfToTextConvert"](File, FilePathTxt)
                if ConversionExecuted:
                    Extension = ".txt"

        # errors can happen if we convert pdf/html/other to txt
        # so if Extension is .txt, I check the existing of the file
        if Extension == ".txt" and os.path.isfile(File):
            info(f"in documents dir - processed: {BaseName}")

            # this document object describe infos about the document
            # for example the version of index algorithm
            FileIndex = f"{File}_wordindex_{VersionSeeking}"
            FileSentences = f"{File}_sentence_separator_{VersionSeeking}"

            if FunSentenceCreate and FunIndexCreate:
                FunSentenceCreate(Prg, FileSentences, FilePathOrigText=File)
                FunIndexCreate(Prg, FileIndex, FileSentences)

            DocumentObj = { "PathAbs": File,
                            "FileIndex": FileIndex,
                            "FileSentences": FileSentences,
                            "Index": util_json_obj.obj_from_file(FileIndex) if isfile(FileIndex) else dict(),
                            "Sentences": util.file_read_lines(Prg, FileSentences) if isfile(FileSentences) else []
            }

            DocumentObjects[BaseName] = DocumentObj  # we store the documents based on their basename

        elif Extension in ExtensionsInFuture:
            info(f"in documents dir - this file type will be processed in the future: {BaseName}")

        else:
            # print_dev(Prg, "in documents dir - not processed file type:", BaseName)
            pass

    return DocumentObjects

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
        # don't duplicate other files, document info json for example
        if ".gz" in FileName[-3:]:
            BaseName = os.path.basename(FileName).replace(".gz", "")
            print(f"Sample doc duplication... {BaseName}   {FileName}")
            ReadSuccess, TextContent = util.file_read_all(Prg, FileName, Gzipped=True)
            FileNameSaved = os.path.join(DirTarget, BaseName)
            # if a previous file exists with same name, it overwrites
            util.file_write_utf8_error_avoid(Prg, FileNameSaved, TextContent)

