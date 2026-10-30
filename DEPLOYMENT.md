# 🚀 Deployment Guide: Online Interview Questions Generator

This package contains everything needed to deploy the **CogniHire: Online Interview Questions Generator** to any cloud platform, container service, or server.

---

## 🌟 Method 1: Streamlit Community Cloud (Recommended & 100% Free)

Streamlit Community Cloud is the fastest and easiest way to deploy this app online with zero server management.

### Steps:
1. **Unzip** this project and push the files to a new repository on your **GitHub** account (e.g. `github.com/your-username/online-interview-questions-generator`).
2. Go to **[share.streamlit.io](https://share.streamlit.io/)** and sign in with your GitHub account.
3. Click **"New app"**.
4. Select your repository, branch (`main`), and set **Main file path** to:
   ```
   app.py
   ```
5. Click **"Deploy!"**.
6. The platform will automatically read `requirements.txt` and `nltk.txt`, install dependencies, and launch your live public URL within 2 minutes!

---

## 🤗 Method 2: Hugging Face Spaces (Free Streamlit Hosting)

1. Go to **[huggingface.co/spaces](https://huggingface.co/spaces)** and click **"Create new Space"**.
2. Give your space a name (e.g. `interview-question-generator`).
3. Select **Streamlit** as the Space SDK.
4. Set license to `mit` and visibility to `Public`.
5. Upload all the files from this unzipped folder into your Space repository.
6. Hugging Face will automatically build and serve the application!

---

## 🐳 Method 3: Docker Deployment (Local or Any Cloud VPS)

The project includes a production-ready `Dockerfile` and `docker-compose.yml`.

### Option A: Using Docker Compose
```bash
docker-compose up --build -d
```
Visit `http://localhost:8501` in your browser.

### Option B: Using Plain Docker CLI
```bash
# 1. Build the Docker image
docker build -t cognihire-app:latest .

# 2. Run the container
docker run -d -p 8501:8501 --name cognihire cognihire-app:latest
```
Access the application at `http://localhost:8501`.

---

## ⚡ Method 4: Render / Railway Deployment

### On Render (render.com):
1. Connect your GitHub repository to Render.
2. Select **"Web Service"**.
3. Choose **Python 3** environment (or **Docker**).
4. For Python environment:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Click **"Create Web Service"**.

---

## ☁️ Method 5: AWS App Runner / Google Cloud Run (Serverless Container)

Because a `Dockerfile` is included:
1. Push the Docker image to AWS ECR or Google Artifact Registry:
   ```bash
   docker build -t your-registry/cognihire-app:latest .
   docker push your-registry/cognihire-app:latest
   ```
2. In AWS App Runner or Google Cloud Run, create a service pointing to that image.
3. Set the container port to `8501`.

---

## 💻 Method 6: Local Quick Run

If running locally on your computer:
- **Windows**: Double-click `run.bat` or run `.\run.ps1` in PowerShell.
- **Mac / Linux**:
  ```bash
  pip install -r requirements.txt
  streamlit run app.py
  ```

---

## 📁 Package Contents Summary

- `app.py`: Streamlit multi-tab dashboard entry point
- `requirements.txt`: Python package requirements
- `nltk.txt`: NLTK corpora definitions for Streamlit Cloud
- `.streamlit/config.toml`: Production theme & server configuration
- `Dockerfile` & `docker-compose.yml`: Containerization definitions
- `Procfile` & `runtime.txt`: PaaS deployment configuration (Render/Heroku)
- `core/`: NLP engine, question generator, resume analyzer, answer evaluator
- `tests/`: Automated unit test suite
- `run.bat` & `run.ps1`: One-click local launch scripts
