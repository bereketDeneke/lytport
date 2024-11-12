from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from database.comments import Comment
from database.follower import Follower
from database.engagement import Engagement 
from database.post import Post
from database.user import User
from database.database import Database

app = FastAPI()

# todo: hanlding d/t scenarios: cheacking for existing data to avoid data duplication/collision
#           :user Table: user_name is unique
            # the rest of the tables they have their own unique ID 
 

# Post model for request/response
class PostModel(BaseModel):
    user_id: int
    media_type: str
    media_url: str
    caption: Optional[str] = None

# Post instance
post_table = Post()

# --- Endpoints ---

# 1. Retrieve a list of all posts
@app.get("/posts/", response_model=List[PostModel])
def get_all_posts():
    try:
        posts = post_table.read_all()
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found")
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 2. Retrieve a single post by its ID
@app.get("/posts/{post_id}", response_model=PostModel)
def get_post(post_id: int):
    try:
        post = post_table.read_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail=f"Post with ID {post_id} not found")
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 3. Create a new post
@app.post("/posts/", response_model=PostModel)
def create_post(post: PostModel):
    try:
        # Validate foreign key (user_id exists) internally
        post_table.write(post.user_id, post.media_type, post.media_url, post.caption)
        return post
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Foreign key constraint failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 4. Update an existing post by ID
@app.put("/posts/{post_id}", response_model=PostModel)
def update_post(post_id: int, updated_post: PostModel):
    try:
        # Check if the post exists
        existing_post = post_table.read_by_id(post_id)
        if not existing_post:
            raise HTTPException(status_code=404, detail=f"Post with ID {post_id} not found")

        # Update the post
        post_table.update(post_id, updated_post.caption)
        return updated_post
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Foreign key constraint failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 5. Delete a post by ID
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    try:
        # Check if the post exists
        existing_post = post_table.read_by_id(post_id)
        if not existing_post:
            raise HTTPException(status_code=404, detail=f"Post with ID {post_id} not found")

        # Delete the post
        post_table.delete(post_id)
        return {"status": "success", "message": f"Post with ID {post_id} has been deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# User model for request/response
class UserModel(BaseModel):
    user_id:int
    username: str
    bio: Optional[str] = None
    followers_count: int
    following_count: int
    location: str
    is_influential: bool

# User instance
user_table = User()


# 1. Retrieve a list of all users
@app.get("/users/", response_model=List[UserModel])
def get_all_users(limit: Optional[int] = 10):
    try:
        users = user_table.read_all(limit)
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# [urgent] todo: create a postman request for this one
# 2. Retrieve a single user by ID
@app.get("/users/{user_id}", response_model=UserModel)
def get_user(user_id: int):
    try:
        user = user_table.read_by_id(user_id)
       
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 3. Create a new user
@app.post("/users/", response_model=UserModel)
def create_user(user: UserModel):
    try:
         # Check if the username already exists
        if user_table.check_username_exists(user.username):
            raise HTTPException(status_code=400, detail="Username already taken")
        
        user_table.write(user.user_id,user.username, user.bio, user.followers_count, user.following_count, user.location, user.is_influential)
        return user
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

class updateModel(BaseModel):
    username: str
    bio: Optional[str] = None


# 4. Update an existing user by ID
@app.put("/users/{user_id}", response_model=updateModel)
def update_user(user_id: int, updated_user: updateModel):
    try:
        # Check if the user exists
        existing_user = user_table.read_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

        # Update the user
        user_table.update(user_id, updated_user.username, updated_user.bio)# updated_user.followers_count, updated_user.following_count, updated_user.location, updated_user.is_influential)
        return updated_user
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Username conflict or invalid update")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# [urgent] todo: create a postman request for this one
# 5. Delete a user by ID
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        # Check if the user exists
        existing_user = user_table.read_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

        # Delete the user
        user_table.delete(user_id)
        return {"status": "success", "message": f"User with ID {user_id} has been deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Engagement model for request/response
class EngagementModel(BaseModel):
    post_id: int
    likes_count: int
    comments_count: int
    shares_count: int
    video_completion_rate: float

# Engagement instance
engagement_table = Engagement()

# --- Endpoints ---

# 1. Retrieve a list of all engagements
@app.get("/engagements/", response_model=List[EngagementModel])
def get_all_engagements():
    try:
        engagements = engagement_table.read_all()
        if not engagements:
            raise HTTPException(status_code=404, detail="No engagements found")
        return engagements
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 2. Retrieve a single engagement by ID
@app.get("/engagements/{engagement_id}", response_model=EngagementModel)
def get_engagement(engagement_id: int):
    try:
        engagement = engagement_table.read_by_id(engagement_id)
        if not engagement:
            raise HTTPException(status_code=404, detail=f"Engagement with ID {engagement_id} not found")
        return engagement
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 3. Create a new engagement
@app.post("/engagements/", response_model=EngagementModel)
def create_engagement(engagement: EngagementModel):
    try:
        # Validate foreign key (post_id exists) internally
        engagement_table.write(engagement.post_id, engagement.likes_count, engagement.comments_count, engagement.shares_count, engagement.video_completion_rate)
        return engagement
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Foreign key constraint failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 4. Update an existing engagement by ID
@app.put("/engagements/{engagement_id}", response_model=EngagementModel)
def update_engagement(engagement_id: int, updated_engagement: EngagementModel):
    try:
        # Check if the engagement exists
        existing_engagement = engagement_table.read_by_id(engagement_id)
        if not existing_engagement:
            raise HTTPException(status_code=404, detail=f"Engagement with ID {engagement_id} not found")

        # Update the engagement
        engagement_table.update(engagement_id, updated_engagement.likes_count, updated_engagement.comments_count)
        return updated_engagement
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 5. Delete an engagement by ID
@app.delete("/engagements/{engagement_id}")
def delete_engagement(engagement_id: int):
    try:
        # Check if the engagement exists
        existing_engagement = engagement_table.read_by_id(engagement_id)
        if not existing_engagement:
            raise HTTPException(status_code=404, detail=f"Engagement with ID {engagement_id} not found")

        # Delete the engagement
        engagement_table.delete(engagement_id)
        return {"status": "success", "message": f"Engagement with ID {engagement_id} has been deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Follower model for request/response
class FollowerModel(BaseModel):
    user_id: int
    follower_user_id: int

# Follower instance
follower_table = Follower()

# --- Endpoints ---

# 1. Retrieve a list of all followers
@app.get("/followers/", response_model=List[FollowerModel])
def get_all_followers():
    try:
        followers = follower_table.read_all()
        if not followers:
            raise HTTPException(status_code=404, detail="No followers found")
        return followers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 2. Retrieve a single follower by ID
@app.get("/followers/{follower_id}", response_model=FollowerModel)
def get_follower(follower_id: int):
    try:
        follower = follower_table.read_by_id(follower_id)
        if not follower:
            raise HTTPException(status_code=404, detail=f"Follower with ID {follower_id} not found")
        return follower
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 3. Create a new follower
@app.post("/followers/", response_model=FollowerModel)
def create_follower(follower: FollowerModel):
    try:
        # Validate foreign key (user_id and follower_user_id exist) internally
        follower_table.write(follower.user_id, follower.follower_user_id)
        return follower
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Foreign key constraint failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 4. Delete a follower by ID
@app.delete("/followers/{follower_id}")
def delete_follower(follower_id: int):
    try:
        # Check if the follower exists
        existing_follower = follower_table.read_by_id(follower_id)
        if not existing_follower:
            raise HTTPException(status_code=404, detail=f"Follower with ID {follower_id} not found")

        # Delete the follower
        follower_table.delete(follower_id)
        return {"status": "success", "message": f"Follower with ID {follower_id} has been deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

