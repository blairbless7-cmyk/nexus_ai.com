#!/bin/bash
mkdir -p backend frontend/components frontend/pages/dashboard

# backend/__init__.py
touch backend/__init__.py

# backend/requirements.txt
cat > backend/requirements.txt <<'REQ'
fastapi==0.110.0
uvicorn[standard]==0.29.0
psycopg2-binary==2.9.9
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.9
stripe==7.8.0
pydantic[email]==2.6.3
python-dotenv==1.0.1
REQ

# backend/Dockerfile
cat > backend/Dockerfile <<'DF'
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt
COPY..
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
DF

# frontend/Dockerfile
cat > frontend/Dockerfile <<'DF'
FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json*./
RUN npm install || npm install --legacy-peer-deps
COPY..
EXPOSE 3000
CMD ["npm", "run", "dev"]
DF

# frontend/package.json (if you don't have one)
if [! -f frontend/package.json ]; then
cat > frontend/package.json <<'PKG'
{
  "name": "nexusai-frontend",
    "version": "1.0.0",
      "scripts": {
          "dev": "next dev -p 3000 -H 0.0.0.0",
              "build": "next build",
                  "start": "next start"
                    },
                      "dependencies": {
                          "next": "14.1.0",
                              "react": "18.2.0",
                                  "react-dom": "18.2.0"
                                    }
                                    }
                                    PKG
                                    fi

                                    #.env
                                    cat >.env <<'ENV'
                                    JWT_SECRET_KEY=super_random_secret_key_change_me_32_chars_min_12345
                                    DATABASE_URL=postgresql://nexus_admin:super_secure_local_dev_password@localhost:5432/nexus_ai_ledger
                                    STRIPE_SECRET_KEY=sk_test_51YourTestKeyHere
                                    STRIPE_WEBHOOK_SECRET=whsec_1YourWebhookSecretHere
                                    ENV

                                    # frontend/.env.local
                                    cat > frontend/.env.local <<'ENV'
                                    NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
                                    ENV

                                    echo "✅ Base files created"
                                    echo "⚠️ Now copy-paste the 8 backend files I gave you earlier (main.py, auth.py, etc) into backend/"
                                    echo "⚠️ And 5 frontend files into frontend/"
                                    echo "Then run: docker-compose up --build -d"