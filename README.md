# User Control Flask Web App

A simple user control web application built with Flask. This web app allows users to register, login, and perform basic user management tasks. It includes form validation, user input handling, and both GET and POST request handling.

## Features
- User Registration
- Form Validation (username, first name, last name, and password rules)
- Error and Success Alerts
- Basic User Login
- Responsive Design using Bootstrap

## Prerequisites
Make sure you have the following installed:
- Python 3.x
- Flask (`pip install flask`)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/user-control-flask-web-app.git
    ```
2. **Navigate to the project directory:**
    ```bash
    cd user-control-flask-web-app
    ```
3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the application:**
    ```bash
    python app.py
    ```
5. **Open your web browser and visit:**
    ```
    http://127.0.0.1:5000
    ```

## Usage

### Register
1. Go to the `/register` page.
2. Fill in the registration form.
3. Make sure to follow the validation rules:
   - **Username**: Must start with a letter, contain only lowercase letters, numbers, or underscores.
   - **First and Last Name**: Must be less than 26 characters.
   - **Password**: Must contain at least one uppercase letter, one number, one special character, and be at least 8 characters long.

### Alerts
- An error alert will show if the form submission fails validation.
- A success alert (green) will display when registration is successful.

## File Structure
