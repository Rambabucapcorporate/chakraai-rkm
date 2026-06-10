-- MySQL Database Schema for RKM Academic Assistant
-- Database: pkf

-- 1. Create the database (if not exists)
CREATE DATABASE IF NOT EXISTS studentDb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE studentDb;

-- 2. Users Table (Handles both Registration and Login)
-- Removed full_name per user request.
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_email (email)
) ENGINE=InnoDB;

-- ==========================================================
-- COMMON SQL QUERIES (FOR REFERENCE)
-- ==========================================

-- Register a new user
-- INSERT INTO users (email, hashed_password) 
-- VALUES ('user@example.com', '$2b$12$hashedpassword...');

-- Find a user by email
-- SELECT * FROM users WHERE email = 'user@example.com';
