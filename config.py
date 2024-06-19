# config.py

import os

class Config:
    MONGO_URI = 'mongodb://localhost:27017/library_management'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
