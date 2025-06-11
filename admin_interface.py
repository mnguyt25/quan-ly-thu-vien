import tkinter as tk
from tkinter import messagebox

# ======= Giao diện Quản trị viên =======
def open_admin_interface():
    window = tk.Tk()
    window.title("Giao diện Quản trị viên")
    window.geometry("400x300")
    try:
        window.iconbitmap("books_icon.ico")
    except:
        pass
    
    # === Menu Bar ===
    menubar = tk.Menu(window)

    # Quản lý sách
    book_menu = tk.Menu(menubar, tearoff=0)
    book_menu.add_command(label="Thêm sách", command=add_book)
    book_menu.add_command(label="Sửa sách", command=edit_book)
    book_menu.add_command(label="Xóa sách", command=delete_book)
    book_menu.add_command(label="Tìm sách", command=find_book)
    book_menu.add_command(label="Hiển thị sách", command=show_book)
    menubar.add_cascade(label="Quản lý sách", menu=book_menu)

    # Quản lý người dùng
    user_menu = tk.Menu(menubar, tearoff=0)
    user_menu.add_command(label="Thêm người dùng", command=lambda: add_user())
    user_menu.add_command(label="Sửa thông tin người dùng", command=lambda: edit_user())
    user_menu.add_command(label="Xóa người dùng", command=lambda: delete_user())
    user_menu.add_command(label="Tìm kiếm thông tin người dùng", command=lambda: find_user())
    user_menu.add_command(label="Hiển thị danh sách người dùng", command=lambda: show_user())
    menubar.add_cascade(label="Quản lý người dùng", menu=user_menu)

    # Thoát
    menubar.add_command(label="Thoát", command=window.destroy)

    window.config(menu=menubar)

    tk.Label(window, text="Quản lý thư viện", font=("Arial", 16)).pack(pady=20)
    
    window.mainloop()

# Demo
# Chức năng sách
def add_book():
    messagebox.showinfo("Quản lý sách", "Chức năng thêm sách")

def edit_book():
    messagebox.showinfo("Quản lý sách", "Chức năng sửa sách")

def delete_book():
    messagebox.showinfo("Quản lý sách", "Chức năng xóa sách")

def find_book():
    messagebox.showinfo("Quản lý sách", "Chức năng tìm sách")

def show_book():
    messagebox.showinfo("Quản lý sách", "Chức năng hiển thị sách")

# Chức năng người dùng
def add_user():
    messagebox.showinfo("Người dùng", "Thêm người dùng")

def edit_user():
    messagebox.showinfo("Người dùng", "Sửa thông tin người dùng")

def delete_user():
    messagebox.showinfo("Người dùng", "Xóa người dùng")

def find_user():
    messagebox.showinfo("Người dùng", "Tìm kiếm thông tin người dùng")

def show_user():
    messagebox.showinfo("Người dùng", "Hiển thị danh sách người dùng")