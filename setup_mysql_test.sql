-- AirBnB_clone_v2 MySQL Test Setup Script
-- This script prepares a MySQL server for testing by creating a database and a user with specific privileges.

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create or update the user
-- The 'hbnb_test' user will be created with the password 'hbnb_test_pwd'
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant privileges to the user on the specific databases

-- 'hbnb_test' is granted SELECT privilege on the 'performance_schema' database
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Refresh privileges to apply changes
FLUSH PRIVILEGES;

-- 'hbnb_test' is granted all privileges on the 'hbnb_test_db' database
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Refresh privileges to apply changes
FLUSH PRIVILEGES;

-- End of script
