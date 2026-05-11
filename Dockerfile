# Stage 1: Build & Dependency Installation
FROM python:3.11-slim AS builder
 
WORKDIR /app
 
# Install uv for fast dependency management
RUN pip install uv
 
# Copy only the dependency files first to leverage Docker cache
COPY pyproject.toml uv.lock requirment.txt ./
 
# Install dependencies into the system path
# We use the requirements file directly to avoid the "package" error
RUN uv pip install --system -r requirment.txt
 
# Copy the data and the script to build the FAISS database
COPY customer_support_tickets.csv create_db.py ./
 
# --- THE FAISS BUILD STEP ---
# This runs DURING the build, so the database is baked into the image
RUN python create_db.py
 
# Stage 2: Final Runtime Image
FROM python:3.11-slim
WORKDIR /app
 
# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
 
# Copy all project files
COPY . .
 
# Copy the FAISS database generated in the builder stage
COPY --from=builder /app/faiss_support_db ./faiss_support_db
 
# Expose ports for both FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501
 
# Default command (starts the backend)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
 
