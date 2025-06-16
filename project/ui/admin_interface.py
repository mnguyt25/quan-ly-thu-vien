import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from customtkinter import *
from PIL import Image
from tkinter import messagebox
from CTkTable import CTkTable
from models.books import add_book_to_store, delete_book_from_store, update_book_in_store, search_books_in_store, get_all_books

def open_admin_interface():
    app = CTk()
    app.title("📚 Quản Lý Thư Viện")
    app.geometry("1024x660")
    app.resizable(False, False)
    set_appearance_mode("light")

    # Sidebar
    sidebar_frame = CTkFrame(app, fg_color="#361035", width=220, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(side="left", fill="y")

    # Logo
    logo_img_data = Image.open("logo.png")
    logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(80, 80))
    logo_container = CTkFrame(sidebar_frame, fg_color="transparent", width=220, height=130)
    logo_container.pack_propagate(False)
    logo_container.pack(pady=10)
    CTkLabel(logo_container, text="", image=logo_img).pack(anchor="center")
    CTkLabel(sidebar_frame, text="Thư Viện", font=("Segoe UI", 18, "bold"), text_color="white").pack(pady=5)

    # Main View
    main_view = CTkFrame(app, fg_color="#f0f0f0")
    main_view.pack(fill="both", expand=True)
    frames = {}

    def show_frame(name):
        for f in frames.values():
            f.pack_forget()
        frames[name].pack_forget()
        if name == "view_books":
            update_table()
        frames[name].pack(expand=True, fill="both", padx=30, pady=25)

    # Thêm sách
    add_book_frame = CTkFrame(main_view, fg_color="white")
    CTkLabel(add_book_frame, text="➕ Thêm Sách", font=("Segoe UI", 22, "bold"), text_color="#2A8C55").pack(pady=20)
    add_id = CTkEntry(add_book_frame, placeholder_text="ID", width=400)
    add_name = CTkEntry(add_book_frame, placeholder_text="Tên sách", width=400)
    add_author = CTkEntry(add_book_frame, placeholder_text="Tác giả", width=400)
    add_pages = CTkEntry(add_book_frame, placeholder_text="Số trang", width=400)
    add_published = CTkEntry(add_book_frame, placeholder_text="Năm xuất bản", width=400)
    add_status = CTkComboBox(add_book_frame, values=["0 - Có sẵn", "1 - Đã mượn", "2 - Quá hạn"], width=400)
    add_type = CTkComboBox(add_book_frame, values=["Truyện ngắn", "Tiểu thuyết", "Giáo trình", "Tài liệu", "Khác"], width=400)

    def add_book():
        id, name, author, pages, published, status, type = add_id.get(), add_name.get(), add_author.get(), add_pages.get(), add_published.get(), add_status.get().split(" - ")[0], add_type.get()
        if not id.isdigit() or not name or not author or not pages.isdigit() or not published.isdigit():
            messagebox.showerror("Lỗi", "Nhập đủ thông tin.")
            return
        add_book_to_store(int(id), name, author, int(pages), int(published), int(status), type)
        messagebox.showinfo("Thành công", f"Thêm sách ID {id} thành công")
        add_id.delete(0, END)
        add_name.delete(0, END)
        add_author.delete(0, END)
        add_pages.delete(0, END)
        add_published.delete(0, END)

    CTkButton(add_book_frame, text="Thêm", command=add_book, fg_color="#2A8C55", hover_color="#207244", font=("Segoe UI", 14)).pack(pady=20)
    for entry in (add_id, add_name, add_author, add_pages, add_published, add_status, add_type):
        entry.pack(pady=6)
    frames["add_book"] = add_book_frame

    # Xoá sách
    delete_book_frame = CTkFrame(main_view, fg_color="white")
    CTkLabel(delete_book_frame, text="🗑️ Xoá Sách", font=("Segoe UI", 22, "bold"), text_color="#D94141").pack(pady=20)
    delete_id = CTkEntry(delete_book_frame, placeholder_text="ID sách", width=400)

    def delete_book_by_id():
        input_id = delete_id.get()
        if not input_id.isdigit():
            messagebox.showerror("Lỗi", "ID không hợp lệ.")
            return
        success = delete_book_from_store(int(input_id))
        if success:
            messagebox.showinfo("Đã xoá", f"Sách ID {input_id} đã được xoá")
        else:
            messagebox.showwarning("Không tìm thấy", f"ID {input_id} không tồn tại")
        delete_id.delete(0, END)

    CTkButton(delete_book_frame, text="Xoá", command=delete_book_by_id, fg_color="#D94141", hover_color="#B32F2F", font=("Segoe UI", 14)).pack(pady=20)
    delete_id.pack(pady=10)
    frames["delete_book"] = delete_book_frame

    # Cập nhật sách
    update_book_frame = CTkFrame(main_view, fg_color="white")
    CTkLabel(update_book_frame, text="✏️ Cập Nhật Sách", font=("Segoe UI", 22, "bold"), text_color="#2A8C55").pack(pady=20)
    old_id = CTkEntry(update_book_frame, placeholder_text="ID sách", width=400)
    new_name = CTkEntry(update_book_frame, placeholder_text="Tên mới", width=400)
    new_author = CTkEntry(update_book_frame, placeholder_text="Tác giả mới", width=400)
    new_pages = CTkEntry(update_book_frame, placeholder_text="Số trang mới", width=400)
    new_published = CTkEntry(update_book_frame, placeholder_text="Năm xuất bản", width=400)
    new_status = CTkComboBox(update_book_frame, values=["0 - Có sẵn", "1 - Đã mượn", "2 - Quá hạn"], width=400)
    new_type = CTkComboBox(update_book_frame, values=["Truyện ngắn", "Tiểu thuyết", "Giáo trình", "Tài liệu", "Khác"], width=400)

    def update_book():
        if not old_id.get().isdigit():
            messagebox.showerror("Lỗi", "ID không hợp lệ.")
            return
        success = update_book_in_store(
            int(old_id.get()),
            name=new_name.get() or None,
            author=new_author.get() or None,
            pages=int(new_pages.get()) if new_pages.get().isdigit() else None,
            published_year=int(new_published.get()) if new_published.get().isdigit() else None,
            status=int(new_status.get().split(" - ")[0]) if new_status.get().isdigit() else None,
            category=new_type.get() or None
        )
        if success:
            messagebox.showinfo("Thành công", "Cập nhật thành công")
            for e in (old_id, new_name, new_author, new_pages, new_published):
                e.delete(0, END)
        else:
            messagebox.showwarning("Không tìm thấy", "ID không tồn tại")

    CTkButton(update_book_frame, text="Cập nhật", command=update_book, fg_color="#2A8C55", hover_color="#207244", font=("Segoe UI", 14)).pack(pady=20)
    for e in (old_id, new_name, new_author, new_pages, new_published, new_status, new_type):
        e.pack(pady=6)
    frames["update_book"] = update_book_frame

    # Xem sách
    view_books_frame = CTkFrame(main_view, fg_color="white")

    # --- Hàm chuyển trạng thái số thành chữ ---
    def status_text(status):
        return {
            0: "Có sẵn",
            1: "Đã mượn",
            2: "Quá hạn"
        }.get(status, "Không rõ")

    # --- Thanh tìm kiếm ---
    search_frame = CTkFrame(view_books_frame, fg_color="transparent")
    search_frame.pack(fill="x", padx=10, pady=(10, 0))

    search_entry = CTkEntry(search_frame, placeholder_text="Tìm kiếm theo tên, tác giả, ID hoặc năm xuất bản", width=400)
    search_entry.pack(side="left", padx=(0, 10))

    def search_books():
        keyword = search_entry.get().strip()
        values = [["ID", "Tên", "Tác giả", "Số trang", "Năm xuất bản", "Trạng thái", "Chủng loại"]]

        for book in search_books_in_store(keyword):
            values.append([
                str(book[0]) if book[0] is not None else "-",
                book[1] or "-",
                book[2] or "-",
                str(book[3]) if book[3] is not None else "-",
                str(book[4]) if book[4] is not None else "-",
                status_text(book[5]) if book[5] is not None else "-",
                book[6] or "-"
            ])

        if len(values) == 1:
            values.append(["-", "Không tìm thấy sách", "-", "-", "-", "-", "-"])

        # Xoá bảng cũ nếu có
        global book_table
        book_table.destroy()

        # Tạo bảng mới
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

    CTkButton(search_frame, text="Tìm kiếm", command=search_books, fg_color="#2A8C55", hover_color="#207244").pack(side="left")

    # --- Bảng dữ liệu ---
    table_container = CTkScrollableFrame(view_books_frame)
    table_container.pack(fill="both", expand=True, padx=10, pady=10)

    global book_table
    book_table = CTkTable(
        master=table_container,
        values=[["ID", "Tên", "Tác giả", "Số trang", "Năm xuất bản", "Trạng thái", "Chủng loại"]],
        colors=["#FAFAFA", "#EEEEEE"],
        header_color="#361035",
        hover_color="#E0E0E0",
        corner_radius=6,
    )
    book_table.edit_row(0, text_color="white")
    book_table.pack(fill="both", expand=True)

    frames["view_books"] = view_books_frame

    # --- Cập nhật bảng khi chuyển giao diện ---
    def update_table():
        values = [["ID", "Tên", "Tác giả", "Số trang", "Năm xuất bản", "Trạng thái", "Chủng loại"]]
        books = get_all_books()

        if books:
            for book in books:
                values.append([
                    str(book[0]) if book[0] is not None else "-",
                    book[1] or "-",
                    book[2] or "-",
                    str(book[3]) if book[3] is not None else "-",
                    str(book[4]) if book[4] is not None else "-",
                    status_text(book[5]) if book[5] is not None else "-",
                    book[6] or "-"
                ])
        else:
            values.append(["-", "Không có sách", "-", "-", "-", "-", "-"])
        
        # Xoá bảng cũ nếu có
        global book_table
        if book_table is not None:
            book_table.destroy()

        # Tạo bảng mới
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

    # Sidebar buttons
    button_style = dict(
        fg_color="transparent",
        font=("Segoe UI", 14),
        text_color="white",
        hover_color="#8844aa",
        anchor="w",
        corner_radius=8,
    )
    padding = dict(anchor="center", ipady=6, pady=6, fill="x", padx=16)

    CTkButton(sidebar_frame, text="📚 Thêm sách", command=lambda: show_frame("add_book"), **button_style).pack(**padding)
    CTkButton(sidebar_frame, text="🗑️ Xoá sách", command=lambda: show_frame("delete_book"), **button_style).pack(**padding)
    CTkButton(sidebar_frame, text="✏️ Cập nhật sách", command=lambda: show_frame("update_book"), **button_style).pack(**padding)
    CTkButton(sidebar_frame, text="📋 Xem danh sách", command=lambda: show_frame("view_books"), **button_style).pack(**padding)

    show_frame("add_book")
    app.mainloop()
