from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from src.logger import logging
from src.exception import CustomException
import sys

class QdrantVector:

    def __init__(self):
        pass

    def set_client(self, qdrant_client1):
        self.client = qdrant_client1

    def collection_exists(self, collection_name: str) -> bool:
        """Checking if collection exists or not """
        try:
            self.client.get_collection(collection_name=collection_name)
            return True
        except Exception:
            return False

    def create_vector_store(self, chatbot_name, text_chunks):
        """
        Creates a vector store for the given chatbot name and text chunks.
        Args:
            chatbot_name: The name of the chatbot.
            text_chunks: A list of text chunks.
        Returns:
            A dictionary containing the message and the status of the vector store, or a string indicating that the vector store already exists.
        """
        try:
            if self.collection_exists(chatbot_name):
                logging.warning(f"Vector DB already exists with this name '{chatbot_name}'.")
                return {"message": "Vector DB already exists with this name"}

            self.client.create_collection(
                    collection_name=chatbot_name,
                    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),)

            embeddings = OpenAIEmbeddings()
            vector_store = Qdrant(client=self.client, collection_name=chatbot_name, embeddings=embeddings,)
            vector_store.add_documents(text_chunks)

            chatbot_status = self.client.get_collection(collection_name=chatbot_name).status
            logging.info(f"Chatbot '{chatbot_name}' is created successfully and the status of the bot is '{chatbot_status}'.")
            return {"message": "Chatbot created successfully", "status": chatbot_status}

        except Exception as e:
            logging.warning(f"Error occurred during document loading into Database '{str(e)}' for the chatbot '{chatbot_name}'")
            raise CustomException(e,sys)

    def update_vector_store(self, chatbot_name, text_chunks):
        """
        Creates a vector store for the given chatbot name and text chunks.
        Args:
            chatbot_name: The name of the chatbot.
            text_chunks: A list of text chunks.
        Returns:
            A dictionary containing the message and the status of the vector store, or a string indicating that the vector store already exists.
        """
        try:
            # if self.collection_exists(chatbot_name):
            #     self.log.warning(f"Vector DB already exists with this name '{chatbot_name}'.")
            #     return {"message": "Vector DB already exists with this name"}

            self.client.recreate_collection(
                    collection_name=chatbot_name,
                    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),)

            embeddings = OpenAIEmbeddings()
            vector_store = Qdrant(client=self.client, collection_name=chatbot_name, embeddings=embeddings,)
            vector_store.add_documents(text_chunks)

            chatbot_status = self.client.get_collection(collection_name=chatbot_name).status
            logging.info(f"Chatbot '{chatbot_name}' is created successfully and the status of the bot is '{chatbot_status}'.")
            return {"message": "Chatbot created successfully", "status": chatbot_status}

        except Exception as e:
            logging.warning(f"Error occurred during document loading into Database '{str(e)}' for the chatbot '{chatbot_name}'")
            raise CustomException(e,sys)


class QdrantMain:

    def create_collection(qdrant_client, chatbot_name: str, text_chunks):
        """Creates or gets the vector store for the given chatbot name and text chunks.
        Args:
            qdrant_client: A QdrantClient object.
            chatbot_name: The name of the chatbot.
            text_chunks: A list of text chunks.
        Returns:
            A dictionary containing the message and the status of the vector store, or a string indicating that the vector store already exists.
        """
        db_obj = QdrantVector()
        db_obj.set_client(qdrant_client)
        vectorstore = db_obj.create_vector_store(chatbot_name, text_chunks)
        return vectorstore
    
    def update_collection(qdrant_client, chatbot_name: str, text_chunks):
        """Updates the vector store for the given chatbot name and text chunks."""
        db_obj1 = QdrantVector()
        db_obj1.set_client(qdrant_client)
        vectorstore = db_obj1.update_vector_store(chatbot_name, text_chunks)
        return vectorstore
