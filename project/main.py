from customtkinter import *
from PIL import Image
from database import Database
from ui.admin_interface import open_admin_interface
from ui.user_interface import open_user_interface

db = Database()  # Kết nối CSDL

# ================== CẤU HÌNH GIAO DIỆN ==================
set_appearance_mode("light")
app = CTk()
app.title("Đăng nhập - Thế Giới Thơ Mộng")
app.iconbitmap("icon.png")
app.resizable(False, False)

# ================== LOAD ẢNH NỀN BÊN TRÁI ==================
side_img_data = Image.open("side-img.png")
img_width, img_height = side_img_data.size
app.geometry(f"{img_width + 360}x{img_height}")
side_img = CTkImage(light_image=side_img_data, dark_image=side_img_data, size=(img_width, img_height))
CTkLabel(master=app, image=side_img, text="").pack(side="left", fill="y")

# ================== FORM ĐĂNG NHẬP BÊN PHẢI ==================
form_frame = CTkFrame(master=app, width=360, height=img_height, fg_color="#ffffff")
form_frame.pack_propagate(False)
form_frame.pack(side="right", fill="both")

content_wrapper = CTkFrame(master=form_frame, fg_color="transparent")
content_wrapper.place(relx=0.5, rely=0.5, anchor="center")

# ---------- Tiêu đề ----------
CTkLabel(content_wrapper, text="Thế Giới Thơ Mộng!", text_color="#361035", font=("Arial Bold", 30)).pack(anchor="w", pady=(0, 10), padx=30)
CTkLabel(content_wrapper, text="Đăng nhập vào tài khoản của bạn", text_color="#7E7E7E", font=("Arial Bold", 18)).pack(anchor="w", pady=(0, 20), padx=30)

# ---------- Nhập tài khoản ----------
CTkLabel(content_wrapper, text="Tài khoản:", text_color="#361035", font=("Arial Bold", 18)).pack(anchor="w", pady=(10, 0), padx=30)
entry_username = CTkEntry(content_wrapper, width=260, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
entry_username.pack(anchor="w", padx=30, pady=(5, 10))

# ---------- Nhập mật khẩu ----------
CTkLabel(content_wrapper, text="Mật khẩu:", text_color="#361035", font=("Arial Bold", 18)).pack(anchor="w", pady=(10, 0), padx=30)
entry_password = CTkEntry(content_wrapper, width=260, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
entry_password.pack(anchor="w", padx=30, pady=(5, 20))

# ---------- Hộp thoại tùy chỉnh ----------
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

# ---------- Xử lý đăng nhập ----------
def login():
    username = entry_username.get()
    password = entry_password.get()
    result = db.fetch_one("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
    if result:
        role = result[0]

        def after_login():
            app.destroy()
            if role == "Admin":
                open_admin_interface()
            else:
                open_user_interface()

        if role == "Admin":
            show_message("Thành công", "Đăng nhập thành công với quyền quản trị viên", on_close=after_login)
        else:
            show_message("Thành công", "Đăng nhập thành công", on_close=after_login)
    else:
        show_message("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")

# ---------- Nút Đăng nhập ----------
login_button = CTkButton(content_wrapper, text="Đăng nhập", command=login, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 16), text_color="#ffffff", width=260)
login_button.pack(anchor="w", pady=(10, 20), padx=30)

# ---------- Mở cửa sổ đăng ký ----------
def open_register_window():
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

    register_button = CTkButton(reg_win, text="Đăng ký", command=register, fg_color="#601E88", text_color="#fff", font=("Arial Bold", 13))
    register_button.pack(pady=20)

    entry_new_user.bind("<Return>", lambda event: register())
    entry_new_pass.bind("<Return>", lambda event: register())

# ================== ĐĂNG KÝ DƯỚI FORM ==================
signup_container = CTkFrame(master=content_wrapper, fg_color="transparent")
signup_container.pack(pady=(0, 20), anchor="w", padx=30)

CTkLabel(signup_container, text="Bạn chưa có tài khoản?", font=("Arial Bold", 16), text_color="#7E7E7E").pack(side="left", padx=(0, 5))
CTkButton(signup_container, text="Đăng ký", font=("Arial Bold", 16), text_color="#601E88", fg_color="transparent", hover_color="#f3f3f3", command=open_register_window, width=1).pack(side="left", pady=0)

entry_username.bind("<Return>", lambda event: login())
entry_password.bind("<Return>", lambda event: login())

# ================== MAIN LOOP ==================
app.mainloop()
