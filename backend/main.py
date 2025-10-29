# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import os
from pathlib import Path

app = FastAPI(title="TaskFlow API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple JSON file storage
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "users": [],
        "teams": [],
        "tasks": [],
        "messages": []
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_id():
    return int(datetime.now().timestamp() * 1000)

# Auth Routes
@app.post("/api/auth/register")
def register(data: dict):
    all_data = load_data()
    
    # Check if user exists
    if any(u["email"] == data["email"] for u in all_data["users"]):
        return {"error": "Email already exists"}, 400
    
    user = {
        "id": str(generate_id()),
        "name": data.get("name", ""),
        "email": data["email"],
        "password": data["password"],
        "role": data.get("role", "member")
    }
    
    all_data["users"].append(user)
    save_data(all_data)
    
    return {
        "access_token": f"token_{user['id']}",
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

@app.post("/api/auth/login")
def login(data: dict):
    all_data = load_data()
    
    user = None
    for u in all_data["users"]:
        if u["email"] == data["email"] and u["password"] == data["password"]:
            user = u
            break
    
    if not user:
        return {"error": "Invalid credentials"}, 401
    
    return {
        "access_token": f"token_{user['id']}",
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

# Teams Routes
@app.post("/api/teams")
def create_team(data: dict):
    all_data = load_data()
    
    team = {
        "id": str(generate_id()),
        "name": data.get("name", ""),
        "leader_id": data.get("leader_id", ""),
        "members": [data.get("leader_id", "")]
    }
    
    all_data["teams"].append(team)
    save_data(all_data)
    
    return team

@app.get("/api/teams")
def get_teams(leader_id: str = None):
    all_data = load_data()
    
    if leader_id:
        teams = [t for t in all_data["teams"] if t.get("leader_id") == leader_id]
    else:
        teams = all_data["teams"]
    
    return teams

@app.post("/api/teams/{team_id}/members/{user_email}")
def add_team_member(team_id: str, user_email: str):
    all_data = load_data()
    
    # Find user
    user = None
    for u in all_data["users"]:
        if u["email"] == user_email:
            user = u
            break
    
    if not user:
        return {"error": "User not found"}, 404
    
    # Find team and add member
    for team in all_data["teams"]:
        if team["id"] == team_id:
            if user["id"] not in team.get("members", []):
                team.setdefault("members", []).append(user["id"])
            save_data(all_data)
            return {"message": "Member added"}
    
    return {"error": "Team not found"}, 404

# Tasks Routes
@app.post("/api/tasks")
def create_task(data: dict):
    all_data = load_data()
    
    task = {
        "id": str(generate_id()),
        "title": data.get("title", ""),
        "description": data.get("description", ""),
        "assigned_to": data.get("assigned_to", ""),
        "assigned_by": data.get("assigned_by", ""),
        "deadline": data.get("deadline", ""),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updates": []
    }
    
    all_data["tasks"].append(task)
    save_data(all_data)
    
    return task

@app.get("/api/tasks")
def get_tasks(team_id: str = None):
    all_data = load_data()
    return all_data["tasks"]

@app.patch("/api/tasks/{task_id}")
def update_task(task_id: str, data: dict):
    all_data = load_data()
    
    for task in all_data["tasks"]:
        if task["id"] == task_id:
            if "status" in data:
                task["status"] = data["status"]
            save_data(all_data)
            return task
    
    return {"error": "Task not found"}, 404

@app.post("/api/tasks/{task_id}/updates")
def add_task_update(task_id: str, data: dict):
    all_data = load_data()
    
    for task in all_data["tasks"]:
        if task["id"] == task_id:
            update = {
                "id": str(generate_id()),
                "message": data.get("message", ""),
                "sent_by": data.get("sent_by", ""),
                "sent_at": datetime.now().isoformat()
            }
            task.setdefault("updates", []).append(update)
            save_data(all_data)
            return update
    
    return {"error": "Task not found"}, 404

# Messages Routes
@app.post("/api/messages")
def create_message(data: dict):
    all_data = load_data()
    
    message = {
        "id": str(generate_id()),
        "sender_id": data.get("sender_id", ""),
        "content": data.get("content", ""),
        "timestamp": datetime.now().isoformat(),
        "chat_type": data.get("chat_type", "project"),
        "recipient_id": data.get("recipient_id")
    }
    
    all_data["messages"].append(message)
    save_data(all_data)
    
    return message

@app.get("/api/messages")
def get_messages():
    all_data = load_data()
    return all_data["messages"]

# Health check
@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "TaskFlow API is running"}