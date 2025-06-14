import tkinter as tk

# ======= Giao diện Quản trị viên =======
def open_admin_interface():
    window = tk.Tk()
    window.title("Giao diện Quản trị viên")
    window.geometry("1200x600")
    try:
        window.iconbitmap("books_icon.ico")
    except:
        pass
    
    # === Menu Bar ===
    menubar = tk.Menu(window)

    

    # Thoát
    menubar.add_command(label="Thoát", command=window.destroy)

    window.config(menu=menubar)

    tk.Label(window, text="Quản lý thư viện", font=("Arial", 16)).pack(pady=20)
    
    window.mainloop()