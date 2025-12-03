import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import os

# --- Configuration ---
# 1. Update this path to your Service Account JSON file.
#    (It should be in the same folder as this script)
SERVICE_ACCOUNT_FILE = 'service_account_key.json'

# 2. Update this to the name of your text file.
INPUT_FILE_NAME = 'your_questions_file.txt'

# 3. Update this to the name of the Firestore Collection where you want to store the questions.
COLLECTION_NAME = 'questions'

def upload_questions_to_firestore():
    """
    Initializes Firebase and uploads each line from the text file 
    as a new document in the specified Firestore collection.
    """
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"ERROR: Service Account file not found at '{SERVICE_ACCOUNT_FILE}'")
        print("Please follow the setup steps to place the key file.")
        return

    # Initialize Firebase Admin SDK
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Admin SDK initialized successfully.")
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")
        return

    db = firestore.client()
    upload_count = 0

    try:
        with open(INPUT_FILE_NAME, 'r', encoding='utf-8') as file:
            print(f"Reading questions from '{INPUT_FILE_NAME}'...")
            for line_number, line in enumerate(file, 1):
                # Clean the line (remove leading/trailing whitespace and newlines)
                question_text = line.strip()

                if question_text: # Only process non-empty lines
                    # Construct the data structure matching your example
                    question_data = {
                        'text': question_text,
                        # Use Firestore's server timestamp for accuracy
                        'createdAt': datetime.datetime.now(datetime.timezone.utc)
                    }

                    # Add a new document to the collection
                    db.collection(COLLECTION_NAME).add(question_data)
                    upload_count += 1
                    
                    # Optional: Print progress
                    if upload_count % 100 == 0:
                        print(f"   ... Uploaded {upload_count} questions so far.")

        print("---")
        print(f"🎉 Successfully uploaded {upload_count} questions to Firestore collection '{COLLECTION_NAME}'.")

    except FileNotFoundError:
        print(f"❌ ERROR: Input file not found at '{INPUT_FILE_NAME}'. Please check the file name.")
    except Exception as e:
        print(f"❌ An unexpected error occurred during upload: {e}")

if __name__ == "__main__":
    upload_questions_to_firestore()