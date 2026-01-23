from main import app

# This file is used by Hugging Face Spaces to run the FastAPI application
# The app instance is imported from main.py and can be served by the platform

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)