@echo off
echo Smart Recipe Application Setup
echo ===========================
echo.

REM Check for Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8+.
    exit /b
)

REM Check for virtual environment
if not exist venv\ (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate && pip install -r requirements.txt

REM Prompt for MongoDB Atlas connection string
set /p MONGODB_URI="Enter your MongoDB Atlas connection string: "
if "%MONGODB_URI%"=="" (
    echo MongoDB Atlas connection string is required.
    exit /b
)

REM Prompt for Voyage AI API key
set /p VOYAGE_API_KEY="Enter your Voyage AI API key: "
if "%VOYAGE_API_KEY%"=="" (
    echo Voyage AI API key is required.
    exit /b
)

REM Prompt for Google Gemini API key
set /p GEMINI_API_KEY="Enter your Google Gemini API key: "
if "%GEMINI_API_KEY%"=="" (
    echo Google Gemini API key is required.
    exit /b
)

REM Create .env file
echo Creating .env file with your API keys...
(
echo # MongoDB Atlas Connection
echo MONGODB_URI=%MONGODB_URI%
echo.
echo # VoyageAI API Key
echo VOYAGE_API_KEY=%VOYAGE_API_KEY%
echo.
echo # Google Gemini API Key
echo GEMINI_API_KEY=%GEMINI_API_KEY%
) > .env

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Ask to create superuser
set /p CREATE_SUPERUSER="Do you want to create a superuser? (y/n): "
if /i "%CREATE_SUPERUSER%"=="y" (
    python manage.py createsuperuser
)

REM Ask to load sample data
set /p LOAD_SAMPLE_DATA="Do you want to load sample recipe data? (y/n): "
if /i "%LOAD_SAMPLE_DATA%"=="y" (
    python load_sample_data.py
)

echo.
echo Setup complete! You can now run the server with:
echo python manage.py runserver
echo.
echo Then visit http://127.0.0.1:8000 in your browser.
