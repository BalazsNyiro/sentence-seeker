# -*- coding: utf-8 -*-
import util, os
import util_json_obj, ui_tkinter_boot_progress_bar
from os.path import isfile
import array

# TODO: refactor this func, LOAD document db in local config
# and don't use document_samples in real environment
ExtensionsConvertable = [".pdf", ".htm", ".html"]
ExtensionsInFuture = [".epub", ".mobi"]

# fixme: TEST IT
def file_convert_to_txt_if_necessary(Prg, FileOrig, FileBaseNames__OrigNames):
    BaseNameNoExt, ExtensionLow = util.basename_without_extension__ext(FileOrig, ExtensionLower=True)
    if ExtensionLow in ExtensionsConvertable:

        FilePathConvertedToText = util.filename_without_extension(FileOrig) + ".txt"
        FileBaseNames__OrigNames[BaseNameNoExt] = FileOrig

        if not os.path.isfile(FilePathConvertedToText):  # convert if it's necessary

            if ExtensionLow == ".pdf":
                Converter = Prg["ConverterPdfToText"]

            if ExtensionLow == ".htm" or ExtensionLow == ".html":
                Converter = Prg["ConverterHtmlToText"]

            if Converter(Prg, FileOrig, FilePathConvertedToText):
                info("Successful conversion to txt: " + FileOrig)
            else:
                ConversionErrorMsg = f"Error, file conversion: {FileOrig}"
                util.log(Prg, ConversionErrorMsg)
                info(ConversionErrorMsg)

_DocsSampleSourceWebpages = None
def document_obj_create_in_document_objects(Prg, DocumentObjects, FileOrigNames, FileTextAbsPath, ProgressPercent, FileIndexAbsPath, FileSentencesAbsPath, Verbose=True):

    BaseNameNoExt, Extension = util.basename_without_extension__ext(FileTextAbsPath)
    if BaseNameNoExt in FileOrigNames: # I can do it with .get() but it's more descriptive
        FileOrig = FileOrigNames[BaseNameNoExt]
    else:
        FileOrig = BaseNameNoExt + Extension

    if not Prg.get("TestExecution", False):  # during test exec hide progress
        info(f"{ProgressPercent} in documents dir - processed: {BaseNameNoExt}", Verbose=Verbose)
    global _DocsSampleSourceWebpages
    if not _DocsSampleSourceWebpages:
        _, _DocsSampleSourceWebpages = util_json_obj.obj_from_file(os.path.join(Prg["DirTextSamples"], "document_samples_source_webpages.json"))

    if BaseNameNoExt not in Prg["DocumentsSourceWebpages"]:
        if BaseNameNoExt in _DocsSampleSourceWebpages["docs"]:
            DocObj = _DocsSampleSourceWebpages["docs"][BaseNameNoExt]
        else:
            DocObj = {"url": "url_unknown",
                      "source_name": "source_unknown",
                      "license": "license_unknown"}

        util_json_obj.doc_source_webpages_update_in_file_and_Prg(Prg, BaseNameNoExt, DocObj)  # and reload the updated db

    # Original: lists.
    # Arrays are more complex, less memory usage:
    # _Status, WordPositionInLines = util_json_obj.obj_from_file(FileIndexAbsPath) if isfile(FileIndexAbsPath) else (ok, dict())
    WordPositionInLines = dict()
    if isfile(FileIndexAbsPath):
        Status, JsonObjReply = util_json_obj.obj_from_file(FileIndexAbsPath)
        if Status == "ok":
            for Word, IndexList in JsonObjReply.items():
                WordPositionInLines[Word] = array.array("I", IndexList)
                                            # fastest to call array directly
                                            # util.int_list_to_array(IndexList)
        else:
            Prg["MessagesForUser"].append(JsonObjReply)

    DocumentObjects[BaseNameNoExt] = \
           document_obj(FileOrigPathAbs=FileOrig,  # if you use pdf/html, the original
                        FileTextPathAbs=FileTextAbsPath,  # and text files are different
                        FileIndex=FileIndexAbsPath,
                        FileSentences=FileSentencesAbsPath,
                        WordPositionInLines=WordPositionInLines,

                        # list of sentences
                        Sentences=util.file_read_lines_simple(FileSentencesAbsPath) if isfile(FileSentencesAbsPath) else [])


def info(Txt, Verbose=True):
    print(Txt, flush=True) if Verbose else 0

# Tested
def document_objects_collect_from_dir_documents(Prg,
                                                VersionSeeker="version_not_set",
                                                FunSentenceCreate=None,
                                                FunIndexCreate=None,
                                                Verbose=True,

                                                # in testcases we want to load only selected files, not all
                                                LoadOnlyThese=None  # ['BaseNameWithoutExt'] the positive examples
                                                ):
    DocumentObjects = dict() # ssp-

    DirDoc = Prg["DirDocuments"]
    for FileConvertableLater in util.files_abspath_collect_from_dir(DirDoc, WantedExtensions=ExtensionsInFuture):
        info(f"in documents dir - this file type will be processed in the future: {FileConvertableLater}")

    FilesConvertable = util.files_abspath_collect_from_dir(DirDoc, WantedExtensions=ExtensionsConvertable)

    FileBaseNames__OrigNames = {}
    for FileToTxt in FilesConvertable:
        file_convert_to_txt_if_necessary(Prg, FileToTxt, FileBaseNames__OrigNames)

    FilesTxt = util.files_abspath_collect_from_dir(DirDoc, WantedExtensions=[".txt"])
    LenFiles = len(FilesTxt)

    FileEndIndex = "_wordindex_{VersionSeeker}"
    FileEndSentence = f"_sentence_separator_{VersionSeeker}"

    ################# sentence / index creation #############################
    if FunSentenceCreate and FunIndexCreate:
        for FileNum, FileTextAbsPath in enumerate(FilesTxt, start=1): # All files recursively collected from DirDocuments
            ui_tkinter_boot_progress_bar.progressbar_refresh_if_displayed(Prg, LenFiles*2, FileNum)

            # this document object describe infos about the document
            # for example the version of index algorithm
            FileIndexAbsPath = FileTextAbsPath + FileEndIndex
            FileSentencesAbsPath = FileTextAbsPath + FileEndSentence

            FunSentenceCreate(Prg, FileSentencesAbsPath, FileTextAbsPath=FileTextAbsPath)
            FunIndexCreate(Prg, FileIndexAbsPath, FileSentencesAbsPath)

    ################# document obj create  #############################
    # start = 1:  if we have 10 elems, last FileNum has to reach 10
    for FileNum, FileTextAbsPath in enumerate(FilesTxt, start=1): # All files recursively collected from DirDocuments
        ProgressPercent = ui_tkinter_boot_progress_bar.progressbar_refresh_if_displayed(Prg, LenFiles*2, FileNum+LenFiles)

        FileIndexAbsPath = FileTextAbsPath + FileEndIndex
        FileSentencesAbsPath = FileTextAbsPath + FileEndSentence

        document_obj_create_in_document_objects(Prg, DocumentObjects, FileBaseNames__OrigNames,
                                                FileTextAbsPath, ProgressPercent,
                                                FileIndexAbsPath, FileSentencesAbsPath, Verbose=Verbose)
    return DocumentObjects

def document_obj(FileOrigPathAbs="", FileTextPathAbs="", FileIndex="", FileSentences="", WordPositionInLines="", Sentences=""):
    return {"FileOrigPathAbs": FileOrigPathAbs,  # if you use pdf/html, the original
            "FileTextPathAbs": FileTextPathAbs,  # and text files are different
            "FileIndex": FileIndex,
            "FileSentences": FileSentences,
            "WordPosition": WordPositionInLines,
            "Sentences": Sentences
           }


# TODO: TEST it
def docs_copy_samples_into_dir_if_necessary(Prg):
    util.dir_create_if_necessary(Prg, Prg["DirDocuments"])
    print(f'Program dir documents: {Prg["DirDocuments"]}', flush=True)

    DocumentsAvailable = document_objects_collect_from_dir_documents(Prg)

    if not DocumentsAvailable:
        DirTextSamples = os.path.join(Prg["DirDocuments"], "text_samples")
        util.dir_create_if_necessary(Prg, DirTextSamples)
        util.web_get_pack_wikipedia(Prg, DirTextSamples)
        docs_copy_samples_into_dir(Prg, DirTextSamples)

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

# used in tests
def doc_objects_delete__file_abspath(Prg, FileAbsPathWithExt):
    BaseName = os.path.basename(FileAbsPathWithExt)
    BaseNameNoExt = util.filename_without_extension(BaseName)
    doc_objects_delete__basename(Prg, BaseNameNoExt)
    util.file_del(FileAbsPathWithExt) # del orig file in every case, if DocObj doesn't exis

def doc_objects_delete__basename(Prg, BaseNameNoExt):
    if DocObj := Prg["DocumentObjectsLoaded"].pop(BaseNameNoExt, None):
        util.file_del(DocObj["FileOrigPathAbs"])
        util.file_del(DocObj["FileTextPathAbs"])
        util.file_del(DocObj["FileIndex"])
        util.file_del(DocObj["FileSentences"])
        util_json_obj.doc_source_webpages_update_in_file_and_Prg(Prg, BaseNameNoExtRemove=BaseNameNoExt)
