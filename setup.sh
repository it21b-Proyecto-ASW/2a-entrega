#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting project setup...${NC}"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${RED}Python is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo -e "${RED}pip is not installed. Please install pip.${NC}"
    exit 1
fi

# Create and activate virtual environment
echo -e "${GREEN}Creating virtual environment...${NC}"
python -m venv .venv
source .venv/Scripts/activate  # For Windows
# source .venv/bin/activate  # For Linux/Mac

# Install requirements
echo -e "${GREEN}Installing requirements...${NC}"
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${GREEN}Creating .env file...${NC}"
    cat > .env << EOL
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=webmaster@localhost
SERVER_EMAIL=root@localhost
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_EMAIL_VERIFICATION=mandatory
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION=True
ACCOUNT_LOGOUT_ON_GET=True
ACCOUNT_LOGIN_ON_PASSWORD_RESET=True
ACCOUNT_LOGOUT_REDIRECT_URL=/
LOGIN_REDIRECT_URL=/
ACCOUNT_PRESERVE_USERNAME_CASING=False
ACCOUNT_USERNAME_MIN_LENGTH=1
SOCIALACCOUNT_PROVIDERS={
    'google': {
        'APP': {
            'client_id': 'your-google-client-id',
            'secret': 'your-google-client-secret',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
EOL
    echo -e "${GREEN}Please update the .env file with your actual configuration values.${NC}"
fi

# Remove existing database if it exists
echo -e "${GREEN}Cleaning up existing database...${NC}"
rm -f db.sqlite3

# Make migrations
echo -e "${GREEN}Creating database migrations...${NC}"
python manage.py makemigrations

# Apply migrations
echo -e "${GREEN}Applying migrations...${NC}"
python manage.py migrate

# Create superuser
echo -e "${GREEN}Creating superuser...${NC}"
python manage.py createsuperuser

# Collect static files
echo -e "${GREEN}Collecting static files...${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${GREEN}You can now run the development server with: python manage.py runserver${NC}" 