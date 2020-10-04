# -*- coding: utf-8 -*-
import util, os, util_ui
import util_json_obj, ui_tkinter_boot_progress_bar
from os.path import isfile

# TODO: refactor this func, LOAD document db in local config
# and don't use document_samples in real environment
ExtensionsConvertable = ".pdf.htm.html"
ExtensionsInFuture = ".epub.mobi"

# fixme: TEST IT
def file_convert_to_txt_if_necessary(Prg, FileOrig, ExtensionLow):
    FileText = FileOrig
    ConversionErrorMsg = ""

    if ExtensionLow in ExtensionsConvertable:
        FilePathConvertedToText = util.filename_without_extension(FileOrig) + ".txt"
        if not os.path.isfile(FilePathConvertedToText):  # convert if necessary

            if ExtensionLow == ".pdf":
                Converter = Prg["PdfToTextConvert"]
            if ExtensionLow == ".htm" or ExtensionLow == ".html":
                Converter = Prg["HtmlToTextConvert"]

            if Converter(Prg, FileOrig, FilePathConvertedToText):
                ExtensionLow = ".txt"
                FileText = FilePathConvertedToText
            else:
                ConversionErrorMsg = f"Error, file conversion: {FileOrig}"
                util.log(Prg, ConversionErrorMsg)

    return FileText, ExtensionLow, ConversionErrorMsg


_DocsSampleInfo = None
def document_obj_create(Prg, FileOrig, FileText, BaseNameNoExt, Progress, VersionSeeker, FunSentenceCreate, FunIndexCreate, Verbose=True):
    if not os.path.isfile(FileText):
        return None

    if not Prg.get("TestExecution", False):  # during test exec hide progress
        info(f"{Progress} in documents dir - processed: {BaseNameNoExt}", Verbose=Verbose)
    global _DocsSampleInfo
    if not _DocsSampleInfo:
        _, _DocsSampleInfo = util_json_obj.obj_from_file(os.path.join(Prg["DirTextSamples"], "document_samples.json"))

    # this document object describe infos about the document
    # for example the version of index algorithm
    FileIndex = f"{FileText}_wordindex_{VersionSeeker}"
    FileSentences = f"{FileText}_sentence_separator_{VersionSeeker}"

    WordPositionInLines = dict()
    if FunSentenceCreate and FunIndexCreate:
        FunSentenceCreate(Prg, FileSentences, FilePathText=FileText)
        FunIndexCreate(Prg, FileIndex, FileSentences)

    if BaseNameNoExt in Prg["DocumentsDb"]:
        Msg = f"Maybe you have more than one files with same Basename: {BaseNameNoExt}"
        print(Msg)
        util.log(Prg, Msg)
    else:
        if BaseNameNoExt in _DocsSampleInfo["docs"]:
            DocObj = _DocsSampleInfo["docs"][BaseNameNoExt]
        else:
            DocObj = {"url": "url_unknown",
                      "source_name": "source_unknown",
                      "license": "license_unknown"}

        util_json_obj.doc_db_update_in_file_and_Prg(Prg, BaseNameNoExt, DocObj)  # and reload the updated db

    # Original: lists.
    # Arrays are more complex, less memory usage:
    # _Status, WordPositionInLines = util_json_obj.obj_from_file(FileIndex) if isfile(FileIndex) else (ok, dict())
    if isfile(FileIndex):
        Status, JsonObjReply = util_json_obj.obj_from_file(FileIndex)
        if Status == "ok":
            for Word, IndexList in JsonObjReply.items():
                WordPositionInLines[Word] = util.int_list_to_array(IndexList)
        else:
            Prg["MessagesForUser"].append(JsonObjReply)

    return document_obj(FileOrigPathAbs=FileOrig,  # if you use pdf/html, the original
                        FileTextPathAbs=FileText,  # and text files are different
                        FileIndex=FileIndex,
                        FileSentences=FileSentences,
                        WordPositionInLines=WordPositionInLines,

                        # list of sentences
                        Sentences=util.file_read_lines(Prg, FileSentences) if isfile(FileSentences) else [])


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
    DocumentObjects = dict()

    Files = util.files_abspath_collect_from_dir(Prg["DirDocuments"])

    for FileNum, FileOrig in enumerate(Files): # All files recursively collected from DirDocuments
        # /home/user/file.txt ->  file.txt (basename) -> file
        BaseNameNoExt, ExtensionLow = util.basename_without_extension__ext(FileOrig, ExtensionLower=True)

        if ExtensionLow not in ".txt" + ExtensionsConvertable + ExtensionsInFuture:
            info(f"in documents dir - not processed file type: {FileOrig}")
            continue

        Progress = f"{FileNum} / {len(Files)}"
        ui_tkinter_boot_progress_bar.progressbar_refresh_if_displayed(Prg, Files, FileNum)

        if LoadOnlyThese and BaseNameNoExt not in LoadOnlyThese:
            continue # used in development, not for end users

        FileText, ExtensionLow, ConversionErrorMsg = file_convert_to_txt_if_necessary(Prg, FileOrig, ExtensionLow)
        if ConversionErrorMsg:
            info(ConversionErrorMsg)
            continue

        if ExtensionLow == ".txt":
            if DocObj := document_obj_create(Prg, FileOrig, FileText, BaseNameNoExt, Progress, VersionSeeker, FunSentenceCreate, FunIndexCreate, Verbose=Verbose):
                DocumentObjects[BaseNameNoExt] = DocObj

        elif ExtensionLow in ExtensionsInFuture:
            info(f"in documents dir - this file type will be processed in the future: {BaseNameNoExt}")

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

