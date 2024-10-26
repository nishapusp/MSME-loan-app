import os
from pymongo import MongoClient
import urllib.parse
import streamlit as st
import certifi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    class Database:
    def __init__(self):
        try:
            # URL encode the username and password
            username = urllib.parse.quote_plus("puspendersharma")
            password = urllib.parse.quote_plus("unionbank")
            
            # Construct the connection string with encoded credentials
            connection_string = f"mongodb+srv://{username}:{password}@msme-loan-app.a0gwq.mongodb.net/msme_loan_db?retryWrites=true&w=majority"
            
            # Try getting connection string from Streamlit secrets first
            if hasattr(st, "secrets"):
                connection_string = st.secrets.get("MONGODB_URI", connection_string)
            # Fall back to environment variable if available
            elif os.getenv('MONGODB_URI'):
                connection_string = os.getenv('MONGODB_URI')
            
            # Add SSL configuration and certifi certificate
            self.client = MongoClient(
                connection_string,
                tls=True,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000
            )
            
            # Test the connection
            self.client.admin.command('ping')
            
            self.db = self.client['msme_loan_db']
            print("Database connection successful!")
            
        except Exception as e:
            error_msg = f"Database connection error: {str(e)}"
            print(error_msg)  # Print to console for debugging
            st.error(error_msg)
            raise e

    def save_application(self, application_data):
        """Save loan application data"""
        try:
            result = self.db.applications.insert_one(application_data)
            return result
        except Exception as e:
            st.error(f"Error saving application: {str(e)}")
            return None
    
    def update_application(self, application_id, updated_data):
        """Update existing application"""
        return self.db.applications.update_one(
            {'_id': application_id},
            {'$set': updated_data}
        )
    
    def get_application(self, application_id):
        """Retrieve specific application"""
        return self.db.applications.find_one({'_id': application_id})
    
    def get_all_applications(self):
        """Retrieve all applications"""
        return list(self.db.applications.find())
    
    def save_document(self, document_data):
        """Save uploaded document information"""
        return self.db.documents.insert_one(document_data)
    
    def get_documents(self, application_id):
        """Get all documents for an application"""
        return list(self.db.documents.find({'application_id': application_id}))
