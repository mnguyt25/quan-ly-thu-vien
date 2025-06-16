import tkinter as tk
from tkinter import messagebox

# ======= Giao diện Người dùng =======
def open_user_interface():
    window = tk.Tk()
    window.title("Giao diện Người dùng")
    window.geometry("400x300")
    try:
        window.iconbitmap("books_icon.ico")
    except:
        pass
    
    # === Menu Bar ===
    menubar = tk.Menu(window)

    # Chức năng
    menubar.add_command(label="Mượn sách", command=borrow)
    menubar.add_command(label="Trả sách", command=return_book)
    # book_menu.add_command(label="Xóa sách", command=delete_book)

    # Thoát
    menubar.add_command(label="Thoát", command=window.destroy)

    window.config(menu=menubar)

    tk.Label(window, text="Thư viện", font=("Arial", 16)).pack(pady=20)
    window.mainloop()

# Demo
def borrow():
    pass

def return_book():
    pass