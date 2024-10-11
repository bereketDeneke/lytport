from database.comments import Comment
from database.follower import Follower
from database.engagment import Engagement 
from database.post import Post
from database.user import User
from database.database import Database
from sqlalchemy.exc import SQLAlchemyError

def drop_tables_in_order():
    try:
        Engagement(drop = True)
        Post(drop = True)
        Follower(drop = True)
        Comment(drop = True)
        User(drop = True)

        print("All tables dropped successfully.")

    except SQLAlchemyError as e:
        print(f"Error dropping tables: {e}")
        raise

drop_tables_in_order()

def main():
    user_db = User()
    post_db = Post()
    follower_db = Follower()
    engagement_db = Engagement()
    comment_db = Comment()

    user_db.write('john_doe', 'This is John\'s bio', 1000, 200, 'New York', True)
    post_db.write(1, 'image', 'http://imageurl.com', 'Great picture!')
    follower_db.write(1, 2)
    engagement_db.write(1, 150, 10, 5, 0.95)
    comment_db.write(1, 1, 'Nice post!', 20)
    users = user_db.read()
    print("Users:", users)

    posts = post_db.read()
    print("Posts:", posts)

    Database.close_connection()

if __name__ == "__main__":
    main()
