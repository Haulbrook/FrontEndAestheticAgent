"""
Firebase configuration for multi-user trip collaboration.

This module handles Firebase Firestore integration for sharing trips between multiple users.
Falls back to local storage if Firebase is not configured.
"""

import os
import json
from typing import Optional, Dict, Any
import streamlit as st

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    firebase_admin = None
    credentials = None
    firestore = None


class FirebaseManager:
    """Manages Firebase Firestore operations for trip data"""

    def __init__(self):
        self.db = None
        self.enabled = False
        self._initialize()

    def _initialize(self):
        """Initialize Firebase if credentials are available"""
        if not FIREBASE_AVAILABLE:
            return

        try:
            # Check if already initialized
            if len(firebase_admin._apps) > 0:
                self.db = firestore.client()
                self.enabled = True
                return

            # Try to get credentials from Streamlit secrets
            firebase_creds = None
            try:
                if 'firebase' in st.secrets:
                    # Convert Streamlit secrets to dictionary
                    firebase_creds = {
                        'type': st.secrets['firebase'].get('type'),
                        'project_id': st.secrets['firebase'].get('project_id'),
                        'private_key_id': st.secrets['firebase'].get('private_key_id'),
                        'private_key': st.secrets['firebase'].get('private_key'),
                        'client_email': st.secrets['firebase'].get('client_email'),
                        'client_id': st.secrets['firebase'].get('client_id'),
                        'auth_uri': st.secrets['firebase'].get('auth_uri'),
                        'token_uri': st.secrets['firebase'].get('token_uri'),
                        'auth_provider_x509_cert_url': st.secrets['firebase'].get('auth_provider_x509_cert_url'),
                        'client_x509_cert_url': st.secrets['firebase'].get('client_x509_cert_url'),
                        'universe_domain': st.secrets['firebase'].get('universe_domain', 'googleapis.com')
                    }
                    # Verify we have the required fields
                    if not firebase_creds.get('project_id') or not firebase_creds.get('private_key'):
                        firebase_creds = None
            except Exception as e:
                print(f"Error reading Streamlit secrets: {e}")
                firebase_creds = None

            # Fall back to environment variable
            if not firebase_creds:
                firebase_creds_json = os.getenv('FIREBASE_CREDENTIALS')
                if firebase_creds_json:
                    firebase_creds = json.loads(firebase_creds_json)

            # Initialize Firebase if we have credentials
            if firebase_creds:
                cred = credentials.Certificate(firebase_creds)
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.enabled = True
                print("Firebase initialized successfully!")
            else:
                print("No Firebase credentials found")
        except Exception as e:
            print(f"Firebase initialization failed: {e}")
            import traceback
            traceback.print_exc()
            self.enabled = False

    def is_enabled(self) -> bool:
        """Check if Firebase is enabled and configured"""
        return self.enabled and self.db is not None

    def save_trip(self, trip_code: str, trip_data: Dict[str, Any]) -> bool:
        """
        Save trip data to Firebase

        Args:
            trip_code: Unique trip identifier
            trip_data: Dictionary containing trip details, checklist, ideas, etc.

        Returns:
            True if successful, False otherwise
        """
        if not self.is_enabled():
            return False

        try:
            # Convert trip_data to JSON-serializable format
            serializable_data = self._prepare_for_firestore(trip_data)

            # Save to Firestore
            doc_ref = self.db.collection('trips').document(trip_code)
            doc_ref.set(serializable_data)
            return True
        except Exception as e:
            print(f"Error saving to Firebase: {e}")
            return False

    def load_trip(self, trip_code: str) -> Optional[Dict[str, Any]]:
        """
        Load trip data from Firebase

        Args:
            trip_code: Unique trip identifier

        Returns:
            Dictionary with trip data or None if not found
        """
        if not self.is_enabled():
            return None

        try:
            doc_ref = self.db.collection('trips').document(trip_code)
            doc = doc_ref.get()

            if doc.exists:
                return self._prepare_from_firestore(doc.to_dict())
            return None
        except Exception as e:
            print(f"Error loading from Firebase: {e}")
            return None

    def trip_exists(self, trip_code: str) -> bool:
        """
        Check if a trip exists in Firebase

        Args:
            trip_code: Unique trip identifier

        Returns:
            True if trip exists, False otherwise
        """
        if not self.is_enabled():
            return False

        try:
            doc_ref = self.db.collection('trips').document(trip_code)
            doc = doc_ref.get()
            return doc.exists
        except Exception as e:
            print(f"Error checking trip existence: {e}")
            return False

    def _prepare_for_firestore(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert data to Firestore-compatible format

        Handles:
        - Pydantic models -> dictionaries
        - Sets -> lists
        - Datetime objects -> ISO strings
        """
        from src.models.trip_data import TripDetails, ChecklistItem, IdeaSuggestion
        from datetime import datetime

        serializable = {}

        for key, value in data.items():
            if value is None:
                serializable[key] = None
            elif isinstance(value, TripDetails):
                serializable[key] = value.model_dump(mode='json')
            elif isinstance(value, list):
                # Handle lists of Pydantic models or regular items
                serializable[key] = [
                    item.model_dump(mode='json') if hasattr(item, 'model_dump')
                    else item
                    for item in value
                ]
            elif isinstance(value, set):
                serializable[key] = list(value)
            elif isinstance(value, datetime):
                serializable[key] = value.isoformat()
            else:
                serializable[key] = value

        return serializable

    def _prepare_from_firestore(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert Firestore data back to application format

        Handles:
        - Dictionaries -> Pydantic models
        - Lists -> sets (for rejected_items)
        """
        from src.models.trip_data import TripDetails, ChecklistItem, IdeaSuggestion

        prepared = {}

        for key, value in data.items():
            if key == 'trip_details' and value:
                prepared[key] = TripDetails(**value)
            elif key == 'checklist' and value:
                prepared[key] = [ChecklistItem(**item) for item in value]
            elif key == 'ideas' and value:
                prepared[key] = [IdeaSuggestion(**item) for item in value]
            elif key == 'rejected_items' and value:
                prepared[key] = set(value)
            else:
                prepared[key] = value

        return prepared


# Global instance
_firebase_manager = None

def get_firebase_manager() -> FirebaseManager:
    """Get or create the global Firebase manager instance"""
    global _firebase_manager
    if _firebase_manager is None:
        _firebase_manager = FirebaseManager()
    return _firebase_manager
