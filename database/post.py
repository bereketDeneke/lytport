from database.database import BaseTable
from sqlalchemy.exc import SQLAlchemyError

class Post(BaseTable):
    def __init__(self, drop = False):
        super().__init__()
        self.table_name = 'posts'
        
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
                    `post_id` INT PRIMARY KEY AUTO_INCREMENT,
                    `user_id` INT,
                    `media_type` VARCHAR(50),
                    `media_url` VARCHAR(255),
                    `caption` TEXT,
                    `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
                );
                """
                self.execute_query(query)

        except SQLAlchemyError as e:
            pass

    def write(self, user_id, media_type, media_url, caption):
        query = f"""
        INSERT INTO `{self.table_name}` (`user_id`, `media_type`, `media_url`, `caption`, `timestamp`)
        VALUES (:user_id, :media_type, :media_url, :caption, CURRENT_TIMESTAMP);
        """
        params = {
            'user_id': user_id,
            'media_type': media_type,
            'media_url': media_url,
            'caption': caption
        }
        self.execute_query(query, params)

    def read(self):
        query = f"SELECT * FROM `{self.table_name}`;"
        return self.fetch_query(query)

    def update(self, post_id, caption=None):
        query = f"""
        UPDATE `{self.table_name}` SET 
            `caption` = COALESCE(:caption, `caption`)
        WHERE `post_id` = :post_id;
        """
        params = {'post_id': post_id, 'caption': caption}
        self.execute_query(query, params)

    def delete(self, post_id):
        query = f"DELETE FROM `{self.table_name}` WHERE `post_id` = :post_id;"
        params = {'post_id': post_id}
        self.execute_query(query, params)


    def drop_table(self):
        self.execute_query(f"DROP TABLE IF EXISTS `{self.table_name}`;")