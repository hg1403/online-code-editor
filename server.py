from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body structure
class CodeRequest(BaseModel):
    language: str
    code: str

# Function to execute code based on language
def run_code(language: str, code: str):
    try:
        if language == "python":
            result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=5)
        elif language == "javascript":
            result = subprocess.run(["node", "-e", code], capture_output=True, text=True, timeout=5)
        else:
            return {"error": "Unsupported language"}

        return {"output": result.stdout if result.stdout else result.stderr}
    except Exception as e:
        return {"error": str(e)}

# Default root endpoint to check if server is running
@app.get("/")
def read_root():
    return {"message": "FastAPI server is running!"}

# API endpoint to execute code
@app.post("/run")
async def execute_code(request: CodeRequest):
    return run_code(request.language, request.code)
