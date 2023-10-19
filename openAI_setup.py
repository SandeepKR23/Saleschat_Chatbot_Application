import os
from dotenv import load_dotenv
import requests
from src.logger import logging
import importlib.util
import shutil

def clear_python_bytecode_cache():
    """
    Clear the Python bytecode cache by deleting the __pycache__ directories in your project.
    """
    # Get the current working directory
    project_directory = os.getcwd()

    # Recursively find and delete all __pycache__ directories in the project directory
    for root, dirs, files in os.walk(project_directory):
        for directory in dirs:
            if directory == "__pycache__":
                cache_dir = os.path.join(root, directory)
                shutil.rmtree(cache_dir)

class SetupClass:
    @staticmethod
    def openai_setup():
        try:
            # Fetch the OpenAI API key from the database (replace this with your actual database retrieval logic)
            openai_api_key_from_db = fetch_api_key_from_database()

            # Update the .env file with the retrieved API key
            update_env_file(openai_api_key_from_db)

            # Load the updated .env file
            load_dotenv()

            openai_api_key = os.getenv("OPENAI_API_KEY")
            print(openai_api_key)
            logging.info("Open AI key is set")

            if openai_api_key is None or openai_api_key == "":
                logging.error("Open AI key is not set.")
                raise ValueError("OPENAI_API_KEY is not set")

            response = requests.get(
                "https://api.openai.com/v1/engines",
                headers={"Authorization": f"Bearer {openai_api_key}"},
            )

            if response.status_code != 200:
                logging.error("Invalid OpenAI API key: %s", response.status_code)
                raise ValueError(f"Invalid OpenAI API key: {response.status_code}")
        except Exception as e:
            logging.error("OpenAI Startup initialization failed: %s", e)
            raise

def fetch_api_key_from_database():
    # Replace this function with your actual logic to fetch the API key from the database
    # For example, you might use an ORM like SQLAlchemy or an API to retrieve the key.

    api_key = "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"
    print(api_key)
    return api_key

def update_env_file(api_key):
    # Read the current .env file and store the lines in a list
    with open(".env", "r") as env_file:
        lines = env_file.readlines()

    # Find and update the line with the OPENAI_API_KEY
    updated_lines = []

    for line in lines:
        if line.startswith("OPENAI_API_KEY="):
            updated_lines.append(f"OPENAI_API_KEY={api_key}\n")
        else:
            updated_lines.append(line)

    # Write the updated lines back to the .env file
    with open(".env", "w") as env_file:
        env_file.writelines(updated_lines)
