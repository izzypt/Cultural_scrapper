import subprocess
import re

email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"

def start_scripts(email):
    print(f"We will start scraping and send email to {email}!!!")
    try:
        process = subprocess.Popen(["python3", "agendalx.py"])
        process.wait()
    except subprocess.CalledProcessError as e:
        print(f"Failed to run the script agendalx.py: {e}")
        return False
    return True

def is_valid_email(email):
    return re.match(email_pattern, email) is not None