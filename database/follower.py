from database.database import BaseTable

class Follower(BaseTable):
    def __init__(self, drop=False):
        super().__init__()
        self.table_name = 'followers'

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
                    `follower_id` INT PRIMARY KEY AUTO_INCREMENT,
                    `user_id` INT,
                    `follower_user_id` INT,
                    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`),
                    FOREIGN KEY (`follower_user_id`) REFERENCES `users`(`user_id`)
                );
                """
                self.execute_query(query)
        except ... as e:
            pass

    def write(self, user_id, follower_user_id):
        query = f"""
        INSERT INTO `{self.table_name}` (`user_id`, `follower_user_id`)
        VALUES (:user_id, :follower_user_id);
        """
        params = {'user_id': user_id, 'follower_user_id': follower_user_id}
        self.execute_query(query, params)

    def read(self):
        query = f"SELECT * FROM `{self.table_name}`;"
        return self.fetch_query(query)

    def delete(self, follower_id):
        query = f"DELETE FROM `{self.table_name}` WHERE `follower_id` = :follower_id;"
        params = {'follower_id': follower_id}
        self.execute_query(query, params)

    def drop_table(self):
        self.execute_query(f"DROP TABLE IF EXISTS `{self.table_name}`;")