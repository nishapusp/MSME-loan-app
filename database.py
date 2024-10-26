import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        # Get MongoDB connection string from environment variable
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client['msme_loan_db']
    
    def save_application(self, application_data):
        """Save loan application data"""
        return self.db.applications.insert_one(application_data)
    
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