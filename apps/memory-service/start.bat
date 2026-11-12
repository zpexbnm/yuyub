@echo off
rem memory-service launcher: wait for ollama, then start hidden
set MEM_EMBED_URL=http://127.0.0.1:11434/v1/embeddings
set MEM_EMBED_MODEL=bge-m3
set MEM_HOST=127.0.0.1
set MEM_PORT=8790
cd /d "%~dp0"

set /a n=0
:wait
powershell -NoProfile -Command "try{(Invoke-RestMethod -Uri http://127.0.0.1:11434/api/tags -TimeoutSec 3) | Out-Null; exit 0}catch{exit 1}" >nul 2>&1
if errorlevel 1 (
  set /a n+=1
  if %n% geq 40 goto startnow
  timeout /t 3 /nobreak >nul
  goto wait
)

:startnow
start "" /b "C:\Users\w2423\AppData\Local\Microsoft\WindowsApps\pythonw.exe" "%~dp0memory_service.py"