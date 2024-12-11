REM FOR WINDOWS
@echo off
SET VENV_DIR=venv

IF NOT EXIST "%VENV_DIR%" (
    echo Virtual environment not found. Creating a new one...
    python -m venv %VENV_DIR%
) ELSE (
    echo Virtual environment found.
)

call %VENV_DIR%\Scripts\activate

IF EXIST "requirements.txt" (
    echo Installing requirements...
    pip install -r requirements.txt
) ELSE (
    echo requirements.txt not found. Skipping package installation.
)

echo Running main.py...
python main.py

deactivate