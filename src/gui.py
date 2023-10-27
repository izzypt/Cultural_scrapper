import customtkinter as tk
from tkinter import messagebox
import tkinter
from tkinter import PhotoImage
import os
from utils import start_scripts, is_valid_email
from dotenv import load_dotenv
import threading

############
# LOAD ENV #
############
dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')
load_dotenv(dotenv_path=dotenv_path)

#########################
# SET GUI COLOR & THEME #
#########################
tk.set_appearance_mode('System')
tk.set_default_color_theme("blue")

###########
# INIT TK #
###########
app = tk.CTk()
app.geometry("720x480")
app.title("Agenda Cultural")

image = PhotoImage(file="../assets/culture_fest.png")
image_label = tkinter.Label(app, image=image)
image_label.pack(padx=10, pady=10)

title = tk.CTkLabel(app, text="Coloca o e-mail em que queres os últimos eventos culturais.")
title.pack(padx=10, pady=10)

email_recipient = tkinter.StringVar()
email = tk.CTkEntry(app, width=350, height=40, textvariable=email_recipient)
email.pack()

progress_bar = tk.CTkProgressBar(app, width=400, mode='indeterminate')

#####################
# HANDLER FUNCTIONS #
#####################
def put_progress_bar():
    progress_bar.pack(padx=10, pady=10)
    progress_bar.start()

def start_scrape():
    rec_email = email_recipient.get()
    if is_valid_email(rec_email):
        os.environ["REC_EMAIL"] = rec_email
        put_progress_bar()
        scraping_thread = threading.Thread(target=scrape_background)
        scraping_thread.start()
    else:
        messagebox.showerror("Invalid email address", "Please enter a valid email address")

def scrape_background():
    print("Started scrap thread..")
    finished_scripts = start_scripts(os.environ["REC_EMAIL"])
    if finished_scripts:
        progress_bar.stop()
        progress_bar.pack_forget()
        button.pack_forget()
        final_message = tk.CTkLabel(app, text="Scrapping finished. Close the program.")
        final_message.pack(padx=10, pady=10)


button = tk.CTkButton(app, text="Start", command=start_scrape)
button.pack(padx=10, pady=10)



app.mainloop()