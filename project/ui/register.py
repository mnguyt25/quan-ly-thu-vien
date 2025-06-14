from customtkinter import *
from database import Database
from ui.messagebox import show_message

def open_register_window():
    db = Database()
    reg_win = CTkToplevel()
    reg_win.title("Đăng ký tài khoản")
    reg_win.geometry("360x360")
    reg_win.resizable(False, False)

    CTkLabel(reg_win, text="Đăng ký tài khoản", font=("Arial Bold", 20)).pack(pady=(20, 10))

    CTkLabel(reg_win, text="Tên đăng nhập:", font=("Arial", 13)).pack(pady=(10, 0))
    entry_new_user = CTkEntry(reg_win, width=260)
    entry_new_user.pack()

    CTkLabel(reg_win, text="Mật khẩu:", font=("Arial", 13)).pack(pady=(10, 0))
    entry_new_pass = CTkEntry(reg_win, show="*", width=260)
    entry_new_pass.pack()

    def register():
        username = entry_new_user.get()
        password = entry_new_pass.get()

        if not username or not password:
            show_message("Thiếu thông tin", "Vui lòng điền đầy đủ")
            return

        if db.fetch_one("SELECT * FROM users WHERE username = %s", (username,)):
            show_message("Trùng tên", "Tên đăng nhập đã tồn tại")
            return

        db.execute_query("INSERT INTO users (username, password, role) VALUES (%s, %s, 'Public')", (username, password))
        show_message("Thành công", "Đăng ký thành công!")
        reg_win.destroy()

    CTkButton(reg_win, text="Đăng ký", command=register, fg_color="#601E88", text_color="#fff", font=("Arial Bold", 13)).pack(pady=20)

    entry_new_user.bind("<Return>", lambda event: register())
    entry_new_pass.bind("<Return>", lambda event: register())
