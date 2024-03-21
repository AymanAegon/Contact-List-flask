-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS contact_db;
CREATE USER IF NOT EXISTS 'dev_user'@'localhost' IDENTIFIED BY 'dev_pwd';
GRANT ALL PRIVILEGES ON `contact_db`.* TO 'dev_user'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'dev_user'@'localhost';
FLUSH PRIVILEGES;