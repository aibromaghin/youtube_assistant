# Use python as base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy and install all dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files in folder
COPY . .

# Expose port for streamlit
EXPOSE 8501

# Run
CMD ["streamlit", "run", "main.py"]