import tkinter as tk
from tkinter import messagebox

def open_user_interface():
    window = tk.Toplevel()
    window.title("Người dùng")
    window.geometry("1200x600")

    def borrow_book():
        messagebox.showinfo("Mượn sách", "Chức năng Mượn sách")

    def return_book():
        messagebox.showinfo("Trả sách", "Chức năng Trả sách")

    def search_book():
        messagebox.showinfo("Tìm kiếm", "Chức năng Tìm sách")

    def extend_book():
        messagebox.showinfo("Gia hạn", "Chức năng Gia hạn trả sách")

    def view_books():
        messagebox.showinfo("Xem", "Chức năng Xem thông tin sách")

    tk.Label(window, text="Giao diện Người dùng", font=("Arial", 16)).pack(pady=10)
    tk.Button(window, text="Mượn sách", width=20, command=borrow_book).pack(pady=5)
    tk.Button(window, text="Trả sách", width=20, command=return_book).pack(pady=5)
    tk.Button(window, text="Tìm kiếm sách", width=20, command=search_book).pack(pady=5)
    tk.Button(window, text="Gia hạn sách", width=20, command=extend_book).pack(pady=5)
    tk.Button(window, text="Xem thông tin sách", width=20, command=view_books).pack(pady=5)
