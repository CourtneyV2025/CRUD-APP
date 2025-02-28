# Your app should store, display, and modify data from an SQLite database. Library System: A database of books with borrowing and returning functionality. 

from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone 

# Create Flask app instance 
app = Flask(__name__) 




