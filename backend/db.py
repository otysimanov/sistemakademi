import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

firebaseConfig = {
    'apiKey': "AIzaSyAfQ0aHfYQyb8kMHfTLCXMRwqXnIqJ4BhE",
    'authDomain': "siakad-21.firebaseapp.com",
    'databaseURL': "https://siakad-21-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "siakad-21",
    'storageBucket': "siakad-21.appspot.com",
    'messagingSenderId': "716402688988",
    'appId': "1:716402688988:web:8d61ef31068ac64344c519"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()