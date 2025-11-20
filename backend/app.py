from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from response_generator import generate_response

app = FastAPI()

# CORS: allow common local dev origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
    ],
    allow_credentials=False,   # keep False if using wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.post("/get-response")
async def get_response(payload: dict, request: Request):
    """
    Expects JSON: {"text": "user's text here"}
    Returns: {"response": "..."}
    """
    try:
        text = payload.get("text", "")
        if not isinstance(text, str):
            return {"response": "Invalid input."}
        reply = generate_response(text)
        return {"response": reply}
    except Exception as e:
        # Return a safe message; log the exception server-side
        # (uvicorn will print the exception traceback)
        return {"response": f"Server error: {e}"}
