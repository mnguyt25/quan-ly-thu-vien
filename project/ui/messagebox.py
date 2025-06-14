from customtkinter import *

def show_message(title, message, icon="info", on_close=None):
    msg = CTkToplevel()
    msg.title(title)
    msg.geometry("300x150")
    msg.resizable(False, False)
    msg.grab_set()

    CTkLabel(msg, text=title, font=("Arial Bold", 18)).pack(pady=(20, 5))
    CTkLabel(msg, text=message, wraplength=250, font=("Arial", 13)).pack(pady=(0, 10))

    def handle_close():
        msg.destroy()
        if on_close:
            on_close()

    CTkButton(msg, text="OK", command=handle_close, font=("Arial Bold", 13)).pack(pady=5)
