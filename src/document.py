# -*- coding: utf-8 -*-
import util, os
import util_json_obj
from os.path import isfile

# TODO: refactor this func, LOAD document db in local config
# and don't use document_samples in real environment

# Tested
def document_objects_collect_from_working_dir(Prg,
                                              VersionSeeking="version_not_set",
                                              FunSentenceCreate=None,
                                              FunIndexCreate=None,
                                              Verbose=True,

                                              # in testcases we want to load only selected files, not all
                                              LoadOnlyTheseFileBaseNames=None # ['FileBaseName'] is the positive example
                                              ):
    def info(Txt):
        if Verbose: print(Txt, flush=True)

    DocumentObjects = dict()
    ExtensionsInFuture = (".epub", ".mobi")

    DbDocumentUpdated = False
    Files = util.files_abspath_collect_from_dir(Prg["DirDocuments"])
    _Status, DocsSampleInfo = util_json_obj.obj_from_file(os.path.join(Prg["DirTextSamples"], "document_samples.json"))

    for FileNum, FileOrig in enumerate(Files): # All files recursively collected from DirDocuments
        Progress = f"{FileNum} / {len(Files)}"

        FileText = FileOrig
        BaseNameText = BaseNameOrig = os.path.basename(FileOrig)
        if LoadOnlyTheseFileBaseNames:
            if BaseNameOrig not in LoadOnlyTheseFileBaseNames:
                continue

        BaseNameOrigWithoutExtension = util.filename_without_extension(BaseNameOrig)
        Extension = util.filename_extension(BaseNameOrig)

        if Extension == ".pdf" or Extension == ".htm" or Extension == ".html":
            info(f"{Progress} in documents dir - pdf/html -> txt conversion: {BaseNameText}\n{FileOrig}\n\n")
            FilePathWithoutExtension = util.filename_without_extension(FileOrig)
            FilePathConvertedToText = f"{FilePathWithoutExtension}.txt"
            if not os.path.isfile(FilePathConvertedToText):
                #info(f"not exists: {FilePathConvertedToText}" )
                if Extension == ".pdf":
                    ConversionExecuted = Prg["PdfToTextConvert"](Prg, FileOrig, FilePathConvertedToText)
                if Extension == ".htm" or Extension == ".html":
                    ConversionExecuted = Prg["HtmlToTextConvert"](Prg, FileOrig, FilePathConvertedToText)

                if ConversionExecuted:
                    Extension = ".txt"
                    FileText = util.filename_without_extension(FileOrig) + Extension
                    BaseNameText = os.path.basename(FileText)
                else:
                    info(f"Error, file conversion: {FileOrig}")
                    continue
            else:
                # info(f"   exists: {FilePathConvertedToText}" )
                pass

        # errors can happen if we convert pdf/html/other to txt
        # so if Extension is .txt, I check the existing of the file
        if Extension == ".txt" and os.path.isfile(FileText):
            info(f"{Progress} in documents dir - processed: {BaseNameText}")

            # this document object describe infos about the document
            # for example the version of index algorithm
            FileIndex = f"{FileText}_wordindex_{VersionSeeking}"
            FileSentences = f"{FileText}_sentence_separator_{VersionSeeking}"

            if FunSentenceCreate and FunIndexCreate:
                FunSentenceCreate(Prg, FileSentences, FilePathText=FileText)
                IndexCreated = FunIndexCreate(Prg, FileIndex, FileSentences)

            if BaseNameOrigWithoutExtension not in Prg["DocumentsDb"]:
                DocObj = {"url": "url_unknown",
                          "source_name": "source_unknown",
                          "license": "license_unknown"}
                if BaseNameOrigWithoutExtension in DocsSampleInfo["docs"]:
                    DocObj = DocsSampleInfo["docs"][BaseNameOrigWithoutExtension]

                util_json_obj.doc_db_update_in_file_and_reload(Prg, BaseNameOrigWithoutExtension, DocObj) # and reload the updated db

            # Original: lists.
            #Arrays are more complex, less memory usage:
            # _Status, Index = util_json_obj.obj_from_file(FileIndex) if isfile(FileIndex) else (ok, dict())
            Index = dict()
            if isfile(FileIndex):
                Status, JsonObjReply = util_json_obj.obj_from_file(FileIndex)
                if Status == "ok":
                    for Word, IndexList in JsonObjReply.items():
                        Index[Word] = util.list_to_array(IndexList)
                else:
                    Prg["MessagesForUser"].append(JsonObjReply)

            DocumentObj = document_obj(FileOrigPathAbs=FileOrig,  # if you use pdf/html, the original
                                       FileTextPathAbs=FileText,  # and text files are different
                                       FileIndex=FileIndex,
                                       FileSentences=FileSentences,
                                       Index=Index,
                                       Sentences=util.file_read_lines(Prg, FileSentences) if isfile(FileSentences) else [])

            DocumentObjects[BaseNameOrigWithoutExtension] = DocumentObj  # we store the documents based on their basename

        elif Extension in ExtensionsInFuture:
            info(f"in documents dir - this file type will be processed in the future: {BaseNameText}")

        else:
            #util.print_dev(Prg, "in documents dir - not processed file type:", BaseNameText)
            pass

    return DocumentObjects

def document_obj(FileOrigPathAbs="", FileTextPathAbs="", FileIndex="", FileSentences="", Index="", Sentences=""):
    return {"FileOrigPathAbs": FileOrigPathAbs,  # if you use pdf/html, the original
            "FileTextPathAbs": FileTextPathAbs,  # and text files are different
            "FileIndex": FileIndex,
            "FileSentences": FileSentences,
            "Index": Index,
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

