# This is a placeholder Dockerfile for the project root.
# Depending on your deployment strategy, you may want to build the frontend, backend, or both.

# Example for a Node.js Frontend:
# FROM node:18-alpine AS builder
# WORKDIR /app
# COPY frontend/package*.json ./
# RUN npm install
# COPY frontend/ ./
# RUN npm run build

# Example for a Python Backend:
FROM python:3.11-slim
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
CMD ["python", "app/main.py"]
