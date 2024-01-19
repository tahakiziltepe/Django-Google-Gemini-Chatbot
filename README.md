# Gemini with Prompt!

Create your own chat environment and define a prompt! People can register on this site and chat with Gemini, influenced of course by the prompt you define!
Be careful about that this project use multi-turn chat system. Therefore, make sure last message from 🤖🤖 Bot! (If not, you can delete your last message.)

## Features

- Login/Logout/Register
- Staff members can add/modify prompts. (Superusers can talk to bot without affecting by prompt.)
- To be able to delete one message or clear entire chat history
- Markdowned special text, codes etc.


## Usage

Create a virtual environment

    python -m venv /path/to/new/virtual/environment

Activate virtual environment  
MacOS:

    source venv/bin/activate

for Windows PowerShell

    <venv_path>\Scripts\Activate.ps1  

Install dependencies 

    pip install -r requirements.txt

Migrate database  

    python manage.py makemigrations
    python manage.py migrate

Create admin user. Needed if you want to use Admin dashboard.

    python manage.py createsuperuser

Start server, port number is optional, default is 8000

    python manage.py runserver
