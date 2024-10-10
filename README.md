
# Instagram Analysis Data Model

This project is designed to analyze users' Instagram profiles and activities based on their IDs, compare them with successful creators, and provide actionable insights and real-time suggestions. The data model is structured to efficiently store and retrieve information related to user profiles, posts, engagements, and comments.

## Data Model Description

The data model consists of the following main entities:

1. **User**: Represents each Instagram user. Contains fields like `user_id`, `username`, `follower_count`, `following_count`, `bio`, and more.
2. **Post**: Stores information about each post made by the users. Includes `post_id`, `user_id`, `caption`, `likes`, `comments_count`, and `posted_at`.
3. **Follower**: Tracks data of their followers. Includes `user_id` and `follower_id`.
4. **Engagement**: Stores metrics such as likes, shares, and comments on posts. Includes `engagement_id`, `post_id`, `user_id`, and `engagement_type`.
5. **Comment**: Stores comments on each post, with fields such as `comment_id`, `post_id`, `user_id`, and `content`.

The relationships between these entities ensure that we can quickly retrieve information such as a user's posts, the engagements on each post, and the comments made by other users.

## Reasoning Behind Using SQL for This Project

We chose **SQL (Structured Query Language)** for this project due to the structured nature of the data and the need for complex queries and relationships. The data consists of multiple related entities, such as users, posts, and engagements, which benefit from SQL's ability to manage relational data efficiently. SQL databases like PostgreSQL or MySQL offer powerful querying capabilities, transaction management, and data integrity, making it a suitable choice for this project.

### Advantages of SQL for this Project:
1. **Relational Data**: SQL is ideal for handling relational data where tables are connected through foreign keys.
2. **Data Integrity**: Ensures data consistency through constraints and relationships.
3. **Complex Queries**: Supports complex joins, subqueries, and aggregations for generating insights.
4. **Scalability**: SQL databases like PostgreSQL are scalable and can handle large datasets with proper indexing and optimization.

## Database Setup Instructions

### 1. Database Configuration
Create a `.env` file in the root directory of the project and add the following details:

```
DB_SERVER=<your_db_server>
DB_NAME=<your_db_name>
DB_USER=<your_db_username>
DB_PASSWORD=<your_db_password>
```

Replace the placeholders `<your_db_server>`, `<your_db_name>`, `<your_db_username>`, and `<your_db_password>` with your actual database connection details.

### 2. Setting Up the Database
If using PostgreSQL or MySQL, create a new database with the name specified in your `.env` file. Then, connect to the database and run the following command to create necessary tables:

```bash
python database.py
```

This script will establish a connection to your database and create tables such as `User`, `Post`, `Follower`, `Engagement`, and `Comment` based on the Entity-Relationship (ER) diagram.

### 3. Running the Application
Once the database is set up, run the application:

```bash
python app.py
```
