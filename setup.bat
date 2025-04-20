@echo off
echo Starting project setup...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not installed. Please install pip.
    exit /b 1
)

REM Create and activate virtual environment
echo Creating virtual environment...
python -m venv .venv
call .venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    (
        echo DEBUG=True
        echo SECRET_KEY=your-secret-key-here
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo DATABASE_URL=sqlite:///db.sqlite3
        echo EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
        echo DEFAULT_FROM_EMAIL=webmaster@localhost
        echo SERVER_EMAIL=root@localhost
        echo ACCOUNT_EMAIL_REQUIRED=True
        echo ACCOUNT_EMAIL_VERIFICATION=mandatory
        echo ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION=True
        echo ACCOUNT_LOGOUT_ON_GET=True
        echo ACCOUNT_LOGIN_ON_PASSWORD_RESET=True
        echo ACCOUNT_LOGOUT_REDIRECT_URL=/
        echo LOGIN_REDIRECT_URL=/
        echo ACCOUNT_PRESERVE_USERNAME_CASING=False
        echo ACCOUNT_USERNAME_MIN_LENGTH=1
        echo SOCIALACCOUNT_PROVIDERS=^
        echo {^
        echo     'google': {^
        echo         'APP': {^
        echo             'client_id': 'your-google-client-id',^
        echo             'secret': 'your-google-client-secret',^
        echo             'key': ''^
        echo         },^
        echo         'SCOPE': [^
        echo             'profile',^
        echo             'email',^
        echo         ],^
        echo         'AUTH_PARAMS': {^
        echo             'access_type': 'online',^
        echo         }^
        echo     }^
        echo }
    ) > .env
    echo Please update the .env file with your actual configuration values.
)

REM Remove existing database if it exists
echo Cleaning up existing database...
if exist db.sqlite3 del db.sqlite3

REM Make migrations
echo Creating database migrations...
python manage.py makemigrations

REM Apply migrations
echo Applying migrations...
python manage.py migrate

REM Create superuser
echo Creating superuser...
python manage.py createsuperuser

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo Setup completed successfully!
echo You can now run the development server with: python manage.py runserver 