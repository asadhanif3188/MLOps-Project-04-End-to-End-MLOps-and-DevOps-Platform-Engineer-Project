from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import time
import random
from faker import Faker
from pydantic import BaseModel

# Initialize Faker and FastAPI
fake = Faker()
app = FastAPI()

# Allow CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for the response
class DataResponse(BaseModel):
    timestamp: int
    user_id: str
    activity: str
    amount: float
    ip_address: str
    device: str
    location: str
    session_duration: int
    label: str

# Function to generate normal data
def generate_normal_data():
    return {
        "timestamp": int(time.time() * 1000),  # Current timestamp in milliseconds
        "user_id": fake.uuid4(),
        "activity": random.choice(["login", "logout", "purchase", "view_item", "add_to_cart"]),
        "amount": round(random.normalvariate(100, 30), 2),  # Normal distribution for amounts
        "ip_address": fake.ipv4(),
        "device": random.choice(["mobile", "desktop", "tablet"]),
        "location": fake.country_code(),
        "session_duration": random.randint(10, 600),  # Session duration in seconds
        "label": "normal"  # Ground truth label
    }

# Function to generate anomalous data
def generate_anomalous_data():
    return {
        "timestamp": int(time.time() * 1000),  # Current timestamp in milliseconds
        "user_id": fake.uuid4(),
        "activity": random.choice(["login", "logout", "purchase", "view_item", "add_to_cart"]),
        "amount": round(random.uniform(1000.0, 10000.0), 2),  # Unusually high amount
        "ip_address": fake.ipv4(),
        "device": random.choice(["mobile", "desktop", "tablet"]),
        "location": fake.country_code(),
        "session_duration": random.randint(0, 10),  # Unusually short session
        "label": "anomalous"  # Ground truth label
    }

# API Endpoints
@app.get("/generate/normal", response_model=DataResponse)
async def generate_normal():
    return generate_normal_data()

@app.get("/generate/anomalous", response_model=DataResponse)
async def generate_anomalous():
    return generate_anomalous_data()

@app.get("/generate", response_model=DataResponse)
async def generate_random():
    if random.random() < 0.9:
        return generate_normal_data()
    else:
        return generate_anomalous_data()