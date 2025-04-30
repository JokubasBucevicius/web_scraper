FROM python:3.11-slim

# Avoid prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates fonts-liberation \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
    libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils libu2f-udev libvulkan1 \
    libgbm1 libgtk-3-0 libxshmfence1 chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome manually
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/google-chrome
ENV PATH="${PATH}:/usr/bin/google-chrome"

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Start the app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
