# config.py
import os

class Config:
    SECRET_KEY = 'your-secret-key-2025-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///defect_tracking.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False