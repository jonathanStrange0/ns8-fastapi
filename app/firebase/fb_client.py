import firebase_admin
import os
from firebase_admin import credentials
from google.cloud import firestore
from google.cloud.firestore_v1.field_path import FieldPath

cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred)
db = firestore.Client()


def fb_client():
    return db
