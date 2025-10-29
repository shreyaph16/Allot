# 🗂️ Allot

**Allot** is a modern, collaborative task management and communication web app built with **React (Vite + TypeScript)** on the frontend and **FastAPI** on the backend.  
It helps teams organize projects, assign tasks, track progress, and chat in real time — all in one interface.

---

## 🚀 Features

- 🧠 Task creation, assignment, and progress tracking  
- 💬 Built-in team chat for project communication  
- 🌙 Light/Dark theme toggle  
- 👥 Manage team members (leader & member roles)  
- ⚡ Fast and reactive frontend (Vite + React + TypeScript)  
- 🧱 Backend powered by FastAPI

---

## 🛠️ Tech Stack

| Area | Technology |
|------|-------------|
| Frontend | React, TypeScript, Vite, Tailwind CSS |
| Backend | FastAPI (Python) |
| UI Components | shadcn/ui, lucide-react |
| Package Manager | npm |
| Server | Uvicorn |

2. Setup and Run Backend (FastAPI)
Create and activate virtual environment
python -m venv venv
venv\Scripts\activate    # On Windows
# or
source venv/bin/activate # On Mac/Linux

Install dependencies
pip install -r backend/requirements.txt

Run the FastAPI server
cd backend
uvicorn main:app --reload --port 8000

Setup and Run Frontend (React + Vite)

In a new terminal (while backend keeps running):

cd frontend
npm install
npm run dev

Your frontend will run at:
http://localhost:5173

Notes

Ensure both backend and frontend servers are running simultaneously.
For first-time setups, allow npm to install dependencies (takes a few minutes).
If you change backend URLs or ports, update your frontend api config accordingly.

📜 License

This project is open source and available under the MIT License

