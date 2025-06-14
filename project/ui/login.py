from customtkinter import *
from PIL import Image # mở ảnh
import sys, os # thêm thư mục cha vào sys.path để import được database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database import Database
from ui.register import open_register_window
from ui.messagebox import show_message
from ui.admin_interface import open_admin_interface
from ui.user_interface import open_user_interface

def open_login_window():
    db = Database()
    app = CTk() # custom window, tạo ra cửa sổ chính, tương tự như tk.Tk() trong tkinter
    app.title("Đăng nhập - Thế Giới Thơ Mộng") # tiêu đề
    app.iconbitmap("icon.ico") 
    app.resizable(False, False) # không cho resize

    # Hiển thị ảnh bên trái
    side_img_data = Image.open("side-img.png")
    img_width, img_height = side_img_data.size
    app.geometry(f"{img_width + 360}x{img_height}")
    side_img = CTkImage(light_image=side_img_data, dark_image=side_img_data, size=(img_width, img_height))
    CTkLabel(master=app, image=side_img, text="").pack(side="left", fill="y")

    # Khung chứa form bên phải
    form_frame = CTkFrame(master=app, width=360, height=img_height, fg_color="#ffffff") # tạo form trắng ở bên phải chứa nội dung chính
    form_frame.pack_propagate(False)
    form_frame.pack(side="right", fill="both")

    # căn giữa form đăng nhập
    content_wrapper = CTkFrame(master=form_frame, fg_color="transparent")
    content_wrapper.place(relx=0.5, rely=0.5, anchor="center")

    # --- Tiêu đề ---
    CTkLabel(content_wrapper, text="Thế Giới Thơ Mộng!", text_color="#361035", font=("Arial Bold", 30)).pack(anchor="w", pady=(0, 10), padx=30)
    CTkLabel(content_wrapper, text="Đăng nhập vào tài khoản của bạn", text_color="#7E7E7E", font=("Arial Bold", 18)).pack(anchor="w", pady=(0, 20), padx=30)

    # --- Entry ---
    CTkLabel(content_wrapper, text="Tài khoản:", text_color="#361035", font=("Arial Bold", 18)).pack(anchor="w", pady=(10, 0), padx=30)
    entry_username = CTkEntry(content_wrapper, width=260, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
    entry_username.pack(anchor="w", padx=30, pady=(5, 10))

    CTkLabel(content_wrapper, text="Mật khẩu:", text_color="#361035", font=("Arial Bold", 18)).pack(anchor="w", pady=(10, 0), padx=30)
    entry_password = CTkEntry(content_wrapper, width=260, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
    entry_password.pack(anchor="w", padx=30, pady=(5, 20))

    # --- Đăng nhập ---
    def login():
        username = entry_username.get()
        password = entry_password.get()
        result = db.fetch_one("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
        if result:
            role = result[0].strip().lower()

            def after_login():
                app.destroy()
                if role == "admin":
                    open_admin_interface()
                else:
                    open_user_interface()

            if role == "admin":
                show_message("Thành công", "Đăng nhập thành công với quyền quản trị viên", on_close=after_login)
            else:
                show_message("Thành công", "Đăng nhập thành công", on_close=after_login)
        else:
            show_message("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")

    CTkButton(content_wrapper, text="Đăng nhập", command=login, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 16), text_color="#ffffff", width=260).pack(anchor="w", pady=(10, 20), padx=30)

    # --- Đăng ký ---
    signup_container = CTkFrame(master=content_wrapper, fg_color="transparent")
    signup_container.pack(pady=(0, 20), anchor="w", padx=30)

    CTkLabel(signup_container, text="Bạn chưa có tài khoản?", font=("Arial Bold", 16), text_color="#7E7E7E").pack(side="left", padx=(0, 5))
    CTkButton(signup_container, text="Đăng ký", font=("Arial Bold", 16), text_color="#601E88", fg_color="transparent", hover_color="#f3f3f3", command=open_register_window, width=1).pack(side="left", pady=0)

    # hỗ trợ nhấn enter để đăng nhập
    entry_username.bind("<Return>", lambda event: login())
    entry_password.bind("<Return>", lambda event: login())

    app.mainloop()
