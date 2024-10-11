from database.database import BaseTable

class User(BaseTable):
    def __init__(self, drop=False):
        super().__init__()
        self.table_name = 'users'
        self.execute_query("SET FOREIGN_KEY_CHECKS = 0;")
        
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
                    `user_id` INT PRIMARY KEY AUTO_INCREMENT,
                    `username` VARCHAR(255),
                    `bio` TEXT,
                    `followers_count` INT,
                    `following_count` INT,
                    `location` VARCHAR(255),
                    `is_influential` BOOLEAN
                );
                """
                self.execute_query(query)
        except Exception as e:
            pass

    def write(self, username, bio, followers_count, following_count, location, is_influential):
        query = f"""
        INSERT INTO `{self.table_name}` (`username`, `bio`, `followers_count`, `following_count`, `location`, `is_influential`)
        VALUES (:username, :bio, :followers_count, :following_count, :location, :is_influential);
        """
        params = {
            'username': username,
            'bio': bio,
            'followers_count': followers_count,
            'following_count': following_count,
            'location': location,
            'is_influential': is_influential
        }
        self.execute_query(query, params)

    def read(self):
        query = f"SELECT * FROM `{self.table_name}`;"
        return self.fetch_query(query)

    def update(self, user_id, username=None, bio=None):
        query = f"""
        UPDATE `{self.table_name}` SET 
            `username` = COALESCE(:username, `username`), 
            `bio` = COALESCE(:bio, `bio`)
        WHERE `user_id` = :user_id;
        """
        params = {'user_id': user_id, 'username': username, 'bio': bio}
        self.execute_query(query, params)

    def delete(self, user_id):
        query = f"DELETE FROM `{self.table_name}` WHERE `user_id` = :user_id;"
        params = {'user_id': user_id}
        self.execute_query(query, params)


    def drop_table(self):
        self.execute_query(f"DROP TABLE IF EXISTS `{self.table_name}`;")