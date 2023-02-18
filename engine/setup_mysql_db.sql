-- Setting up the sql db
CREATE DATABASE IF NOT EXISTS {tech-mavericks};
CREATE USER IF NOT EXISTS '{nuru}'@'localhost' IDENTIFIED BY '{postgres}';
GRANT ALL PRIVILEGES ON mavericks . * TO '{nuru}'@'localhost';
GRANT SELECT ON performance_schema . * TO '{nuru}'@'localhost';
