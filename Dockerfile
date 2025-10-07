# Use Python 3.13 slim base
FROM python:3.13-slim

# Install required system packages for GUI (updated for Debian trixie)
RUN apt-get update && \
    apt-get install -y \
    python3-tk \
    tcl8.6-dev tk8.6-dev \
    libx11-dev \
    libgl1 \
    libglib2.0-0 \
    libxrender1 \
    libxext6 \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*


# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Environment variable to show GUI
ENV DISPLAY=:0

# Default command to run the main app
CMD ["python", "main.py"]
