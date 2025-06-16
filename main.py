import tkinter as tk
import pyodbc
from tkinter import messagebox
from database import Database
from admin_interface import open_admin_interface
from user_interface import open_user_interface, get_user_id

# ======= Kết nối CSDL SQL Server =======
db = Database()

# ======= Hàm Đăng nhập =======
def login():
    username = entry_user.get()
    password = entry_pass.get()

    # Dùng dấu ? thay cho %s (chuẩn SQL Server)
    result = db.fetch_one("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))

    if result:
        role = result[0]
        messagebox.showinfo("Thành công", f"Đăng nhập thành công với vai trò: {role}")
        login_window.destroy()

        if role.lower() == "admin":
            open_admin_interface()
        else:
            open_user_interface(username)
    else:
        messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu.")

# ======= Giao diện Đăng ký =======
def open_register_window():
    reg_win = tk.Toplevel()
    reg_win.title("Đăng ký tài khoản")
    reg_win.geometry("300x250")

    tk.Label(reg_win, text="Tên đăng nhập:").pack()
    entry_new_user = tk.Entry(reg_win)
    entry_new_user.pack()

    tk.Label(reg_win, text="Mật khẩu:").pack()
    entry_new_pass = tk.Entry(reg_win, show="*")
    entry_new_pass.pack()

    def register():
        username = entry_new_user.get()
        password = entry_new_pass.get()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ")
            return

        # Truy vấn kiểm tra username đã tồn tại
        if db.fetch_one("SELECT * FROM users WHERE username = ?", (username,)):
            messagebox.showerror("Trùng tên", "Tên đăng nhập đã tồn tại")
            return

        # Thêm người dùng mới (role mặc định: public)
        db.execute_query("INSERT INTO users (username, password, role) VALUES (?, ?, 'public')",
                         (username, password))
        
        messagebox.showinfo("Thành công", "Đăng ký thành công!")
        reg_win.destroy()

    tk.Button(reg_win, text="Đăng ký", command=register).pack(pady=10)

# ======= Giao diện Đăng nhập chính =======
if __name__ == "__main__":
    login_window = tk.Tk()
    login_window.title("Đăng nhập hệ thống")
    login_window.geometry("300x220")

    try:
        login_window.iconbitmap("books_icon.ico")
    except:
        pass

    tk.Label(login_window, text="Tên đăng nhập:").pack()
    entry_user = tk.Entry(login_window)
    entry_user.pack()

    tk.Label(login_window, text="Mật khẩu:").pack()
    entry_pass = tk.Entry(login_window, show="*")
    entry_pass.pack()

    tk.Button(login_window, text="Đăng nhập", command=login).pack(pady=10)
    tk.Button(login_window, text="Đăng ký tài khoản", command=open_register_window).pack()

    login_window.mainloop()
