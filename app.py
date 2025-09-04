from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get configuration from environment variables
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('FLASK_ENV') != 'production'

if not OPENROUTER_API_KEY:
    print("⚠️ Warning: OPENROUTER_API_KEY environment variable not set!")

