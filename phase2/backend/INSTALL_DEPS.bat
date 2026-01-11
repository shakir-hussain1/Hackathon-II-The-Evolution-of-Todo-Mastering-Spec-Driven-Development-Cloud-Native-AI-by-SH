@echo off
echo Installing Python dependencies...
echo.

cd /d "%~dp0"

venv\Scripts\pip install fastapi>=0.110.0
venv\Scripts\pip install uvicorn>=0.27.0
venv\Scripts\pip install sqlmodel>=0.0.14
venv\Scripts\pip install sqlalchemy>=2.0.25
venv\Scripts\pip install psycopg2-binary>=2.9.0
venv\Scripts\pip install PyJWT>=2.8.0
venv\Scripts\pip install pydantic>=2.5.0
venv\Scripts\pip install pydantic-settings>=2.1.0
venv\Scripts\pip install python-dotenv>=1.0.0
venv\Scripts\pip install python-multipart>=0.0.6
venv\Scripts\pip install typing-extensions>=4.9.0
venv\Scripts\pip install passlib>=1.7.4
venv\Scripts\pip install "bcrypt>=4.0.0,<5.0.0"

echo.
echo ====================================
echo Dependencies installed successfully!
echo ====================================
echo.
pause
