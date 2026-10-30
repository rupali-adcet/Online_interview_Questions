Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Starting CogniHire: Online Interview Questions Generator (NLP)" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Set-Location -Path $PSScriptRoot
streamlit run app.py
