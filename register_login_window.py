# import tkinter as tk
# from tkinter import messagebox

# # ======= Giao diện Đăng ký =======
# def open_register_window():
#     # Mở cửa sổ để đăng ký
#     reg_win = tk.Toplevel()
#     reg_win.title("Đăng ký tài khoản")
#     reg_win.geometry("300x250")

#     tk.Label(reg_win, text="Tên đăng nhập:").pack()
#     entry_new_user = tk.Entry(reg_win)
#     entry_new_user.pack()

#     tk.Label(reg_win, text="Mật khẩu:").pack()
#     entry_new_pass = tk.Entry(reg_win, show="*")
#     entry_new_pass.pack()

#     def register():
#         username = entry_new_user.get()
#         password = entry_new_pass.get()

#         if not username or not password:
#             messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ")
#             return

#         if db.fetch_one("SELECT * FROM users WHERE username = %s", (username,)):
#             messagebox.showerror("Trùng tên", "Tên đăng nhập đã tồn tại")
#             return

#         db.execute_query("INSERT INTO users (username, password, role) VALUES (%s, %s, 'Người dùng')",
#                        (username, password))
        
#         messagebox.showinfo("Thành công", "Đăng ký thành công!")
#         reg_win.destroy()

#     tk.Button(reg_win, text="Đăng ký", command=register).pack(pady=10)