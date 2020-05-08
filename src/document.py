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


    DocumentObjects = dict()
    ExtensionsInFuture = {".html": 0, ".htm": 0}

    for FileText in util.files_abspath_collect_from_dir(Prg["DirDocuments"]):

        FileOrig = FileText
        BaseNameOrig = BaseNameText = os.path.basename(FileText)
        Extension = pathlib.Path(FileText).suffix.lower()

        if Extension == ".pdf":
            info(f"in documents dir - pdf -> txt conversion: {BaseNameText}")
            FilePathWithoutExtension = FileText.rsplit(".", 1)[0]
            FilePathTxt = f"{FilePathWithoutExtension}.txt"
            if not os.path.isfile(FilePathTxt):
                ConversionExecuted = Prg["PdfToTextConvert"](FileText, FilePathTxt)
                if ConversionExecuted:
                    Extension = ".txt"
                    FileText = FileText[:-4] + Extension  # FileText: pdf -> txt
                    BaseNameText = os.path.basename(FileText)
                else:
                    print(f"Error: pdf -> txt conversion: {FileOrig}")
                    continue

        # errors can happen if we convert pdf/html/other to txt
        # so if Extension is .txt, I check the existing of the file
        if Extension == ".txt" and os.path.isfile(FileText):
            info(f"in documents dir - processed: {BaseNameText}")

            # this document object describe infos about the document
            # for example the version of index algorithm
            FileIndex = f"{FileText}_wordindex_{VersionSeeking}"
            FileSentences = f"{FileText}_sentence_separator_{VersionSeeking}"

            if FunSentenceCreate and FunIndexCreate:
                FunSentenceCreate(Prg, FileSentences, FilePathText=FileText)
                FunIndexCreate(Prg, FileIndex, FileSentences)

            DocumentObj = { "FileOrigPathAbs": FileOrig,  # if you use pdf/html, the original
                            "FileTextPathAbs": FileText,  # and text files are different

                            "FileIndex": FileIndex,
                            "FileSentences": FileSentences,
                            "Index": util_json_obj.obj_from_file(FileIndex) if isfile(FileIndex) else dict(),
                            "Sentences": util.file_read_lines(Prg, FileSentences) if isfile(FileSentences) else []
            }

            DocumentObjects[BaseNameOrig] = DocumentObj  # we store the documents based on their basename

        elif Extension in ExtensionsInFuture:
            info(f"in documents dir - this file type will be processed in the future: {BaseNameText}")

        else:
            # print_dev(Prg, "in documents dir - not processed file type:", BaseNameText)
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
    for FileName in util.files_abspath_collect_from_dir(Prg["DirTextSamples"]):
        # don't duplicate other files, document info json for example
        if ".gz" in FileName[-3:]:
            BaseName = os.path.basename(FileName).replace(".gz", "")
            # print(f"Sample doc duplication... {BaseName}   {FileName}")
            ReadSuccess, TextContent = util.file_read_all(Prg, FileName, Gzipped=True)
            FileNameSaved = os.path.join(DirTarget, BaseName)
            # if a previous file exists with same name, it overwrites
            util.file_write_utf8_error_avoid(Prg, FileNameSaved, TextContent)

