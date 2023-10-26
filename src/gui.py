import customtkinter as tk
import tkinter
from tkinter import PhotoImage
import os
from utils import start_scripts
from dotenv import load_dotenv

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

#####################
# HANDLER FUNCTIONS #
#####################
def start_scrape():
    rec_email = email_recipient.get()
    os.environ["REC_EMAIL"] = rec_email
    progress_bar.pack(padx=10, pady=10)
    progress_bar.start()
    finished_scripts = start_scripts(os.environ["REC_EMAIL"])
    if finished_scripts:
        finish_scrape()

def finish_scrape():
    progress_bar.stop()
    progress_bar.pack_forget()
    button.pack_forget()
    final_message = tk.CTkLabel(app, text="Scrapping finished. Close the program.")
    final_message.pack(padx=10, pady=10)

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

button = tk.CTkButton(app, text="Start", command=start_scrape)
button.pack(padx=10, pady=10)

app.mainloop()