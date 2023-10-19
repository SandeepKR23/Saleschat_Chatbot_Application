# ML Chatbot Project

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