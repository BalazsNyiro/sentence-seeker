# -*- coding: utf-8 -*-
import util, os, gzip
import util_json_obj
from os.path import isfile

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
        if Verbose: print(Txt)

    DocumentObjects = dict()
    ExtensionsInFuture = {".epub": 0, ".mobi": 0}

    DbDocumentUpdated = False
    for FileOrig in util.files_abspath_collect_from_dir(Prg["DirDocuments"]):

        FileText = FileOrig
        BaseNameOrig = BaseNameText = os.path.basename(FileOrig)
        if LoadOnlyTheseFileBaseNames:
            if BaseNameOrig not in LoadOnlyTheseFileBaseNames:
                continue

        Extension = util.filename_extension(FileOrig)

        if Extension == ".pdf" or Extension == ".htm" or Extension == ".html":
            info(f"in documents dir - pdf/html -> txt conversion: {BaseNameText}\n{FileOrig}\n\n")
            FilePathWithoutExtension = util.filename_without_extension(FileOrig)
            FilePathConvertedToText = f"{FilePathWithoutExtension}.txt"
            if not os.path.isfile(FilePathConvertedToText):
                #print("not exists: ", FilePathConvertedToText )
                if Extension == ".pdf":
                    ConversionExecuted = Prg["PdfToTextConvert"](Prg, FileOrig, FilePathConvertedToText)
                if Extension == ".htm" or Extension == ".html":
                    ConversionExecuted = Prg["HtmlToTextConvert"](Prg, FileOrig, FilePathConvertedToText)

                if ConversionExecuted:
                    Extension = ".txt"
                    FileText = util.filename_without_extension(FileOrig) + Extension
                    BaseNameText = os.path.basename(FileText)
                else:
                    print(f"Error, file conversion: {FileOrig}")
                    continue
            else:
                # print("   exists: ", FilePathConvertedToText )
                pass

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
                IndexCreated = FunIndexCreate(Prg, FileIndex, FileSentences)
                if IndexCreated:
                    util_json_obj.doc_db_update(Prg, BaseNameOrig) # and reload the updated db
                    DbDocumentUpdated = True

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

    if DbDocumentUpdated: # then reload infos
        Prg["DocumentsDb"] = util_json_obj.obj_from_file(Prg["FileDocumentsDb"])["docs"]

    return DocumentObjects

# TODO: TEST it
def docs_copy_samples_into_dir_if_necessary(Prg):
    DocumentsAvailable = document_objects_collect_from_working_dir(Prg)
    if not DocumentsAvailable:
        WikiPagesUse = input("\nDo you want to use Wikipedia page pack from Sentence seeker server? (y/n) ").strip()
        if WikiPagesUse.strip().lower() == "y":
            Url = "http://sentence-seeker.net/texts/packs/wikipedia.txt.gz"
            BinaryFromWeb = util.web_get("http://sentence-seeker.net/texts/packs/wikipedia.txt.gz", Binary=True)
            Bytes = gzip.decompress(BinaryFromWeb)
            Text = util.utf8_conversion_with_warning(Bytes, Url)
            print(Text)

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

