@echo off
title CogniHire - Online Interview Questions Generator (NLP)
color 0B

echo ===============================================================================
echo                COGNIONE: INTERVIEW QUESTIONS GENERATOR (NLP)
echo ===============================================================================
echo.
echo [*] Initializing NLP Dashboard...
echo [*] Setting working directory...

cd /d "%~dp0"

echo [*] Launching Streamlit web application...
echo [*] URL: http://localhost:8501
echo.
echo ===============================================================================
echo  If the browser does not open automatically, open your browser and go to:
echo  http://localhost:8501
echo ===============================================================================
echo.

python -m streamlit run app.py --server.headless=false

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] An error occurred while launching the application.
    echo [!] Error code: %ERRORLEVEL%
    pause
)
