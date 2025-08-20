import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),       # Will be 'mysql-db'
    "user": os.getenv("DB_USER"),       # Will be 'root'
    "password": os.getenv("DB_PASSWORD"), # Will be 'password'
    "database": os.getenv("DB_DATABASE")  # Will be 'webapp'
}