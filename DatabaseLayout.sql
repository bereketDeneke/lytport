-- Drop tables if they already exist
DROP TABLE IF EXISTS Comment;
DROP TABLE IF EXISTS Engagement;
DROP TABLE IF EXISTS Follower;
DROP TABLE IF EXISTS Post;
DROP TABLE IF EXISTS User;

-- Table: User
CREATE TABLE User (
    user_id INT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    bio TEXT,
    followers_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    location VARCHAR(255),
    is_influential BOOLEAN DEFAULT FALSE
);

-- Table: Post
CREATE TABLE Post (
    post_id INT PRIMARY KEY,
    user_id INT,
    media_type VARCHAR(50),
    media_url VARCHAR(255),
    caption TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Table: Follower
CREATE TABLE Follower (
    follower_id INT PRIMARY KEY,
    user_id INT,
    follower_user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (follower_user_id) REFERENCES User(user_id)
);

-- Table: Engagement
CREATE TABLE Engagement (
    engagement_id INT PRIMARY KEY,
    post_id INT,
    likes_count INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    shares_count INT DEFAULT 0,
    video_completion_rate FLOAT DEFAULT 0,
    FOREIGN KEY (post_id) REFERENCES Post(post_id)
);

-- Table: Comment
CREATE TABLE Comment (
    comment_id INT PRIMARY KEY,
    post_id INT,
    user_id INT,
    message TEXT,
    like_count INT DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES Post(post_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);
