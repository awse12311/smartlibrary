

-- users 資料表
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    face_recognition_image_path VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- questionnaire_books_interest 資料表 書籍類型標籤
CREATE TABLE questionnaire_books_interest (
    id SERIAL PRIMARY KEY,
    parent_interest_id INTEGER REFERENCES questionnaire_books_interest(id),
    interest_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- books 資料表
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    book_id BIGINT,
    best_book_id BIGINT,
    work_id BIGINT,
    books_count INTEGER,
    isbn VARCHAR(13),
    isbn13 BIGINT,
    title VARCHAR(500) NOT NULL,
    label BIGINT REFERENCES questionnaire_books_interest(id),--書籍類型標籤
    language_code VARCHAR(20),
    average_rating FLOAT,
    ratings_count BIGINT,
    work_ratings_count BIGINT,
    work_text_reviews_count BIGINT,
    image_url VARCHAR(500),
    small_image_url VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);



-- authors 資料表
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    book_id BIGINT REFERENCES books(id),
    author_name VARCHAR(500) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- ratings 資料表
CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    book_id BIGINT REFERENCES books(id),
    rating INTEGER,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- questionnaire_users_interest 資料表 使用者興趣標籤
CREATE TABLE questionnaire_users_interest (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    interests_id INTEGER, -- 新增 interests_id 欄位
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
-- 添加索引
CREATE INDEX idx_label ON books(label);
CREATE INDEX idx_title ON books(title);
CREATE INDEX idx_author_name ON authors(author_name);
CREATE INDEX idx_user_id ON ratings(user_id);
CREATE INDEX idx_book_id ON ratings(book_id);
CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_user_id_interests_id ON questionnaire_users_interest(user_id, interests_id);
CREATE INDEX idx_parent_interest_id ON questionnaire_books_interest(parent_interest_id);
CREATE INDEX idx_interest_name ON questionnaire_books_interest(interest_name);

-- 關聯
ALTER TABLE authors ADD CONSTRAINT fk_books_id FOREIGN KEY (book_id) REFERENCES books(id);
ALTER TABLE ratings ADD CONSTRAINT fk_books_id FOREIGN KEY (book_id) REFERENCES books(id);
ALTER TABLE ratings ADD CONSTRAINT fk_users_id FOREIGN KEY (user_id) REFERENCES users(user_id);
ALTER TABLE questionnaire_users_interest ADD CONSTRAINT fk_users_id FOREIGN KEY (user_id) REFERENCES users(user_id);
ALTER TABLE questionnaire_users_interest ADD CONSTRAINT fk_interests_id FOREIGN KEY (interests_id) REFERENCES questionnaire_books_interest(id);
