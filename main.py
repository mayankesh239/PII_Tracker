import os
import logging
import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError
from github import Github

# MongoDB connection details
mongodb_uri = "mongodb+srv://mayankesh:password@cluster0.r6kp7ek.mongodb.net/?retryWrites=true&w=majority"
database_name = "pii_tracker_data"
collection_name = "sensitive_data"
commit_file = ".pii_commit"

# GitHub repository and file details
repository_url = "https://github.com/mayankesh239/main/"
file_path = "general.json"

# Logging configuration
logging.basicConfig(level=logging.INFO, filename="/home/mayankesh/Desktop/Akto/PII_Tracker/pii_sync.log")

def fetch_github_data(since_commit=None):

    try:
        # Initialize GitHub API client
        access_token = os.getenv("GITHUB_ACCESS_TOKEN")  # Set your access token as an environment variable
        g = Github(access_token)

        # Get the repository and file
        repository_parts = repository_url.replace("https://github.com/", "").split("/")
        repository_owner = repository_parts[0]
        repository_name = repository_parts[1]
        repository = g.get_repo(f"{repository_owner}/{repository_name}")

        # Get the file contents
        try:
            content_of_file = repository.get_contents(file_path)
            file_sha = content_of_file.sha
        except Exception as e:
            logging.error(f"Error accessing the file in the repository: {e}")
            return [], since_commit

        # Compare with the last synchronized commit
        if file_sha == since_commit:
            print("********************  The data is alerady upto date  ********************")
            return [], since_commit

        # Decode file contents and parse as JSON
        data = content_of_file.decoded_content.decode("utf-8")
        parsed_data = json.loads(data)

        # Filter sensitive data where "sensitive" is true
        sensitive_data = [item for item in parsed_data["types"] if item.get("sensitive")]

        print("******************** Successfully fetched the data from github ********************")

        print("new_commit: " + file_sha)
        # return parsed_data["types"], file_sha
        return sensitive_data, file_sha

    except Exception as e:
        logging.error(f"Error fetching data from GitHub: {e}")
        return [], since_commit

def update_mongodb_collection(data):
    try:
        # Connect to MongoDB
        client = MongoClient(mongodb_uri)
        db = client[database_name]
        collection = db[collection_name]

        # Clear existing data in the collection
        collection.delete_many({})

        # Insert new data into the collection having attributes name, regexPattern and onKey
        documents = [{"name": item["name"], "regexPattern": item["regexPattern"], "onKey": item["onKey"]} for item in data]
        collection.insert_many(documents)

        # Close the MongoDB connection
        client.close()
        print("******************** Successfully updated the mongoDB ********************")

    except ConnectionFailure as ce:
        logging.error(f"Error occurred while establishing a connection to MongoDB: {ce}")

    except BulkWriteError as bwe:
        logging.error(f"Error occurred during bulk write operation while updating the MongoDB collection.: {bwe.details}")

def retrieve_last_commit():
    if os.path.isfile(commit_file):
        with open(commit_file, "r") as file:
            last_commit = file.read().strip()
            print("last_commit: " + last_commit)
            return last_commit
        
    return None

def save_last_commit(new_commit):
    with open(commit_file, "w") as file:
        file.write(new_commit)


def main():
    try:
        # Read the last synchronized commit from commit file
        last_commit = retrieve_last_commit()

        # Fetch data from GitHub using github access token
        data, new_commit = fetch_github_data(since_commit=last_commit)

        # Update MongoDB collection if there are any changes in the github repository
        if data:
            update_mongodb_collection(data)
            save_last_commit(new_commit)

        logging.info("The script has been executed successfully.")
        print("******************** The script has been executed successfully ********************")

    except Exception as e:
        logging.error(f"An error occurred during the execution of the script: {e}")

if __name__ == "__main__":
    main()
