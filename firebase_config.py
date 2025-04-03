import firebase_admin
from firebase_admin import credentials, firestore

# Path to Firebase credentials JSON file (Replace with your actual file path)
cred_path = "firebase-creditionals.json"

def initialize_firebase():
    try:
        # Check if Firebase app is already initialized
        firebase_admin.get_app()
    except ValueError:
        # Initialize the app with credentials
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            return None
    
    return firestore.client()

# Initialize Firestore DB
db = initialize_firebase()
