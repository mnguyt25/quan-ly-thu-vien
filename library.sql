-- Tạo cơ sở dữ liệu
CREATE DATABASE library;
USE library_db;

CREATE TABLE users (
    username VARCHAR(100) PRIMARY KEY,
    password VARCHAR(100) NOT NULL,
    role ENUM('admin', 'public') NOT NULL
);
drop table users
-- Thêm dữ liệu mẫu
INSERT INTO users (username, password, role) 
VALUES 
('admin@', 'admin@123', 'admin'),
('admin1', '123', 'admin'),
('user1', '456', 'public');
DELETE FROM users;


-- Tạo bảng sách
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten_sach VARCHAR(255) NOT NULL,
    tac_gia VARCHAR(255) NOT NULL,
    so_trang INT,
    nam_xuat_ban INT,
    trang_thai TINYINT DEFAULT 0,
    chung_loai VARCHAR(100)
);
DROP TABLE books;
-- Tạo bảng thành viên
CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten_thanh_vien VARCHAR(100) NOT NULL,
    FOREIGN KEY (ten_thanh_vien) REFERENCES users(username) ON DELETE CASCADE
);

-- Tạo bảng mượn sách
CREATE TABLE borrowings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_thanh_vien INT,
    id_sach INT,
    ngay_muon DATE NOT NULL,
    ngay_tra DATE,
    han_tra DATE,
    FOREIGN KEY (id_thanh_vien) REFERENCES members(id) ON DELETE CASCADE,
    FOREIGN KEY (id_sach) REFERENCES books(id) ON DELETE CASCADE
);

SHOW TABLES; 
DESCRIBE users; 
INSERT INTO books (id, title, author, available)
VALUES
(1, 'Đắc Nhân Tâm', 'Dale Carnegie', 5),
(2, 'Tuổi trẻ đáng giá bao nhiêu?', 'Rosie Nguyễn', 3),
(3, 'Harry Potter và Hòn đá Phù thủy', 'J.K. Rowling', 2),
(4, 'Lập trình Python cơ bản', 'Nguyễn Văn A', 4),
(5, 'Chuyện con mèo dạy hải âu bay', 'Luis Sepúlveda', 6);

