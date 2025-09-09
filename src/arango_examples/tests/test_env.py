import os
from dotenv import load_dotenv

load_dotenv()

print("Environment variables:")
print(f"GOOGLE_APPLICATION_CREDENTIALS = {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
print(f"File exists: {os.path.exists(os.getenv('GOOGLE_APPLICATION_CREDENTIALS', ''))}")
print(f"ARANGO_USER = {os.getenv('ARANGO_USER')}")
print(f"ARANGO_PASSWORD = {os.getenv('ARANGO_PASSWORD')}")