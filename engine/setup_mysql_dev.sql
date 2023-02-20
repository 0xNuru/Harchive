-- Setting up the sql db
CREATE DATABASE IF NOT EXISTS maverics;
CREATE USER IF NOT EXISTS 'dev'@'localhost' IDENTIFIED BY 'devroot';
GRANT ALL PRIVILEGES ON maverics . * TO 'dev'@'localhost';
GRANT SELECT ON performance_schema . * TO 'dev'@'localhost';
