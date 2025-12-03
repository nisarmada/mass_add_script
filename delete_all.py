import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# --- Configuration ---
SERVICE_ACCOUNT_FILE = 'service_account_key.json'
COLLECTION_NAME = 'questions'

def delete_all_documents():
    """
    Deletes all documents from the specified Firestore collection.
    """
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"ERROR: Service Account file not found at '{SERVICE_ACCOUNT_FILE}'")
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
    
    # Get all documents in the collection
    collection_ref = db.collection(COLLECTION_NAME)
    docs = collection_ref.stream()
    
    deleted_count = 0
    
    print(f"Deleting all documents from '{COLLECTION_NAME}' collection...")
    
    # Delete documents in batches for efficiency
    batch = db.batch()
    batch_count = 0
    
    for doc in docs:
        batch.delete(doc.reference)
        batch_count += 1
        deleted_count += 1
        
        # Firestore batches are limited to 500 operations
        if batch_count >= 500:
            batch.commit()
            print(f"   ... Deleted {deleted_count} documents so far.")
            batch = db.batch()
            batch_count = 0
    
    # Commit any remaining deletions
    if batch_count > 0:
        batch.commit()
    
    print("---")
    print(f"🗑️  Successfully deleted {deleted_count} documents from '{COLLECTION_NAME}' collection.")

if __name__ == "__main__":
    # Safety confirmation
    print(f"⚠️  WARNING: This will delete ALL documents in the '{COLLECTION_NAME}' collection!")
    confirm = input("Type 'DELETE' to confirm: ")
    
    if confirm == 'DELETE':
        delete_all_documents()
    else:
        print("❌ Deletion cancelled.")

