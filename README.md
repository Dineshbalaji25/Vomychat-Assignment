## Linktr Backend with Referral System
## Introduction
This project is a backend implementation for a platform similar to Linktr.ee or Bento.me that includes a referral system. The backend is built using Django and Django REST Framework (DRF) and uses JWT for authentication. The system allows users to register, log in, request password resets, and track referrals. Each user is assigned a unique referral code, and when a new user registers using that code, a referral record is created. Additionally, the project includes security measures such as input validation, password hashing, and protection against common web vulnerabilities.

## Features
User Registration & Authentication
Users can register with a username, email, and password. Duplicate checks and proper validations (e.g., email format, password strength) are in place to ensure data integrity.

## JWT Authentication
On successful login, the API returns both access and refresh tokens, allowing for secure, token-based authentication throughout the application.

## Password Reset
A password reset endpoint sends a reset link to the user's email. This enables users to securely reset their passwords via email verification and token expiration.

## Referral System
Each user is given a unique referral code that they can share. When a new user registers using that referral code, the referral is recorded in the system with details such as the referrer, referred user, date of referral, and status (pending, successful, etc.).

## Optional Rewards
A Rewards model is included to track incentives earned by users who refer others. This feature can be extended to offer credits, free premium features, or other rewards based on referral activity.

## Security Measures
The project implements various security measures including:

CSRF protection
XSS prevention
SQL injection safeguards
Secure password hashing
Scalability Considerations
The system is designed to handle high traffic and large numbers of concurrent users. 


## Repository Clone
To clone the repository, run the following command:

git clone https://github.com/yourusername/linktr-backend.git
cd linktr-backend


## Virtual Environment Setup
Create a virtual environment and activate it:

#Create a virtual environment (using venv)
python -m venv env

#Activate the virtual environment (Windows)
env\Scripts\activate

#Activate the virtual environment (macOS/Linux)
source env/bin/activate

## configure email backend
Django Settings for Email Backend
In your linktr/settings.py, include or update the following email configuration:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'<br>
EMAIL_HOST = 'smtp.gmail.com'<br>
EMAIL_PORT = 587<br>
EMAIL_USE_TLS = True<br>
EMAIL_HOST_USER = youremail@gmail.com<br>
EMAIL_HOST_PASSWORD = "password@1234"

## Create the database
Making Migrations and Migrating the Database
Generate the migration files for the users app and apply them:

python manage.py makemigrations users
python manage.py migrate

## Running the Server
To start the development server, run:

python manage.py runserver
By default, the server will be available at http://127.0.0.1:8000.

## API Endpoints
Once the server is running, you can access the following endpoints:

User Registration:
POST http://127.0.0.1:8000/api/register/<br>
{
  "username": "admin",<br>
  "email": "yourmail@example.com",<br>
  "password": "Password123!",<br>
  "referral_code": "REFERRAL_CODE"
}<br>

User Login:
POST http://127.0.0.1:8000/api/login/<br>
{
  "username_or_email": "newuser",
  "password": "StrongPassword123!"
}<br>

On success, you will receive an access token and a refresh token. Use the access token in the Authorization header (e.g., Authorization: Bearer <your_access_token>) for authenticated requests.

Forgot Password:
POST http://127.0.0.1:8000/api/forgot-password/<br>

{
  "email": "newuser@example.com"
}

List Referrals:
GET http://127.0.0.1:8000/api/referrals/
Requires the Authorization header with your access token.

Referral Statistics:
GET http://127.0.0.1:8000/api/referral-stats/
Requires the Authorization header with your access token.

## How to Use the API Endpoints
<h2>Register a User:</h2>
Send a POST request to /api/register/ with the required JSON payload.<br>
<h2>Login:</h2>
Send a POST request to /api/login/ to receive JWT tokens. Include the access token in the header for subsequent authenticated requests.<br>
<h2>Forgot Password:</h2>
Send a POST request to /api/forgot-password/ with the user's email to receive a password reset link.<br>
<h2>Access Referral Data:</h2>
Use GET requests for /api/referrals/ and /api/referral-stats/ with the proper JWT token in the Authorization header.
