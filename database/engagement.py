from database.database import BaseTable
from sqlalchemy.exc import SQLAlchemyError


class Engagement(BaseTable):
    def __init__(self, drop=False):
        super().__init__()
        self.table_name = 'engagements'
        
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
                    `engagement_id` INT PRIMARY KEY AUTO_INCREMENT,
                    `post_id` INT,
                    `likes_count` INT,
                    `comments_count` INT,
                    `shares_count` INT,
                    `video_completion_rate` FLOAT,
                    FOREIGN KEY (`post_id`) REFERENCES `posts`(`post_id`)
                );
                """
                self.execute_query(query)
                print(f"Table `{self.table_name}` created successfully.")
            
        except SQLAlchemyError as e:
            print(f"Error creating table `{self.table_name}`: {e}")
            raise  

        except Exception as e:
            print(f"Unexpected error creating table `{self.table_name}`: {e}")
            raise  

    def write(self, post_id, likes_count, comments_count, shares_count, video_completion_rate):
        query = f"""
        INSERT INTO `{self.table_name}` (`post_id`, `likes_count`, `comments_count`, `shares_count`, `video_completion_rate`)
        VALUES (:post_id, :likes_count, :comments_count, :shares_count, :video_completion_rate);
        """
        params = {
            'post_id': post_id,
            'likes_count': likes_count,
            'comments_count': comments_count,
            'shares_count': shares_count,
            'video_completion_rate': video_completion_rate
        }
        self.execute_query(query, params)

    def read(self):
        query = f"SELECT * FROM `{self.table_name}`;"
        return self.fetch_query(query)

    def update(self, engagement_id, likes_count=None, comments_count=None):
        query = f"""
        UPDATE `{self.table_name}` SET 
            `likes_count` = COALESCE(:likes_count, `likes_count`), 
            `comments_count` = COALESCE(:comments_count, `comments_count`)
        WHERE `engagement_id` = :engagement_id;
        """
        params = {
            'engagement_id': engagement_id,
            'likes_count': likes_count,
            'comments_count': comments_count
        }
        self.execute_query(query, params)

    def delete(self, engagement_id):
        query = f"DELETE FROM `{self.table_name}` WHERE `engagement_id` = :engagement_id;"
        params = {'engagement_id': engagement_id}
        self.execute_query(query, params)


    def drop_table(self):
        self.execute_query(f"DROP TABLE IF EXISTS `{self.table_name}`;")