from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from src.logger import logging
from src.exception import CustomException
import sys

class Pdf_Process:

    def __init__(self) -> None:
        self._all_docs = []
        self.set_prefix("")

    def set_files(self, files):
        self._pdf_files = files

    def set_prefix(self, prefix):
        self._prefix = prefix
        
    def get_text_chunks(self):
        """Splits the documents into chunks of text."""
        # assert len(self._all_docs) != 0 
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1536, chunk_overlap=150,
                separators=["\n\n", "\n", "(?<=\. )", " ", ""],
                )
            chunks = text_splitter.split_documents(self._all_docs)
            logging.info(f"Number of chunks splitted is : {len(chunks)}")
            return chunks
        except Exception as e:
            logging.error(f"Error occurred during document loading files: {str(e)}")
            raise CustomException(e,sys)
        
    def set_pdf_files(self, files):
        for pdf_file in files:
            try:
                loader = PyPDFLoader(self._prefix+pdf_file)
                documents = loader.load()
                self._all_docs.extend(documents)
                logging.info(f"Number of documents loaded from '{pdf_file}' is: {len(documents)}")
            except FileNotFoundError as e:
                logging.error(f"Error occurred during loading {pdf_file}: {e}")
            except PermissionError as e:
                logging.error(f"Error occurred during loading {pdf_file}: {e}")
            except Exception as e:
                logging.error(f"Error occurred during loading {pdf_file}: {e}")
    
    def set_text_documen(self, txt):
        self._all_docs.append(txt)

class File_main:

    def get_chuncks(pdf_files, prefix= None):
        file_obj = Pdf_Process()

        if prefix is not None:
            file_obj.set_prefix(prefix)

        try:
            file_obj.set_pdf_files(pdf_files)
        except (FileNotFoundError, PermissionError) as e:
            raise CustomException(e,sys)
        return file_obj.get_text_chunks()