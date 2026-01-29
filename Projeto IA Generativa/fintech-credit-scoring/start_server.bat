@echo off
REM Inicia o servidor Uvicorn em nova janela
start "" "C:\Users\Vitor\AppData\Local\Microsoft\WindowsApps\python3.13.exe" -m uvicorn src.main:app --host 127.0.0.1 --port 8000
echo Servidor iniciado em nova janela. Feche a janela do servidor para parar.
