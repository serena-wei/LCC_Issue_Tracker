-- Disable foreign key checks to avoid foreign key issues when dropping tables
SET foreign_key_checks = 0;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS issues;
DROP TABLE IF EXISTS comments;

-- Create the users table.
CREATE TABLE users (
    -- The AUTO_INCREMENT column is treated as NOT NULL, so there is no need to explicitly add NOT NULL.
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    -- Store bcrypt hash values as binary strings.
    password_hash CHAR(60) BINARY NOT NULL,
    email VARCHAR(320) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    profile_image VARCHAR(255),
    role ENUM('visitor', 'helper', 'admin') NOT NULL,
    status ENUM('active', 'inactive') NOT NULL
);

-- Create the issues table.
CREATE TABLE issues (
    -- The AUTO_INCREMENT column is treated as NOT NULL, so there is no need to explicitly add NOT NULL.
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    summary VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status ENUM('new', 'open', 'stalled', 'resolved') NOT NULL,
    -- ON DELETE RESTRICT: Prevent deletion of a user from the 'users' table if there are references to that 'user_id' in the issues table.
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- Create the comments table.
CREATE TABLE comments (
    -- The AUTO_INCREMENT column is treated as NOT NULL, so there is no need to explicitly add NOT NULL.
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    -- ON DELETE RESTRICT: Prevent deletion of a issue from the 'issues' table if there are references to that 'issue_id' in the comments table.
    FOREIGN KEY (issue_id) REFERENCES issues(issue_id) ON DELETE RESTRICT,
    -- ON DELETE RESTRICT: Prevent deletion of a user from the 'users' table if there are references to that 'user_id' in the comments table.
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- Enable foreign key checks
SET foreign_key_checks = 1;