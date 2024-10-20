# Saleschat Chatbot Project: AI Chatbot Implementation in Low-Code Application.

This project aims to develop an AI-powered chatbot using advanced machine learning techniques and low-code development tools. The chatbot is capable of answering user queries by retrieving information from stored documents and offering intelligent, context-aware responses.

## Overview
The AI Chatbot is built using the LangChain framework and OpenAI models such as GPT-3.5 Turbo. It integrates QdrantDB as a vector store to enable semantic search on uploaded PDF documents, allowing users to ask questions and receive relevant, document-based answers. The chatbot’s key function is to provide intelligent, contextually accurate responses by understanding user intent and leveraging embeddings for information retrieval.

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
