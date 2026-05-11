# Stage 1: Build & FAISS Generation
FROM python:3.11-slim AS builder
 
WORKDIR /app
 
# Install build dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
 
# 1. Create a virtual environment
RUN python -m venv /opt/venv
 
# 2. Activate the virtual environment for all future commands
ENV PATH="/opt/venv/bin:$PATH"
 
# Copy and install requirements (This installs INTO the venv)
COPY requirment.txt .
RUN pip install --no-cache-dir -r requirment.txt
 
# Copy data and build script
COPY customer_support_tickets.csv create_db.py ./
 
# Build the database (Python now sees pandas perfectly!)
RUN python create_db.py
 
# Stage 2: Final Runtime Image
FROM python:3.11-slim
WORKDIR /app
 
# Copy the entire virtual environment from the builder
COPY --from=builder /opt/venv /opt/venv
 
# Activate the virtual environment in the final image
ENV PATH="/opt/venv/bin:$PATH"
 
# Copy your source code
COPY . .
 
# Copy the FAISS database generated in the builder stage
COPY --from=builder /app/faiss_support_db ./faiss_support_db
 
# Expose ports for Backend and Frontend
EXPOSE 8000
EXPOSE 8501
 
# Start the Backend (Make sure it's api:app, not api.py:app)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
   
