# FuzzyWash™: AI-Powered Cycle Time Predictor

![Fuzzy Logic](https://img.shields.io/badge/Logic-Fuzzy-blue.svg)
![React](https://img.shields.io/badge/Frontend-React-61dafb.svg)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)

FuzzyWash is a modern web application that calculates the optimal washing machine cycle time based on Dirt Level and Load Size using Mathematical Fuzzy Logic.

## Architecture

This project is built using a clean, modern, separated architecture:

1. **Frontend**: React.js with Vite, using elegant Vanilla CSS and smooth layout animations.
2. **Backend**: Python FastAPI with `scikit-fuzzy` to process inputs through Mamdani fuzzy inference rules.
3. **Database**: Lightweight SQLite keeping track of your calculation history.
4. **MATLAB**: A native `.m` file (`matlab_files/washing_machine_fuzzy.m`) for academic representation including 3D Surface diagrams.

## Features

- Interactive frontend UI
- Modular backend (Python)
- Fuzzy inference system
- Real-time prediction

## How to Run Locally

### 1. Start the Backend
Open a terminal in the `backend` folder and run:
```bash
pip install -r requirements.txt
python main.py
```
*Server will start on http://127.0.0.1:8000*

### 2. Start the Frontend
Open a terminal in the `frontend` folder and run:
```bash
npm install
npm run dev
```
*Frontend will be accessible at http://localhost:5173*

## Fuzzy Logic Rules Implemented
- IF Dirt is Low AND Load is Small THEN Time is Short
- IF Dirt is Medium AND Load is Large THEN Time is Long
- *(and 7 other rules ensuring smooth outputs!)*
