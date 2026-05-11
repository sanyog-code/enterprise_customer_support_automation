# Stage 1: Build & FAISS Generation
FROM python:3.11-slim AS builder
 
WORKDIR /app
 
# Install build-essential for packages that need to compile code
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
 
# Copy the requirements file
COPY requirment.txt .
 
# Install dependencies into a prefix folder
RUN pip install --no-cache-dir --prefix=/install -r requirment.txt
 
# Copy necessary files to build the database
COPY customer_support_tickets.csv create_db.py ./
 
# Build the FAISS database during the image build
RUN python create_db.py
 
# Stage 2: Final Runtime Image
FROM python:3.11-slim
WORKDIR /app
 
# Copy libraries from the builder
COPY --from=builder /install /usr/local
 
# Copy your source code and config
COPY . .
 
# Ensure the FAISS database is copied over
COPY --from=builder /app/faiss_support_db ./faiss_support_db
 
# Expose ports for Backend and Frontend
EXPOSE 8000
EXPOSE 8501
 
# Start the Backend by default
CMD ["uvicorn", "api.py:app", "--host", "0.0.0.0", "--port", "8000"]
  
