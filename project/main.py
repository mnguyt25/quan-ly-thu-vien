from customtkinter import *
from tkinter import messagebox
from PIL import Image
from database import Database
from ui.admin_interface import open_admin_interface
from ui.user_interface import open_user_interface

# ======= Kết nối CSDL MySQL =======
db = Database()

# ================== CẤU HÌNH GIAO DIỆN ==================
set_appearance_mode("light")
app = CTk()
app.title("Đăng nhập - Thế Giới Thơ Mộng")
app.resizable(False, False)

# ================== LOAD ẢNH NỀN BÊN TRÁI ==================
side_img_data = Image.open("side-img.png")
img_width, img_height = side_img_data.size

# Tự động điều chỉnh kích thước cửa sổ theo ảnh
app.geometry(f"{img_width + 360}x{img_height}")

# CTkImage cho ảnh gốc
side_img = CTkImage(light_image=side_img_data, dark_image=side_img_data, size=(img_width, img_height))

# Hiển thị ảnh bên trái
CTkLabel(master=app, image=side_img, text="").pack(side="left", fill="y")

# ================== FORM ĐĂNG NHẬP BÊN PHẢI ==================
form_frame = CTkFrame(master=app, width=360, height=img_height, fg_color="#ffffff")
form_frame.pack_propagate(False)
form_frame.pack(side="right", fill="both")

# ---------- Tiêu đề ----------
CTkLabel(master=form_frame, text="Thế Giới Thơ Mộng!", text_color="#361035", font=("Arial Bold", 24)).pack(anchor="w", pady=(60, 5), padx=30)
CTkLabel(master=form_frame, text="Sign in to your account", text_color="#7E7E7E", font=("Arial", 12)).pack(anchor="w", padx=30)

# ---------- Nhập tài khoản ----------
CTkLabel(master=form_frame, text="Tài khoản:", text_color="#361035", font=("Arial Bold", 14)).pack(anchor="w", pady=(40, 0), padx=30)
entry_user = CTkEntry(master=form_frame, width=260, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
entry_user.pack(anchor="w", padx=30, pady=(5, 0))

# ---------- Nhập mật khẩu ----------
CTkLabel(master=form_frame, text="Mật khẩu:", text_color="#361035", font=("Arial Bold", 14)).pack(anchor="w", pady=(25, 0), padx=30)
entry_pass = CTkEntry(master=form_frame, width=260, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
entry_pass.pack(anchor="w", padx=30, pady=(5, 0))

# ---------- Hàm đăng nhập ----------
def login():
    username = entry_user.get()
    password = entry_pass.get()
    result = db.fetch_one("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
    if result:
        role = result[0]
        messagebox.showinfo("Thành công", f"Đăng nhập thành công với vai trò: {role}")
        app.destroy()
        if role == "Admin":
            open_admin_interface()
        else:
            open_user_interface()
    else:
        messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")

# ---------- Nút Đăng nhập ----------
CTkButton(master=form_frame, text="Đăng nhập", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=260, command=login).pack(anchor="w", pady=(40, 20), padx=30)

# ================== ĐĂNG KÝ NGAY DƯỚi ==================
def open_register_window():
    reg_win = CTkToplevel(app)
    reg_win.title("Đăng ký tài khoản")
    reg_win.geometry("300x250")

    CTkLabel(reg_win, text="Tên đăng nhập:").pack(pady=(10, 0))
    entry_new_user = CTkEntry(reg_win)
    entry_new_user.pack()

    CTkLabel(reg_win, text="Mật khẩu:").pack(pady=(10, 0))
    entry_new_pass = CTkEntry(reg_win, show="*")
    entry_new_pass.pack()

    def register():
        username = entry_new_user.get()
        password = entry_new_pass.get()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đủ")
            return

        if db.fetch_one("SELECT * FROM users WHERE username = %s", (username,)):
            messagebox.showerror("Trùng tên", "Tên đăng nhập đã tồn tại")
            return

        db.execute_query("INSERT INTO users (username, password, role) VALUES (%s, %s, 'Public')", (username, password))
        messagebox.showinfo("Thành công", "Đăng ký thành công!")
        reg_win.destroy()

    CTkButton(reg_win, text="Đăng ký", command=register).pack(pady=15)

# Nút mở đăng ký
signup_container = CTkFrame(master=form_frame, fg_color="transparent")
signup_container.pack(pady=(10, 0))

CTkLabel(signup_container, text="Bạn chưa có tài khoản?", font=("Arial", 11), text_color="#7E7E7E").pack(side="left", padx=(0, 5))
CTkButton(signup_container, text="Đăng ký", font=("Arial", 11), text_color="#601E88", fg_color="transparent", hover_color="#f3f3f3", width=60, height=28, command=open_register_window).pack(side="left")

# ================== MAIN LOOP ==================
app.mainloop()