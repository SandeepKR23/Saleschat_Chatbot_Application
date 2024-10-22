# Saleschat Chatbot Project: AI Chatbot Implementation in Low-Code Application.

## Project Overview
This project focuses on implementing an **AI-based chatbot** within a low-code platform to assist users in building multiple chatbots effortlessly. The application integrates **OpenAI’s GPT-3.5 Turbo** and **LangChain framework**, providing capabilities such as semantic search, entity extraction, and vector-based data storage using **QdrantDB**. This project aims to revolutionize the user experience by enabling seamless chatbot creation and interaction with PDF documents stored as vectors.
![langchain](https://github.com/user-attachments/assets/850e44f7-6ac5-45eb-93a8-6e5a48ebed85)

## Features
- **AI-Powered Chatbot**: Utilizes GPT-3.5 for natural language understanding and response generation.
- **Semantic Search**: Enables understanding of user intent and provides relevant, context-aware answers.
- **PDF Integration**: Allows chatbot interaction with PDF documents stored in QdrantDB for rich, document-based user responses.
- **Low-Code Development**: Simplifies the chatbot creation process, making it accessible to users without extensive programming knowledge.

## Technologies Used
- **OpenAI GPT-3.5 Turbo** for conversational capabilities.
- **LangChain** for seamless integration of language models.
- **QdrantDB** for vector storage and similarity search.
- **Low-Code Platform** for rapid development and deployment.

## Architecture
The architecture follows a modular approach with the following components:
![Project_ARc1](https://github.com/user-attachments/assets/5b7a2f4c-1e24-4bd7-a81f-9dc1cc0dd97d)

- **Chatbot Interface**: Front-end for users to interact with the chatbot.
- **Document Storage**: PDF documents are stored in QdrantDB as vectors.
- **Semantic Search Engine**: Facilitates accurate and context-aware search capabilities.
- **Chatbot Logic**: Powered by OpenAI’s GPT-3.5, providing personalized responses.
  
## OpenAI Pricing calculation.

Please find the detailed pricing breakdown for the Phase 1 project below. This includes all relevant cost estimations associated with the OpenAI model usage.
![image](https://github.com/user-attachments/assets/c456f562-cc95-4d26-9a4c-f058f27414ee)


## How It Works
- **Document Upload**: Users upload PDFs that are converted into vector embeddings and stored in QdrantDB.
- **User Interaction**: Users interact with the chatbot via a low-code interface.
- **Information Retrieval**: Chatbot performs a semantic search on the stored documents to provide relevant answers.
- **Response Generation**: GPT-3.5 generates human-like responses based on user queries and retrieved information.

## Screenshots
The initial interaction page with Emma, the chatbot.
   
![image](https://github.com/user-attachments/assets/767fbd95-2e04-4992-b2b0-f4dcc3541595)
![image](https://github.com/user-attachments/assets/4e48162d-9953-41fc-b82f-f0d038f3a8d0)
![image](https://github.com/user-attachments/assets/7e011804-a394-4054-b7da-0ec34334194e)
![image](https://github.com/user-attachments/assets/9a37575a-2694-44af-821c-9d50748350df)

Pleae refer to this file for more details **AI Chatbot Implementation in Low-Code Application Report.pdf**, it's available in the repositary.

# Created a environment
```
conda create -p venv python==3.11

conda activate venv/
```
# Install all necessary libraries
```
pip install -r requirements.txt
```

# Commands to execute code
```
uvicorn main:app --host 0.0.0.0 --port 5000 --ssl-keyfile "C:/Users/rajku-sa/Documents/MEGA/Ineuron/ML_Chatbot_Project/certificates/domain.key" --ssl-certfile "C:/Users/rajku-sa/Documents/MEGA/Ineuron/ML_Chatbot_Project/certificates/domain-1689779644033.crt"

uvicorn main:app --host 127.0.0.1 --port 8000
```

# Postman API's with data:

```
https://192.168.253.122:5000/create-chatbot
{
  "Chatbot_Name": "Chatbot123",
  "files": [
    {
      "filename": "ECT 01 Composable Enterprises Intro.pdf"
    },
    {
      "filename": "Research in AI-based chatbot.pdf"
    }
  ]
}
```
## License
This project is licensed under the MIT License. See the LICENSE file for details.
