import google.generativeai as genai
from .models import *
import os
from dotenv import load_dotenv

load_dotenv()

def generate_content_bot(msg):
    i = 0
    while 1 == 1:
        try:
            print("utils -> Trying...")
            genai.configure(api_key=str(os.getenv('GOOGLE_API_KEY')))
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(msg)
            yanit = response.text
            print(yanit)
            return yanit.replace('•', '  *')
        except ValueError:
            i = i + 1
            print("utils -> Has got ValueError. Tried: " + str(i))
            if i > 3:
                return """Has got ValueError. <br><span class="placeholder col-12 bg-danger"></span>"""
            else:
                continue
        except Exception as e:
            return str(e) + """<br><span class="placeholder col-12 bg-danger"></span>"""
