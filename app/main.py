import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from dotenv import load_dotenv

from app.db.base import Base
from app.db.session import engine
from app.utils import verify_jwt_token


# routers
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.routers.product_router import router as product_router
from app.routers.order_router import router as order_router

# Load environment variables
load_dotenv()

# Create DB tables
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI(
    title="Warehouse Management System (WMS)",
    version="1.0.0",
    description="FastAPI backend with JWT authentication"
)

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define protected paths
        protected_paths = ["/orders", "/products"]

        try:
            # Only protect certain paths
            if any(request.url.path.startswith(path) for path in protected_paths):
                auth_header = request.headers.get("Authorization")
                
                if not auth_header or not auth_header.startswith("Bearer "):
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Authorization header missing or invalid"}
                    )

                token = auth_header.split(" ")[1]
                print(1)
                try:
                    payload = verify_jwt_token(token)
                    request.state.user = payload  # store payload for route access
                    print(payload)
                except Exception:
                    print(3)
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Invalid or expired token"}
                    )
                print(2)
            # Proceed to the next middleware / route
            response = await call_next(request)
            return response

        except Exception as exc:
            # Catch any unexpected errors in middleware
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error in authentication middleware"}
            )

app.add_middleware(JWTAuthMiddleware)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)

# Health Check
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "OK", "message": "WMS backend is running"}


if __name__ == "__main__":
    import uvicorn

    workers = int(os.getenv("API_UVICORN_WORKER", 1))
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))

    print(
        f"Starting WMS server with {workers} workers on {host}:{port}"
    )

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        workers=workers,
    )
