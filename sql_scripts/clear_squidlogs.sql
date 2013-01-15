DROP DATABASE IF EXISTS squidlogs;
CREATE DATABASE squidlogs DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL PRIVILEGES ON `squidlogs` . * TO 'ajreinoso'@'localhost' WITH GRANT OPTION ;
GRANT ALL PRIVILEGES ON `squidlogs` . * TO 'ajreinoso'@'%' WITH GRANT OPTION ;