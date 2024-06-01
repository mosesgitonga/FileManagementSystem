-- mock details for development purpose only
CREATE DATABASE IF NOT EXISTS fms_db;
CREATE USER IF NOT EXISTS 'fms_developer'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON fms_db.* TO 'fms_developer'@'localhost';
FLUSH PRIVILEGES;
