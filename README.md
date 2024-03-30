### Budget Management System
## Overview
This is a Python application for managing budgets, allowing users to perform various financial transactions such as depositing, withdrawing, transferring between accounts, etc. It uses SQLAlchemy for database management and Passlib for secure password hashing.

## Features
User Authentication: Users can register for new accounts and log in securely.
Main Account Operations: Users can view their main account balance, deposit into it, and withdraw from it.
Budget Account Management: Users can create multiple budget accounts, view their balances, deposit into, withdraw from, transfer between them, and delete them.
Security: Passwords are securely hashed using bcrypt for storage in the database, ensuring user data safety.

## Requirements

Python 3.x
SQLAlchemy
Passlib

## Installation

# Clone the repository:
git clone https://github.com/Ogachi254bank_budget_tracker_marv.git

# Install the required dependencies:

pip install -r requirements.txt

# Run the application:
python init_db.py

python cli.py

## Usage

Upon running the application, you will be prompted with the main menu:
Login: Existing users can log in.
Register: New users can create an account.
Exit: Quit the application.
After logging in, you will be presented with the user menu where you can perform various operations related to your accounts.
Follow the prompts to perform transactions such as viewing balances, depositing, withdrawing, creating budget accounts, managing them, and logging out.
Exit the application when you're done.

## Notes

Ensure you have Python installed on your system.
Make sure to keep your passwords secure and do not share them with anyone.
Always log out when you're finished using the application, especially on shared devices.

## Disclaimer

This application is for educational purposes only. Do not use it for handling real financial transactions without proper security measures and auditing. The developer holds no responsibility for any misuse or damages caused by the application.