-- AirBnB_clone_v2 MySQL Development Setup Script
-- This script prepares a MySQL server for the project by creating a database and a user with specific privileges.

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create or update the user
-- The 'hbnb_dev' user will be created with the password 'hbnb_dev_pwd'
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant privileges to the user on the specific databases

-- 'hbnb_dev' is granted all privileges on the 'hbnb_dev_db' database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Refresh privileges to apply changes
FLUSH PRIVILEGES;

-- 'hbnb_dev' is granted SELECT privilege on the 'performance_schema' database
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Refresh privileges to apply changes
FLUSH PRIVILEGES;

-- End of script
