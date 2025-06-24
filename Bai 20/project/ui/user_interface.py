from customtkinter import *
from tkinter import messagebox
from PIL import Image
from CTkTable import CTkTable
from database import db
from models.books import *

def open_user_interface(username):
    app = CTk()
    app.title("📖 Thư Viện")
    app.geometry("1024x660")
    app.resizable(False, False)
    set_appearance_mode("light")

    sidebar_frame = CTkFrame(app, fg_color="#361035", width=220, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(side="left", fill="y")

    # Logo
    logo_img_data = Image.open("project/logo.png")
    logo_img = CTkImage(
        dark_image=logo_img_data, light_image=logo_img_data, size=(80, 80)
    )
    logo_container = CTkFrame(
        sidebar_frame, fg_color="transparent", width=220, height=130
    )
    logo_container.pack_propagate(False)
    logo_container.pack(pady=10)
    CTkLabel(logo_container, text="", image=logo_img).pack(anchor="center")

    CTkLabel(
        sidebar_frame,
        text="Thư Viện",
        font=("Segoe UI", 18, "bold"),
        text_color="white",
    ).pack(pady=5)

    user_label = db.fetch_one(
        "SELECT username FROM users WHERE username = %s", (username,)
    )
    username_display = user_label[0] if user_label else username
    CTkLabel(
        sidebar_frame,
        text=f"👤 {username_display}",
        font=("Segoe UI", 14),
        text_color="white",
    ).pack(side="bottom", pady=10)

    main_view = CTkFrame(app, fg_color="#f0f0f0")
    main_view.pack(fill="both", expand=True)
    frames = {}

    def show_frame(name):
        for f in frames.values():
            f.pack_forget()
        frames[name].pack(expand=True, fill="both", padx=30, pady=25)
        if name == "view_books":
            update_table()
        if name == "history":
            update_history_table()

    # === XEM SÁCH ===
    view_books_frame = CTkFrame(main_view, fg_color="white")
    CTkLabel(
        view_books_frame,
        text="📚 Danh Sách Sách",
        font=("Segoe UI", 22, "bold"),
        text_color="#2A8C55",
    ).pack(pady=10)

    search_entry = CTkEntry(
        view_books_frame,
        placeholder_text="Tìm kiếm theo tên, tác giả, ID hoặc năm xuất bản",
        width=500,
    )
    search_entry.pack(pady=6)

    def status_text(status):
        return {0: "Có sẵn", 1: "Đã mượn", 2: "Quá hạn"}.get(status, "Không rõ")

    def update_table():
        keyword = search_entry.get().strip()
        books = search_books_in_store(keyword) if keyword else get_all_books()
        values = [
            [
                "ID",
                "Tên",
                "Tác giả",
                "Số trang",
                "Năm xuất bản",
                "Trạng thái",
                "Chủng loại",
            ]
        ]
        if books:
            for b in books:
                values.append(
                    [
                        str(b[0]),
                        b[1],
                        b[2],
                        str(b[3]),
                        str(b[4]),
                        status_text(b[5]),
                        b[6],
                    ]
                )
        else:
            values.append(["-", "Không tìm thấy sách", "-", "-", "-", "-", "-"])
        global book_table
        try:
            book_table.destroy()
        except:
            pass
        book_table = CTkTable(
            master=table_container,
            values=values,
            colors=["#FAFAFA", "#EEEEEE"],
            header_color="#361035",
            hover_color="#E0E0E0",
            corner_radius=6,
        )
        book_table.edit_row(0, text_color="white")
        book_table.pack(fill="both", expand=True)

    CTkButton(
        view_books_frame,
        text="🔍 Tìm kiếm",
        command=update_table,
        fg_color="#2A8C55",
        hover_color="#207244",
    ).pack()

    table_container = CTkScrollableFrame(view_books_frame)
    table_container.pack(fill="both", expand=True, padx=10, pady=10)

    global book_table
    book_table = CTkTable(
        master=table_container,
        values=[
            [
                "ID",
                "Tên",
                "Tác giả",
                "Số trang",
                "Năm xuất bản",
                "Trạng thái",
                "Chủng loại",
            ]
        ],
        colors=["#FAFAFA", "#EEEEEE"],
        header_color="#361035",
        hover_color="#E0E0E0",
        corner_radius=6,
    )
    book_table.edit_row(0, text_color="white")
    book_table.pack(fill="both", expand=True)

    frames["view_books"] = view_books_frame

    # === MƯỢN SÁCH ===
    borrow_frame = CTkFrame(main_view, fg_color="white")
    CTkLabel(
        borrow_frame,
        text="📗 Mượn Sách",
        font=("Segoe UI", 22, "bold"),
        text_color="#2A8C55",
    ).pack(pady=10)
    borrow_entry = CTkEntry(
        borrow_frame, placeholder_text="ID sách muốn mượn", width=400
    )
    borrow_entry.pack(pady=6)

    def borrow_book():
        book_id = borrow_entry.get()
        if not book_id.isdigit():
            messagebox.showerror("Lỗi", "ID không hợp lệ.")
            return
        success = borrow_book_by_id(int(book_id), username)
        if success:
            messagebox.showinfo("✅ Thành công", "Đã mượn sách.")
        else:
            messagebox.showwarning("⚠️ Thất bại", "Không thể mượn sách này.")

    CTkButton(
        borrow_frame,
        text="📗 Mượn sách",
        command=borrow_book,
        fg_color="#2A8C55",
        hover_color="#207244",
    ).pack(pady=6)
    frames["borrow"] = borrow_frame

    # === TRẢ SÁCH ===
    return_frame = CTkFrame(main_view, fg_color="white")
    CTkLabel(
        return_frame,
        text="📕 Trả Sách",
        font=("Segoe UI", 22, "bold"),
        text_color="#D94141",
    ).pack(pady=10)
    return_entry = CTkEntry(
        return_frame, placeholder_text="ID sách muốn trả", width=400
    )
    return_entry.pack(pady=6)

    def return_book():
        book_id = return_entry.get()
        if not book_id.isdigit():
            messagebox.showerror("Lỗi", "ID không hợp lệ.")
            return
        success = return_book_by_id(int(book_id), username)
        if success:
            messagebox.showinfo("✅ Thành công", "Đã trả sách.")
        else:
            messagebox.showwarning("⚠️ Thất bại", "Không thể trả sách.")

    CTkButton(
        return_frame,
        text="📕 Trả sách",
        command=return_book,
        fg_color="#D94141",
        hover_color="#B32F2F",
    ).pack(pady=6)
    frames["return"] = return_frame

    # === LỊCH SỬ MƯỢN ===
    history_frame = CTkFrame(main_view, fg_color="white")
    CTkLabel(
        history_frame,
        text="🕓 Lịch Sử Mượn Sách",
        font=("Segoe UI", 22, "bold"),
        text_color="#2A8C55",
    ).pack(pady=10)
    extend_entry = CTkEntry(
        history_frame, placeholder_text="ID sách muốn gia hạn", width=400
    )
    extend_entry.pack(pady=6)

    def extend_loan():
        book_id = extend_entry.get()
        if not book_id.isdigit():
            messagebox.showerror("Lỗi", "ID không hợp lệ.")
            return
        success = extend_loan_by_id(int(book_id), username)
        if success:
            messagebox.showinfo("Đã gia hạn", "Gia hạn thành công.")
        else:
            messagebox.showwarning("Không thể gia hạn", "Không thể gia hạn sách.")

    CTkButton(
        history_frame,
        text="⏱️ Gia hạn",
        command=extend_loan,
        fg_color="#2A8C55",
        hover_color="#207244",
    ).pack(pady=6)

    history_table_container = CTkScrollableFrame(history_frame)
    history_table_container.pack(fill="both", expand=True, padx=10, pady=10)

    global history_table
    try:
        history_table.destroy()
    except:
        pass
    history_table = CTkTable(
        master=history_table_container,
        values=[["ID Sách", "Tên Sách", "Ngày Mượn", "Trạng Thái", "Gia Hạn"]],
        colors=["#FAFAFA", "#EEEEEE"],
        header_color="#361035",
        hover_color="#E0E0E0",
        corner_radius=6,
    )
    history_table.edit_row(0, text_color="white")
    history_table.pack(fill="both", expand=True)

    def update_history_table():
        records = get_borrow_history_by_user(username)
        values = [["ID Sách", "Tên Sách", "Ngày Mượn", "Trạng Thái", "Gia Hạn"]]
        if records:
            for r in records:
                book_id = str(r[0])
                title = r[1]
                date = str(r[2])
                status = "Đã trả" if r[3] == 1 else "Chưa trả"
                extension = (
                    "Đã gia hạn" if r[4] == 1 else ("Chưa gia hạn" if r[4] == 0 else "")
                )
                values.append([book_id, title, date, status, extension])
        else:
            values.append(["-", "-", "-", "-", "Chưa có lịch sử mượn"])
        global history_table
        try:
            history_table.destroy()
        except:
            pass
        history_table = CTkTable(
            master=history_table_container,
            values=values,
            colors=["#FAFAFA", "#EEEEEE"],
            header_color="#361035",
            hover_color="#E0E0E0",
            corner_radius=6,
        )
        history_table.edit_row(0, text_color="white")
        history_table.pack(fill="both", expand=True)

    frames["history"] = history_frame

    # Sidebar Buttons
    button_style = dict(
        fg_color="transparent",
        font=("Segoe UI", 14),
        text_color="white",
        hover_color="#8844aa",
        anchor="w",
        corner_radius=8,
    )
    padding = dict(anchor="center", ipady=6, pady=6, fill="x", padx=16)

    CTkButton(
        sidebar_frame,
        text="📚 Xem sách",
        command=lambda: show_frame("view_books"),
        **button_style,
    ).pack(**padding)
    CTkButton(
        sidebar_frame,
        text="📗 Mượn sách",
        command=lambda: show_frame("borrow"),
        **button_style,
    ).pack(**padding)
    CTkButton(
        sidebar_frame,
        text="📕 Trả sách",
        command=lambda: show_frame("return"),
        **button_style,
    ).pack(**padding)
    CTkButton(
        sidebar_frame,
        text="🕓 Lịch sử mượn",
        command=lambda: show_frame("history"),
        **button_style,
    ).pack(**padding)

    show_frame("view_books")
    app.mainloop()