from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fuzzy_logic import compute_cycle_time
from database import init_db, save_history, get_history
import uvicorn

app = FastAPI(title="Fuzzy Logic Washing Machine API")

# Allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Since it's local, we allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the SQLite database table when starting
init_db()

# Request model for prediction
class WashingRequest(BaseModel):
    dirt_level: float
    load_size: float

# Response model
class WashingResponse(BaseModel):
    cycle_time: float
    message: str

@app.post("/predict", response_model=WashingResponse)
def predict_cycle_time(req: WashingRequest):
    # Validate inputs
    if not (0 <= req.dirt_level <= 100) or not (0 <= req.load_size <= 100):
        raise HTTPException(status_code=400, detail="Dirt level and load size must be between 0 and 100")
    
    # Process inputs through fuzzy logic
    time_result = compute_cycle_time(req.dirt_level, req.load_size)
    
    # Save the calculation in the database
    save_history(req.dirt_level, req.load_size, time_result)
    
    return WashingResponse(
        cycle_time=time_result,
        message=f"Calculated cycle time: {time_result} minutes"
    )

@app.get("/history")
def history():
    return get_history()

if __name__ == "__main__":
    print("Starting up the Fuzzy Logic Backend Server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
