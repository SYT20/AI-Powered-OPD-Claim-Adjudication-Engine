import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Detect if running in production (Render sets RENDER=true)
    is_production = os.environ.get("RENDER") is not None
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=not is_production  # Disable reload in production
    )
