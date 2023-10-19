import os
import sys
from keyword import iskeyword
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from qdrant_client import QdrantClient
from openAI_setup import SetupClass
from src.components.file_process import File_main
from src.components.qdrant_db import QdrantMain
from src.components.scv import Question_main
from src.logger import logging
from src.exception import CustomException
from openAI_setup import clear_python_bytecode_cache

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
origins = ["*"]  # You can restrict this to specific origins for security.
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

# Load environment variables
load_dotenv()

# Initialize Qdrant client
qdrant_client = QdrantClient(os.getenv("QDRANT_HOST"))
# qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"),api_key=os.getenv("QDRANT_API_KEY"),)

class Filename(BaseModel):
    """Pydantic models: filename attribute."""
    filename: str

class ChatbotCreationRequest(BaseModel):
    """Pydantic models: declare the "shape" of the data as classes with attributes."""
    chatbot_name : str
    # constr(max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    files: list[Filename]
    
    @validator('chatbot_name')
    def validate_chatbotname(cls, name):
        """Checking for the classname validation"""
        if iskeyword(name):
            raise ValueError(f"Chatbot name cannot be a reserved keyword ({name})")
        return name.lower()

class ChatbotDeleteRequest(BaseModel):
    """Pydantic models: delete chatbot attributes"""
    chatbot_name : str

    @validator("chatbot_name", pre=True, always=True)
    def lower_case_chatbot_name(cls, value):
        return value.lower()

class QuestionInput(BaseModel):
    """Pydantic models: QuestionInput attributes"""
    question : str
    bot_name : str

    @validator("bot_name", pre=True, always=True)
    def lower_case_chatbot_name(cls, value):
        return value.lower()

@app.on_event("startup")
async def startup_event():
    try:
        clear_python_bytecode_cache()
        SetupClass.openai_setup()
        logging.info("Initial setup is done")
    except Exception as e:
        logging.error(f"Issue with the initial setup process")
        raise CustomException(e,sys)

@app.post("/create-chatbot/")
async def create_chatbot(request: ChatbotCreationRequest):
    """ 
    Creates a new chatbot from the given PDF files.
    Args:
        request: A ChatbotCreationRequest object containing the chatbot name and PDF files.
    Returns:
        A dictionary containing the message and the status of the chatbot creation, or a string indicating that the chatbot already exists.
    """
    logging.info("Chatbot Creation: Bot name is '%s'.", request.chatbot_name) 
    try:
        pdf_file_paths = [file.filename for file in request.files]
        logging.info("List of file names are %s for the chatbot '%s'.", pdf_file_paths, request.chatbot_name)
        path_prefix= os.getenv("FILE_PATH_PREFIX")
        text_chunks= File_main.get_chuncks(pdf_file_paths, path_prefix)
        vectorstore = QdrantMain.create_collection(qdrant_client, request.chatbot_name, text_chunks)
        return vectorstore
    except Exception as e:
        logging.error("Chatbot creation failed due to the error: '%s'.", e) 

@app.post("/update-chatbot/")
async def update_chatbot(request: ChatbotCreationRequest):
    """ 
    Creates a new chatbot from the given PDF files.
    Args:
        request: A ChatbotCreationRequest object containing the chatbot name and PDF files.
    Returns:
        A dictionary containing the message and the status of the chatbot creation, or a string indicating that the chatbot already exists.
    """
    logging.info("Chatbot Creation: Bot name is '%s'", request.chatbot_name) 
    try:
        pdf_file_paths = [file.filename for file in request.files]
        logging.info("List of file names are %s for the chatbot '%s'", pdf_file_paths, request.chatbot_name)
        path_prefix= os.getenv("FILE_PATH_PREFIX")
        text_chunks= File_main.get_chuncks(pdf_file_paths, path_prefix)
        vectorstore = QdrantMain.update_collection(qdrant_client, request.chatbot_name, text_chunks)
        return vectorstore
    except Exception as e:
        logging.error("Chatbot creation failed due to the error: '%s'", e) 

@app.post("/delete-chatbot/")
async def delete_chatbot(request_data: ChatbotDeleteRequest):
    """ Deletes the chatbot with the given name.
        Args:
            request_data: A ChatbotDeleteRequest object containing the chatbot name.
        Returns:
            A dictionary containing the message and the status of the chatbot deletion, or a string indicating that the chatbot does not exist.
    """
    try:
        chatbot_name = request_data.chatbot_name
        # Check if the collection exists
        if qdrant_client.get_collection(collection_name=chatbot_name):
            qdrant_client.delete_collection(collection_name=chatbot_name)
            logging.info(f"Delete: Chatbot '{chatbot_name}' deleted successfully")
            return {"message": f"Chatbot '{chatbot_name}' deleted successfully"}
        
        logging.info("Chatbot '%s' does not exist!!!", chatbot_name)
        return {"message": f"Chatbot '{chatbot_name}' does not exist!!!"}
    except Exception as e:
        logging.warning("Error occurred during chatbot deletion.")
        raise CustomException(e,sys)

@app.post("/ask-question/")
async def ask_question(request_ques: QuestionInput):
    """
    Handles an incoming POST request to ask a question to the chatbot.
    Args:
        request_ques (QuestionInput): A Pydantic model containing the question and bot name.
    Returns:
        Response: The response from the chatbot after processing the question.
    """
    bot_question = request_ques.question
    bot_name = request_ques.bot_name
    response= Question_main.ask_question(qdrant_client, bot_name, bot_question)
    return response

@app.get("/")
async def read_root():
    """Testing purpose"""
    return {"message": "Hello, FastAPI!"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, ssl_keyfile="C:/Users/rajku-sa/Documents/MEGA/My_code/ML_Bot_Project/certificates/domain.key", ssl_certfile="C:/Users/rajku-sa/Documents/MEGA/My_code/ML_Bot_Project/certificates/domain-1689779644033.crt")
    # uvicorn.run(app, host="127.0.0.1", port=5000)
