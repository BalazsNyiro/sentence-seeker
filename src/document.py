# -*- coding: utf-8 -*-
import util, os, util_ui
import util_json_obj, ui_tkinter_boot_progress_bar
from os.path import isfile

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
                Converter = Prg["PdfToTextConvert"]

            if ExtensionLow == ".htm" or ExtensionLow == ".html":
                Converter = Prg["HtmlToTextConvert"]

            if Converter(Prg, FileOrig, FilePathConvertedToText):
                info("Successful conversion to txt: " + FileOrig)
            else:
                ConversionErrorMsg = f"Error, file conversion: {FileOrig}"
                util.log(Prg, ConversionErrorMsg)
                info(ConversionErrorMsg)

_DocsSampleInfo = None
def document_obj_create(Prg, FileOrigNames, FileTextAbsPath, ProgressPercent, VersionSeeker, FunSentenceCreate, FunIndexCreate, Verbose=True):
    if not os.path.isfile(FileTextAbsPath):
        return None

    BaseNameNoExt, Extension = util.basename_without_extension__ext(FileTextAbsPath)
    if BaseNameNoExt in FileOrigNames: # I can do it with .get() but it's more descriptive
        FileOrig = FileOrigNames[BaseNameNoExt]
    else:
        FileOrig = BaseNameNoExt + Extension

    if not Prg.get("TestExecution", False):  # during test exec hide progress
        info(f"{ProgressPercent} in documents dir - processed: {BaseNameNoExt}", Verbose=Verbose)
    global _DocsSampleInfo
    if not _DocsSampleInfo:
        _, _DocsSampleInfo = util_json_obj.obj_from_file(os.path.join(Prg["DirTextSamples"], "document_samples.json"))

    # this document object describe infos about the document
    # for example the version of index algorithm
    FileIndexAbsPath = f"{FileTextAbsPath}_wordindex_{VersionSeeker}"
    FileSentencesAbsPath = f"{FileTextAbsPath}_sentence_separator_{VersionSeeker}"

    WordPositionInLines = dict()
    if FunSentenceCreate and FunIndexCreate:
        FunSentenceCreate(Prg, FileSentencesAbsPath, FileTextAbsPath=FileTextAbsPath)
        FunIndexCreate(Prg, FileIndexAbsPath, FileSentencesAbsPath)

    if BaseNameNoExt not in Prg["DocumentsDb"]:
        if BaseNameNoExt in _DocsSampleInfo["docs"]:
            DocObj = _DocsSampleInfo["docs"][BaseNameNoExt]
        else:
            DocObj = {"url": "url_unknown",
                      "source_name": "source_unknown",
                      "license": "license_unknown"}

        util_json_obj.doc_db_update_in_file_and_Prg(Prg, BaseNameNoExt, DocObj)  # and reload the updated db

    # Original: lists.
    # Arrays are more complex, less memory usage:
    # _Status, WordPositionInLines = util_json_obj.obj_from_file(FileIndexAbsPath) if isfile(FileIndexAbsPath) else (ok, dict())
    if isfile(FileIndexAbsPath):
        Status, JsonObjReply = util_json_obj.obj_from_file(FileIndexAbsPath)
        if Status == "ok":
            for Word, IndexList in JsonObjReply.items():
                WordPositionInLines[Word] = util.int_list_to_array(IndexList)
        else:
            Prg["MessagesForUser"].append(JsonObjReply)

    return document_obj(FileOrigPathAbs=FileOrig,  # if you use pdf/html, the original
                        FileTextPathAbs=FileTextAbsPath,  # and text files are different
                        FileIndex=FileIndexAbsPath,
                        FileSentences=FileSentencesAbsPath,
                        WordPositionInLines=WordPositionInLines,

                        # list of sentences
                        Sentences=util.file_read_lines(Prg, FileSentencesAbsPath) if isfile(FileSentencesAbsPath) else [])


def info(Txt, Verbose=True):
    print(Txt, flush=True) if Verbose else 0

# Tested
def document_objects_collect_from_working_dir(Prg,
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

    for FileNum, FileTextAbsPath in enumerate(FilesTxt): # All files recursively collected from DirDocuments
        ProgressPercent = ui_tkinter_boot_progress_bar.progressbar_refresh_if_displayed(Prg, LenFiles, FileNum)

        if DocObj := document_obj_create(Prg, FileBaseNames__OrigNames, FileTextAbsPath, ProgressPercent, VersionSeeker, FunSentenceCreate, FunIndexCreate, Verbose=Verbose):
            BaseNameNoExt, _ = util.basename_without_extension__ext(FileTextAbsPath)
            DocumentObjects[BaseNameNoExt] = DocObj


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
    DocumentsAvailable = document_objects_collect_from_working_dir(Prg)
    DirTarget = os.path.join(Prg["DirDocuments"], "text_samples")

    util.dir_create_if_necessary(Prg, Prg["DirDocuments"])
    print(f'Program dir documents: {Prg["DirDocuments"]}', flush=True)
    util.dir_create_if_necessary(Prg, DirTarget)

    if not DocumentsAvailable:
        util.web_get_pack_wikipedia(Prg, DirTarget)
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

# Fixme: test it
def doc_objects_delete(Prg, FileAbsPathWithExt):
    BaseName = os.path.basename(FileAbsPathWithExt)
    BaseNameWithoutExt = util.filename_without_extension(BaseName)
    if DocObj := Prg["DocumentObjectsLoaded"].pop(BaseNameWithoutExt, None):
        util.file_del(DocObj["FileOrigPathAbs"])
        util.file_del(DocObj["FileTextPathAbs"])
        util.file_del(DocObj["FileIndex"])
        util.file_del(DocObj["FileSentences"])
    util.file_del(FileAbsPathWithExt) # del orig file in every case, if DocObj doesn't exis

