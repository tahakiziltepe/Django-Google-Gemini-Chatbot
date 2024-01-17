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
            return yanit.replace('<pre>', "<'pre'>").replace('<code>', "<'code'>").replace('•', '  *')
        except ValueError:
            i = i + 1
            print("utils -> Except çalıştı. Deneme: " + str(i))
            if i > 3:
                return "Tekrar yazar mısınız?"
            else:
                continue
        except Exception as e:
            return str(e) + """<br><span class="placeholder col-12 bg-danger"></span>"""
