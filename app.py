from database.comments import Comment
from database.follower import Follower
from database.engagement import Engagement 
from database.post import Post
from database.user import User
from database.database import Database
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import pandas as pd

user_db = User()
post_db = Post()
comment_db = Comment()
engagement_db = Engagement()
follower_db = Follower()

def drop_tables_in_order():
    try:
        # Get a connection from the engine
        with Database.get_engine().connect() as connection:
            # Disable foreign key checks to allow dropping tables with dependencies
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        
            # Drop tables in reverse order of foreign key dependencies
            Engagement(drop=True)  # No foreign key dependencies
            Comment(drop=True)     # Depends on Post and User
            Follower(drop=True)    # Depends on User
            Post(drop=True)        # Depends on User
            User(drop=True)        # Independent

            print("All tables dropped successfully.")
        
            # Re-enable foreign key checks after dropping tables
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    except SQLAlchemyError as e:
        print(f"Error dropping tables: {e}")
        raise


def load_data_from_csv(file_path, table_class):
    """
    General function to load data from CSV into the corresponding table.
    
    Args:
    file_path (str): Path to the CSV file.
    table_class (BaseTable): The class corresponding to the table (User, Post, Comment, etc.)
    
    """
    # Read the CSV data using pandas
    data_df = pd.read_csv(file_path)
    
    # Initialize the table object
    table_obj = table_class()


def load_users_from_csv(file_path):
    data_df = pd.read_csv(file_path)
    user_db = User()

    for _, row in data_df.iterrows():
        user_db.write(
            user_id=int(row['user_id']) + 8,
            username=row['username'], 
            bio=row['bio'], 
            followers_count=row['followers_count'], 
            following_count=row['following_count'], 
            location=row['location'], 
            is_influential=row['is_influential']
        )
    print(f"Loaded {len(data_df)} records into the User table.")

def load_posts_from_csv(file_path):
    data_df = pd.read_csv(file_path)
    post_db = Post()

    for _, row in data_df.iterrows():
        post_db.write(
            user_id=int(row['user_id']) + 8, 
            media_type=row['media_type'], 
            media_url=row['media_url'], 
            caption=row['caption']
        )
    print(f"Loaded {len(data_df)} records into the Post table.")


def load_comments_from_csv(file_path):
    data_df = pd.read_csv(file_path)
    comment_db = Comment()

    for _, row in data_df.iterrows():
        comment_db.write(
            post_id=row['post_id'], 
            user_id=int(row['user_id']) + 8, 
            message=row['message'], 
            like_count=row['like_count']
        )
    print(f"Loaded {len(data_df)} records into the Comment table.")

def load_engagements_from_csv(file_path):
    data_df = pd.read_csv(file_path)
    engagement_db = Engagement()

    for _, row in data_df.iterrows():
        engagement_db.write(
            post_id=row['post_id'], 
            likes_count=row['likes_count'], 
            comments_count=row['comments_count'], 
            shares_count=row['shares_count'], 
            video_completion_rate=row['video_completion_rate']
        )
    print(f"Loaded {len(data_df)} records into the Engagement table.")

def main():
    # drop_tables_in_order()

    # Load data into each table from the corresponding CSV file
    load_users_from_csv('data/Dummy_Users_Data.csv')
    load_posts_from_csv('data/Dummy_Posts_Data.csv')
    load_comments_from_csv('data/Dummy_Comments_Data.csv')
    load_engagements_from_csv('data/Dummy_Engagement_Data.csv')

    # Optionally, read and print data for validation
    user_db = User()
    print("Users:", user_db.read())

    post_db = Post()
    print("Posts:", post_db.read())

    comment_db = Comment()
    print("Comments:", comment_db.read())

    engagement_db = Engagement()
    print("Engagements:", engagement_db.read())

    Database.close_connection()

if __name__ == "__main__":
    main()

