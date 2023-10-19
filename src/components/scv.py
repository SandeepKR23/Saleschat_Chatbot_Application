from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Qdrant
from langchain.prompts import PromptTemplate
from src.logger import logging
from src.exception import CustomException
import sys

class Scvisitor:
    def __init__(self) -> None:
        pass

    def set_client(self, qdrant_client1):
        self.client= qdrant_client1

    def vector_store(self, chatbot_name):
        try:
            embeddings = OpenAIEmbeddings()
            vector_store = Qdrant(
                client=self.client,
                collection_name= chatbot_name,
                embeddings=embeddings,
            )
            model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

            # Build prompt
            template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. 
            Keep the answer as concise as possible. Use three sentences maximum.  
            {context}
            Question:{question}
            AI bot Answer:"""

            QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
            qa= RetrievalQA.from_chain_type(
                llm=model, 
                chain_type="stuff", 
                retriever=vector_store.as_retriever(), 
                chain_type_kwargs= {"prompt": QA_CHAIN_PROMPT})
            return qa
        except Exception as e:
            logging.error(f"Error occurred during creating QA chain: {str(e)}'.")
            raise CustomException(e,sys)

    def get_answer(self, bot_name: str, question: str):
        try:
            logging.info("Question from the chatbot '%s'.", bot_name)
            qa_chain = self.vector_store(bot_name)
            response = qa_chain({"query": question})
            return {"response": response["result"]}
        except Exception as e:
            logging.error(f"Error occurred during question processing: {str(e)}")
            raise CustomException(e,sys)
    
class Question_main:
    def ask_question(qdrant_client, bot_name ,question):
        scv_obj = Scvisitor()
        scv_obj.set_client(qdrant_client)
        answer = scv_obj.get_answer(bot_name, question)
        return answer
