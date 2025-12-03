Here is a user-friendly version of the guide for your Firebase Questions Uploader scripts.

Firebase Questions Uploader: A Simple Guide
This tool provides Python scripts to quickly upload questions from a plain text file into your Firestore database and manage the question collection.

What You'll Need
You'll need a couple of things before you start:

Python: Make sure you have Python version 3.10 or newer installed.

The Firebase Admin SDK: You can install the required Python library using pip:

pip install firebase-admin

-Initial Setup
To allow the scripts to connect to your Firebase project, you need to set up a service account:

Obtain your service account key from the Firebase Console. You can usually find this under Project Settings in the Service Accounts tab.

Once generated, save the downloaded JSON file as service_account_key.json in the same directory as your Python scripts.

How to Use the Scripts
Both scripts, script.py (for uploading) and delete_all.py (for deleting), contain configuration variables at the top. Before running, ensure you set these to match your project:

SERVICE_ACCOUNT_FILE: The path to your Firebase credentials JSON (service_account_key.json).

COLLECTION_NAME: The exact name of your target Firestore collection.

INPUT_FILE_NAME: The name of your text file containing the questions (only required for script.py).

⬆️ Uploading Questions
Create a simple text file (e.g., questions.txt) where each line is a separate question you want to upload.

Example content:

What is your favorite color? How do you handle stress? What motivates you?

Run the upload script:

python3 script.py

Note: Running this script multiple times will create duplicate question entries in your Firestore collection.

🗑️ Deleting All Questions
To completely clear the collection specified in the configuration:

Run the deletion script:
python3 delete_all.py

The script will prompt you for confirmation before deleting any data.