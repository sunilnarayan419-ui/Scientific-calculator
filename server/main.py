from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from solver import solve_math_problem
from models import MathRequest, MathResponse

app = FastAPI(title="Universal Scientific Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Universal Scientific Calculator API is running"}

@app.post("/solve", response_model=MathResponse)
def solve(request: MathRequest):
    return solve_math_problem(request)
