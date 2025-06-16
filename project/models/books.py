import sys, os # thêm thư mục cha vào sys.path để import được database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database import Database

def add_book_to_store(id, name, author, pages, published_year, status, category):
    db = Database()
    db.execute_query(
        """
        INSERT INTO books (id, ten_sach, tac_gia, so_trang, nam_xuat_ban, trang_thai, chung_loai)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (id, name, author, pages, published_year, status, category)
    )
    db.cursor.close()
    db.conn.close()

def delete_book_from_store(book_id):
    db = Database()
    query = "DELETE FROM books WHERE id = %s"
    db.cursor.execute(query, (book_id,))
    db.conn.commit()
    deleted = db.cursor.rowcount > 0
    db.cursor.close()
    db.conn.close()
    return deleted

def update_book_in_store(book_id, name=None, author=None, pages=None, published_year=None, status=None, category=None):
    updates = []
    values = []
    db = Database()

    if name:
        updates.append("ten_sach = %s")
        values.append(name)
    if author:
        updates.append("tac_gia = %s")
        values.append(author)
    if pages is not None:
        updates.append("so_trang = %s")
        values.append(pages)
    if published_year is not None:
        updates.append("nam_xuat_ban = %s")
        values.append(published_year)
    if status is not None:
        updates.append("trang_thai = %s")
        values.append(status)
    if category:
        updates.append("chung_loai = %s")
        values.append(category)

    if not updates:
        return False

    values.append(book_id)
    query = f"UPDATE books SET {', '.join(updates)} WHERE id = %s"
    db.cursor.execute(query, values)
    db.conn.commit()
    updated = db.cursor.rowcount > 0
    db.cursor.close()
    db.conn.close()
    return updated

def search_books_in_store(keyword):
    db = Database()

    if keyword.isdigit():
        # Nếu là số, tìm theo id hoặc năm xuất bản chính xác, ngoài ra vẫn tìm gần đúng theo tên và tác giả
        query = """
            SELECT * FROM books
            WHERE id = %s
            OR nam_xuat_ban = %s
            OR LOWER(ten_sach) LIKE %s
            OR LOWER(tac_gia) LIKE %s
        """
        like_keyword = f"%{keyword.lower()}%"
        db.cursor.execute(query, (int(keyword), int(keyword), like_keyword, like_keyword))
    else:
        # Nếu là chữ, chỉ tìm trong tên và tác giả (gần đúng)
        query = """
            SELECT * FROM books
            WHERE LOWER(ten_sach) LIKE %s
            OR LOWER(tac_gia) LIKE %s
        """
        like_keyword = f"%{keyword.lower()}%"
        db.cursor.execute(query, (like_keyword, like_keyword))

    results = db.cursor.fetchall()
    db.cursor.close()
    db.conn.close()
    return results

def get_all_books():
    db = Database()
    result = db.fetch_all("""
        SELECT 
            id, 
            ten_sach AS name, 
            tac_gia AS author,
            so_trang AS pages,
            nam_xuat_ban AS published_year,
            trang_thai AS status,
            chung_loai AS category
        FROM books
    """)
    db.cursor.close()
    db.conn.close()
    return result