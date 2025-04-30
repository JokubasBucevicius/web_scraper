This project is an AI-powered web scraper with a Streamlit frontend. It allows users to input a website, scrape its content in multiple pages using Selenium, and extract meaningful data using Google's Gemini AI with its free tokens. Currently the project has been only tested on Wikepedia.org and skelbiu.lt websites, so other websites might require some addtional tweaking and some code manipulations or additional tools to counter CAPTCHAS and cookies for example.
---

## Project Overview

- **Language**: Python 3.11
- **Frontend**: Streamlit
- **Scraping**: Selenium (Headless Chrome)
- **Parsing**: Google Generative AI (Gemini)
- **Containerized**: Docker

---

## Project Files

```
main.py          # Streamlit UI
scrape.py        # Selenium scraping + content cleaning
parse.py         # Gemini API parsing logic
requirements.txt # Python dependencies
Dockerfile       # Docker container config
.env             # file where you store your Gemini API key (APIs can be obtained for free in Google AI Studio)
```

---

##  Dockerization Process

### Step 1: Created `requirements.txt`

In this file I have listed all the required libraries to run this project in the current configuration. This project could be used with different LLMs (Ollama, OpenAI, ...) but it requires the installation of the related packages.
```
streamlit
selenium
beautifulsoup4
python-dotenv
google-generativeai
```

---

### Step 2: Wrote the `Dockerfile`
```dockerfile
# Start from a official Python 3.11 image
FROM python:3.11-slim

# Prevents interactive prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# Install required system dependencies:
# - Core tools (wget, curl, unzip, etc.)
# - Google Chrome runtime dependencies (fonts, GTK, libx11, etc.)
# - Chromium driver (needed by Selenium to control Chrome)
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates fonts-liberation \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
    libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils libu2f-udev libvulkan1 \
    libgbm1 libgtk-3-0 libxshmfence1 chromium-driver \
    && rm -rf /var/lib/apt/lists/*  # clean up package cache to reduce image size

# Download and install the latest stable version of Google Chrome
# Needed for headless browsing in Selenium
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb  # cleanup installer

# Set environment variable so Selenium can find Chrome
ENV CHROME_BIN=/usr/bin/google-chrome

# Add Chrome to the system PATH
ENV PATH="${PATH}:/usr/bin/google-chrome"

# Set the working directory inside the container
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Open port 8501 so Streamlit can be accessed from outside the container
EXPOSE 8501

# Define the default command to run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
---

###  Step 3: Built the Docker Image inside the WSL2 using Docker Desktop app for launching the engine.

```bash
docker build -t ai-web-scraper .
```

---

### Step 4: Ran the Container with working API key from .env file

```bash
docker run --env-file .env -p 8501:8501 ai-web-scraper
```

Then accessed it in the browser at: [http://localhost:8501](http://localhost:8501)

---

##  Issues Encountered (and Solved)

### 1. `no chrome binary at /usr/bin/google-chrome`
**Fix**: Installed Google Chrome manually inside the container.

---

### 2. Docker not working in WSL initially
**Fixes**:
- Installed Docker Desktop for Windows
- Enabled WSL2 integration only for `Ubuntu-22.04`
- Ran `wsl --shutdown` to apply group changes after adding user to `docker` group

---

### 3. Docker daemon error: `permission denied`
**Fix**: Ran `sudo usermod -aG docker $USER` and restarted WSL

---

##  Example Use Case for the app

1. Open the app
2. Enter a website URL (e.g. `https://www.skelbiu.lt/skelbimai/1?autocompleted=1&keywords=rtx&cost_min=&cost_max=&type=0&condition=&cities=0&distance=0&mainCity=0&search=1&category_id=4325&user_type=0&ad_since_min=0&ad_since_max=0&visited_page=1&orderBy=-1&detailsSearch=1`) (! Has been heavily tested on this URL in order to find second hand market prices for RTX series GPUs, but it should work with items inside skelbiu.lt, just make sure to reduce the page number to less than 5 otherwise free version on GEMINI AI might not work)
3. Choose "Single Page" or "Multiple Pages"
4. In the prompt, write something like:
   > _"Extract all the article headlines and authors from this page."_
5. Get clean, structured data parsed by Gemini

---

##  Final Thoughts

This project demonstrates how to combine Python automation, AI-powered parsing, and modern devops (Docker) into a single reproducible app. It can be extended to scrape product listings, job posts, academic papers — anything you can describe to Gemini.

---

