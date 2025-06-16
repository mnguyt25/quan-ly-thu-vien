def register():
        username = entry_new_user.get()
        password = entry_new_pass.get()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ")
            return

        if db.fetch_one("SELECT * FROM users WHERE username = %s", (username,)):
            messagebox.showerror("Trùng tên", "Tên đăng nhập đã tồn tại")
            return

        db.execute_query(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, 'Public')",
            (username, password),
        )

        messagebox.showinfo("Thành công", "Đăng ký thành công!")
        reg_win.destroy()

    tk.Button(frame, text="Đăng ký", command=register).pack(pady=15)