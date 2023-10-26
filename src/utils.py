import subprocess
import main

def start_scripts(email):
    print(f"We will start scraping and send email to {email}!!!")
    try:
        process = subprocess.Popen(["python3", "agendalx.py"])
        process.wait()
    except subprocess.CalledProcessError as e:
        print(f"Failed to run the script agendalx.py: {e}")
        return False
    return True
