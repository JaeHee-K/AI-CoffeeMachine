-- file name : coffee.sql
-- pwd : /ISIA_coffee/app/schema/coffee.sql

CREATE DATABASE ISIADB default CHARACTER SET UTF8;

use ISIADB;

CREATE TABLE coffee(centroid_1 FLOAT UNSIGNED NOT NULL, centroid_2 FLOAT UNSIGNED NOT NULL,
    density INT UNSIGNED NOT NULL
    ) CHARSET=utf8;