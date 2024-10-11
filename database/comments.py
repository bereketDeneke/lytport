from .database import BaseTable

class Comment(BaseTable):
    def __init__(self, drop=False):
        super().__init__()
        self.table_name = 'comments'
        
        if drop:
            self.drop_table()
        else:
            self.create_table()

    def create_table(self):
        try:
            result = self.fetch_query(f"SHOW TABLES LIKE '{self.table_name}';")
            if not result:
                query = f"""
                CREATE TABLE `{self.table_name}` (
                    `comment_id` INT PRIMARY KEY AUTO_INCREMENT,
                    `post_id` INT,
                    `user_id` INT,
                    `message` TEXT,
                    `like_count` INT,
                    `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (`post_id`) REFERENCES `posts`(`post_id`),
                    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
                );
                """
                self.execute_query(query)

        except ... as e:
            pass

    def write(self, post_id, user_id, message, like_count):
        query = f"""
        INSERT INTO `{self.table_name}` (`post_id`, `user_id`, `message`, `like_count`, `timestamp`)
        VALUES (:post_id, :user_id, :message, :like_count, CURRENT_TIMESTAMP);
        """
        params = {
            'post_id': post_id,
            'user_id': user_id,
            'message': message,
            'like_count': like_count
        }
        self.execute_query(query, params)

    def read(self):
        query = f"SELECT * FROM `{self.table_name}`;"
        return self.fetch_query(query)

    def update(self, comment_id, message=None, like_count=None):
        query = f"""
        UPDATE `{self.table_name}` SET 
            `message` = COALESCE(:message, `message`),
            `like_count` = COALESCE(:like_count, `like_count`)
        WHERE `comment_id` = :comment_id;
        """
        params = {
            'comment_id': comment_id,
            'message': message,
            'like_count': like_count
        }
        self.execute_query(query, params)

    def delete(self, comment_id):
        query = f"DELETE FROM `{self.table_name}` WHERE `comment_id` = :comment_id;"
        params = {'comment_id': comment_id}
        self.execute_query(query, params)

    def drop_table(self):
        self.execute_query(f"DROP TABLE IF EXISTS `{self.table_name}`;")