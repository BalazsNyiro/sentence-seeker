# -*- coding: utf-8 -*-
import util, os
import util_json_obj, ui_tkinter_boot_progress_bar
from os.path import isfile
import array
import concurrent.futures
from concurrent.futures import FIRST_COMPLETED, ALL_COMPLETED

ExtensionsConvertable = [".pdf", ".htm", ".html"]
ExtensionsInFuture = [".epub", ".mobi"]

# fixme: TEST IT
def file_convert_to_txt_if_necessary(Prg, FileOrigAbsPath, Converted__FileBaseNames__OrigNames):
    BaseNameNoExt, ExtensionLow = util.basename_without_extension__ext(FileOrigAbsPath, ExtensionLower=True)
    if ExtensionLow in ExtensionsConvertable:

        FilePathConvertedToText = util.filename_without_extension(FileOrigAbsPath) + ".txt"
        Converted__FileBaseNames__OrigNames[BaseNameNoExt] = FileOrigAbsPath

        if not os.path.isfile(FilePathConvertedToText):  # convert if it's necessary

            if ExtensionLow == ".pdf":
                Converter = Prg["ConverterPdfToText"]

            if ExtensionLow == ".htm" or ExtensionLow == ".html":
                Converter = Prg["ConverterHtmlToText"]

            if Converter(Prg, FileOrigAbsPath, FilePathConvertedToText):
                info("Successful conversion to txt: " + FileOrigAbsPath)
            else:
                ConversionErrorMsg = f"Error, file conversion: {FileOrigAbsPath}"
                util.log(Prg, ConversionErrorMsg)
                info(ConversionErrorMsg)

_DocsSampleSourceWebpages = None
def document_obj_create_in_document_objects(Prg, DocumentObjects, ConvertedFileOrigNames_AbsPath, FileTextAbsPath, FileIndexAbsPath, FileSentencesAbsPath, WordPositionInLines=None):
    if WordPositionInLines == None:
        WordPositionInLines = dict()

    BaseNameNoExt, DotExtension = util.basename_without_extension__ext(FileTextAbsPath)
    if BaseNameNoExt in ConvertedFileOrigNames_AbsPath: # I can do it with .get() but it's more descriptive
        BaseNameNoExtOrig, DotExtensionOrig = util.basename_without_extension__ext(FileTextAbsPath)
        FileOrig = BaseNameNoExtOrig + DotExtensionOrig
    else:
        FileOrig = BaseNameNoExt + DotExtension

    # if not Prg.get("TestExecution", False):  # during test exec hide progress
    #     info(f"{ProgressPercent} in documents dir - processed: {BaseNameNoExt}", Verbose=Verbose)
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

        util_json_obj.doc_source_webpages_update_in_Prg(Prg, BaseNameNoExt, DocObj)  # and reload the updated db

    DocumentObjects[BaseNameNoExt] = \
           document_obj(FileOrigPathAbs=FileOrig,  # if you use pdf/html, the original
                        FileTextAbsPath=FileTextAbsPath,  # and text files are different
                        FileIndex=FileIndexAbsPath,
                        FileSentences=FileSentencesAbsPath,
                        WordPositionInLines=WordPositionInLines,

                        # list of sentences
                        Sentences=util.file_read_lines(Prg, Fname=FileSentencesAbsPath) if isfile(FileSentencesAbsPath) else [])


def info(Txt, Verbose=True):
    print(Txt, flush=True) if Verbose else 0

# can't be embedded function in another func!
# Can't pass Prg through multiple function parameter pass, you have to create a thin Prg before fun call
def sentence_and_index_create(FunSentenceCreate, FunIndexCreate, SubSentenceMultiplier, WordPositionMultiplier, FileSentencesAbsPath, FileTextAbsPath, FileIndexAbsPath):
    FunSentenceCreate({}, FileSentencesAbsPath, FileTextAbsPath=FileTextAbsPath)
    FunIndexCreate({}, FileIndexAbsPath, FileSentencesAbsPath, SubSentenceMultiplier=SubSentenceMultiplier, WordPositionMultiplier=WordPositionMultiplier)
    return FileTextAbsPath

def word_pos_in_line_load(FileIndexAbsPath):
    WordPositionInLines = dict()
    MessageForUser = None
    if isfile(FileIndexAbsPath):
        Status, JsonObjReply = util_json_obj.obj_from_file(FileIndexAbsPath)

        if Status == "ok":
            for Word, IndexList in JsonObjReply.items():
                WordPositionInLines[Word] = array.array("Q", IndexList)
                # fastest to call array directly than
                # util.int_list_to_array(IndexList)
        else:
            MessageForUser = JsonObjReply

    # FileIndexAbsPath in return is important because it's processed parallel and I don't know the processed file name from caller side
    return FileIndexAbsPath, WordPositionInLines, MessageForUser
    #################################################################


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

    ConvertedFileBaseNames__OrigNames = {}
    for FileToTxt in FilesConvertable:
        file_convert_to_txt_if_necessary(Prg, FileToTxt, ConvertedFileBaseNames__OrigNames)

    FilesTxt = util.files_abspath_collect_from_dir(DirDoc, WantedExtensions=[".txt"])
    LenFiles = len(FilesTxt)

    FileEndIndex = f"_wordindex_{VersionSeeker}"
    FileEndSentence = f"_sentence_separator_{VersionSeeker}"

    ################# sentence / index creation #############################
    if FunSentenceCreate and FunIndexCreate:
        MultiCore = True

        # MultiCore = False # Set it false if you want to debug

        if not Prg["OsIsUnixBased"] or Prg["TestExecution"]:
            MultiCore = False

        if MultiCore:

            Futures = []
            with concurrent.futures.ProcessPoolExecutor() as Executor:
                for FileNum, FileTextAbsPath in enumerate(FilesTxt, start=1): # All files recursively collected from DirDocuments

                    # this document object describe infos about the document
                    # for example the version of index algorithm
                    FileIndexAbsPath = FileTextAbsPath + FileEndIndex
                    FileSentencesAbsPath = FileTextAbsPath + FileEndSentence
                    Futures.append(Executor.submit(sentence_and_index_create,
                                    FunSentenceCreate, FunIndexCreate,
                                    Prg["SubSentenceMultiplier"], Prg["WordPositionMultiplier"],
                                    FileSentencesAbsPath, FileTextAbsPath, FileIndexAbsPath))

                DonePrevLen = -1
                while True:
                    Done, NotDone = concurrent.futures.wait(Futures, return_when=FIRST_COMPLETED)
                    if len(Done) != DonePrevLen:
                        DonePrevLen = len(Done)
                        print("indexed:", len(Done), "  waiting:", len(NotDone))
                    ui_tkinter_boot_progress_bar.progressbar_refresh_if_displayed(Prg, LenFiles * 2, len(Done))
                    if not NotDone:
                        break

        else: # on windows I use one Core to index files
            for FileNum, FileTextAbsPath in enumerate(FilesTxt,
                                                      start=1):  # All files recursively collected from DirDocuments
                ui_tkinter_boot_progress_bar.progressbar_refresh_if_displayed(Prg, LenFiles * 2, FileNum)

                # this document object describe infos about the document
                # for example the version of index algorithm
                FileIndexAbsPath = FileTextAbsPath + FileEndIndex
                FileSentencesAbsPath = FileTextAbsPath + FileEndSentence

                FunSentenceCreate(Prg, FileSentencesAbsPath, FileTextAbsPath=FileTextAbsPath)
                FunIndexCreate(Prg, FileIndexAbsPath, FileSentencesAbsPath)


                print("indexed:", FileNum, "  waiting:", len(FilesTxt) - FileNum)

    ################### parallel index loading ###############
    ######  the parallel solution is slower
    # WordPositionAll = dict()
    # Futures = []
    # with concurrent.futures.ProcessPoolExecutor() as Executor:
    #     for FileTextAbsPath in FilesTxt:
    #         FileIndexAbsPath = FileTextAbsPath + FileEndIndex
    #         Futures.append(Executor.submit(word_pos_in_line_load, FileIndexAbsPath))
    #         # WordPositionInLines, MessageForUser = word_pos_in_line_load(FileIndexAbsPath)

    #     concurrent.futures.wait(Futures, return_when=ALL_COMPLETED)
    #     for Future in Futures:
    #         # because of parallel execution I have to give back the processed FileIndexAbsPath
    #         FileIndexAbsPath, WordPositionInLines, MessageForUser = Future.result()
    #         if MessageForUser:
    #             Prg["MessagesForUser"].append(MessageForUser)
    #         else:
    #             WordPositionAll[FileIndexAbsPath] = WordPositionInLines

    ################# document obj create  #############################
    # start = 1:  if we have 10 elems, last FileNum has to reach 10
    for FileNum, FileTextAbsPath in enumerate(FilesTxt, start=1): # All files recursively collected from DirDocuments
        ProgressPercent = ui_tkinter_boot_progress_bar.progressbar_refresh_if_displayed(Prg, LenFiles*2, FileNum+LenFiles)

        FileIndexAbsPath = FileTextAbsPath + FileEndIndex
        FileSentencesAbsPath = FileTextAbsPath + FileEndSentence

        _, WordPositionInLines, MessageForUser = word_pos_in_line_load(FileIndexAbsPath)

        document_obj_create_in_document_objects(Prg, DocumentObjects, ConvertedFileBaseNames__OrigNames,
                                                FileTextAbsPath, FileIndexAbsPath, FileSentencesAbsPath,
                                                 WordPositionInLines = WordPositionInLines)

    util_json_obj.doc_source_webpages_save_from_memory_to_file(Prg)
    return DocumentObjects


def document_obj(FileOrigPathAbs="", FileTextAbsPath="", FileIndex="", FileSentences="", WordPositionInLines="", Sentences=""):
    return {"FileOrigPathAbs": FileOrigPathAbs,  # if you use pdf/html, the original
            "FileTextPathAbs": FileTextAbsPath,  # and text files are different
            "FileIndex": FileIndex,
            "FileSentences": FileSentences,
            "WordPosition": WordPositionInLines,
            "Sentences": Sentences
            }


def docs_copy_samples_into_dir_if_necessary(Prg, LoadDefaultsForced=False):
    util.dir_create_if_necessary(Prg, Prg["DirDocuments"])
    # print(f'Program dir documents: {Prg["DirDocuments"]}', flush=True)

    DirTextSamples = os.path.join(Prg["DirDocuments"], "text_samples")
    util.dir_create_if_necessary(Prg, DirTextSamples)
    FilesTxt = util.files_abspath_collect_from_dir(DirTextSamples, WantedExtensions=ExtensionsConvertable + [".txt"])
    if (not FilesTxt) or LoadDefaultsForced:
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
