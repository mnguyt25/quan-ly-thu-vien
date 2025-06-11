create database Library;

CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(100) NOT NULL,
    role ENUM('Quản trị viên', 'Người dùng') NOT NULL -- chỉ nhập một trong hai giá trị cố định
);

insert into users (username, password, role) value ("admin", "123", "Quản trị viên");

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    ten_sach TEXT NOT NULL,
    tac_gia TEXT NOT NULL,
    so_trang INTEGER,
    nam_xuat_ban INTEGER,
    trang_thai INTEGER DEFAULT 0,
    chung_loai TEXT
);

CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    ten_thanh_vien TEXT NOT NULL
);

CREATE TABLE borrowings (
    id SERIAL PRIMARY KEY,
    id_thanh_vien INTEGER REFERENCES members(id) ON DELETE CASCADE,
    id_sach INTEGER REFERENCES books(id) ON DELETE CASCADE,
    ngay_muon DATE NOT NULL,
    ngay_tra DATE,
    han_tra DATE
);
SELECT * FROM books;
SELECT * FROM members;
SELECT * FROM borrowings;
select * from users;
