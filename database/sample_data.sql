-- Insert sample products
INSERT INTO products (name, category, price, stock) VALUES
('ノートパソコン', '電子機器', 89800, 15),
('ワイヤレスマウス', '電子機器', 3980, 50),
('USBメモリ 32GB', '電子機器', 1280, 100),
('オフィスチェア', '家具', 15800, 8),
('デスク', '家具', 29800, 5),
('ボールペン（10本セット）', '文房具', 580, 200),
('ノート A4', '文房具', 280, 150),
('コーヒーメーカー', '家電', 12800, 12),
('電子レンジ', '家電', 18900, 7),
('スマートフォンケース', 'アクセサリー', 1980, 80);

-- Insert sample customers
INSERT INTO customers (name, email) VALUES
('田中太郎', 'tanaka@example.com'),
('山田花子', 'yamada@example.com'),
('佐藤次郎', 'sato@example.com'),
('鈴木美咲', 'suzuki@example.com'),
('高橋健一', 'takahashi@example.com');

-- Insert sample orders (with dates in the last 2 weeks)
INSERT INTO orders (customer_id, product_id, quantity, order_date, total_price) VALUES
(1, 1, 1, datetime('now', '-10 days'), 89800),
(2, 2, 2, datetime('now', '-9 days'), 7960),
(3, 6, 3, datetime('now', '-8 days'), 1740),
(1, 4, 1, datetime('now', '-7 days'), 15800),
(4, 3, 5, datetime('now', '-6 days'), 6400),
(5, 8, 1, datetime('now', '-5 days'), 12800),
(2, 10, 4, datetime('now', '-4 days'), 7920),
(3, 7, 10, datetime('now', '-3 days'), 2800),
(4, 9, 1, datetime('now', '-2 days'), 18900),
(5, 5, 1, datetime('now', '-1 days'), 29800);