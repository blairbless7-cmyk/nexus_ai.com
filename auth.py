import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from jose import jwt, JWTError
from passlib.context import CryptContext

# Config from env - no hardcoded secrets
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY missing in.env")
    DATABASE_URL = os.getenv("DATABASE_URL")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 120

    router = APIRouter(prefix="/auth", tags=["auth"])
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

    # --- Schemas ---
    class UserRegister(BaseModel):
        email: EmailStr
            password: str = Field(min_length=8, max_length=72)
                first_name: str = Field(min_length=1, max_length=100)
                    last_name: str = Field(min_length=1, max_length=100)
                        role: str = Field(pattern="^(enterprise_client|ai_talent)$")
                            country_iso: str = Field(min_length=2, max_length=2)
                                company_name: Optional[str] = None

                                class TokenResponse(BaseModel):
                                    access_token: str
                                        token_type: str = "bearer"
                                            role: str
                                                user_id: str

                                                # --- DB Helper ---
                                                def get_db():
                                                    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
                                                        try:
                                                                yield conn
                                                                    finally:
                                                                            conn.close()

                                                                            def get_password_hash(password: str) -> str:
                                                                                return pwd_context.hash(password)

                                                                                def verify_password(plain: str, hashed: str) -> bool:
                                                                                    return pwd_context.verify(plain, hashed)

                                                                                    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
                                                                                        to_encode = data.copy()
                                                                                            expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
                                                                                                to_encode.update({"exp": expire})
                                                                                                    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

                                                                                                    # --- Routes ---
                                                                                                    @router.post("/register", status_code=201)
                                                                                                    async def register(user: UserRegister):
                                                                                                        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
                                                                                                            cur = conn.cursor()
                                                                                                                try:
                                                                                                                        # Check existing
                                                                                                                                cur.execute("SELECT id FROM users WHERE email = %s", (user.email,))
                                                                                                                                        if cur.fetchone():
                                                                                                                                                    raise HTTPException(status_code=400, detail="Email already registered")

                                                                                                                                                            user_id = str(uuid.uuid4())
                                                                                                                                                                    hashed = get_password_hash(user.password)

                                                                                                                                                                            cur.execute("""
                                                                                                                                                                                        INSERT INTO users (id, email, password_hash, role, first_name, last_name, company_name, country_iso)
                                                                                                                                                                                                    VALUES (%s, %s, %s, %s::user_role, %s, %s, %s, %s)
                                                                                                                                                                                                            """, (user_id, user.email.lower(), hashed, user.role, user.first_name, user.last_name, user.company_name, user.country_iso.upper()))

                                                                                                                                                                                                                    # Create empty talent profile if talent
                                                                                                                                                                                                                            if user.role == 'ai_talent':
                                                                                                                                                                                                                                        cur.execute("""
                                                                                                                                                                                                                                                        INSERT INTO talent_profiles (user_id, skills_tags, bio, years_experience, target_hourly_rate, sandbox_aggregate_score)
                                                                                                                                                                                                                                                                        VALUES (%s, ARRAY[]::TEXT[], '', 0, 0.00, 0.00)
                                                                                                                                                                                                                                                                                    """, (user_id,))

                                                                                                                                                                                                                                                                                            conn.commit()
                                                                                                                                                                                                                                                                                                    return {"status": "profile_provisioned_successfully", "user_id": user_id, "email": user.email, "role": user.role}
                                                                                                                                                                                                                                                                                                        except HTTPException:
                                                                                                                                                                                                                                                                                                                raise
                                                                                                                                                                                                                                                                                                                    except Exception as e:
                                                                                                                                                                                                                                                                                                                            conn.rollback()
                                                                                                                                                                                                                                                                                                                                    raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
                                                                                                                                                                                                                                                                                                                                        finally:
                                                                                                                                                                                                                                                                                                                                                cur.close()
                                                                                                                                                                                                                                                                                                                                                        conn.close()

                                                                                                                                                                                                                                                                                                                                                        @router.post("/login", response_model=TokenResponse)
                                                                                                                                                                                                                                                                                                                                                        async def login(form_data: OAuth2PasswordRequestForm = Depends()):
                                                                                                                                                                                                                                                                                                                                                            conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
                                                                                                                                                                                                                                                                                                                                                                cur = conn.cursor()
                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                            cur.execute("SELECT id, email, password_hash, role FROM users WHERE email = %s", (form_data.username.lower(),))
                                                                                                                                                                                                                                                                                                                                                                                    db_user = cur.fetchone()
                                                                                                                                                                                                                                                                                                                                                                                            if not db_user or not verify_password(form_data.password, db_user['password_hash']):
                                                                                                                                                                                                                                                                                                                                                                                                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

                                                                                                                                                                                                                                                                                                                                                                                                                token = create_access_token({"sub": db_user['email'], "role": db_user['role'], "user_id": str(db_user['id'])})
                                                                                                                                                                                                                                                                                                                                                                                                                        return {"access_token": token, "token_type": "bearer", "role": db_user['role'], "user_id": str(db_user['id'])}
                                                                                                                                                                                                                                                                                                                                                                                                                            finally:
                                                                                                                                                                                                                                                                                                                                                                                                                                    cur.close()
                                                                                                                                                                                                                                                                                                                                                                                                                                            conn.close()

                                                                                                                                                                                                                                                                                                                                                                                                                                            # --- Dependency to protect other routes ---
                                                                                                                                                                                                                                                                                                                                                                                                                                            async def get_current_user(token: str = Depends(oauth2_scheme)):
                                                                                                                                                                                                                                                                                                                                                                                                                                                credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    email: str = payload.get("sub")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            role: str = payload.get("role")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    user_id: str = payload.get("user_id")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if email is None or user_id is None:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        raise credentials_exception
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                return {"email": email, "role": role, "user_id": user_id}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    except JWTError:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            raise credentials_exception

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            @router.get("/me")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            async def me(current_user = Depends(get_current_user)):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                return current_user