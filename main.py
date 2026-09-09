# ADD THESE LINES:
import contracts, jobs
app.include_router(contracts.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")

# FIX CORS - REPLACE YOUR EXISTING ONE WITH:
# app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import auth, billing, sandbox, contracts, jobs

app = FastAPI(title="NexusAI Core")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router, prefix="/api/v1")
app.include_router(billing.router, prefix="/api/v1")
app.include_router(sandbox.router, prefix="/api/v1")
app.include_router(contracts.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")

@app.get("/api/v1/health")
def health(): return {"status": "healthy", "fee": "10%"}
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all routers
from auth import router as auth_router
from jobs import router as jobs_router
from contracts import router as contracts_router
from billing import router as billing_router

# Try to import sandbox safely (it may have docker dependency)
try:
    from sandbox import router as sandbox_router
        HAS_SANDBOX = True
        except ImportError:
            HAS_SANDBOX = False
                print("⚠️ sandbox.py not loaded - no docker")

                app = FastAPI(
                    title="NexusAI API",
                        description="AI Talent Marketplace - Secure 10% fee escrow",
                            version="1.0.0"
                            )

                            # CORS - allow frontend
                            app.add_middleware(
                                CORSMiddleware,
                                    allow_origins=[
                                            "http://localhost:3000",
                                                    "http://127.0.0.1:3000",
                                                            "http://localhost:3001",
                                                                ],
                                                                    allow_credentials=True,
                                                                        allow_methods=["*"],
                                                                            allow_headers=["*"],
                                                                            )

                                                                            # Mount routers with /api/v1 prefix to match frontend
                                                                            app.include_router(auth_router, prefix="/api/v1")
                                                                            app.include_router(jobs_router, prefix="/api/v1")
                                                                            app.include_router(contracts_router, prefix="/api/v1")
                                                                            app.include_router(billing_router, prefix="/api/v1")

                                                                            if HAS_SANDBOX:
                                                                                app.include_router(sandbox_router, prefix="/api/v1")

                                                                                @app.get("/")
                                                                                async def root():
                                                                                    return {
                                                                                            "status": "NexusAI API running",
                                                                                                    "docs": "/docs",
                                                                                                            "auth": "/api/v1/auth/login",
                                                                                                                    "jobs_search": "/api/v1/jobs/search",
                                                                                                                            "version": "1.0.0 - secure 10% escrow"
                                                                                                                                }

                                                                                                                                @app.get("/health")
                                                                                                                                async def health():
                                                                                                                                    # Quick DB check
                                                                                                                                        try:
                                                                                                                                                import psycopg2
                                                                                                                                                        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
                                                                                                                                                                conn.close()
                                                                                                                                                                        db_status = "connected"
                                                                                                                                                                            except Exception as e:
                                                                                                                                                                                    db_status = f"error: {str(e)}"
                                                                                                                                                                                        return {"api": "ok", "db": db_status, "sandbox": HAS_SANDBOX}

                                                                                                                                                                                        # Run with: uvicorn main:app --reload --port 8000
                                                                                                                                                                                        if __name__ == "__main__":
                                                                                                                                                                                            import uvicorn
                                                                                                                                                                                                uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)