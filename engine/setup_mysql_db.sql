-- Setting up the sql db
CREATE DATABASE IF NOT EXISTS {db_name};
CREATE USER IF NOT EXISTS '{username}'@'localhost' IDENTIFIED BY '{password}';
GRANT ALL PRIVILEGES ON maverics . * TO '{username}'@'localhost';
GRANT SELECT ON performance_schema . * TO '{username}'@'localhost';
