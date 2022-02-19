CREATE DATABASE sXXXXXX;
USE sXXXXXX;

CREATE TABLE persons (
    cpr CHAR(11) NOT NULL,
    first_name VARCHAR(45),
    last_name VARCHAR(90),
    height TINYINT UNSIGNED,
    weight SMALLINT,
    biological_mother CHAR(11),
    biological_father CHAR(11),
    PRIMARY KEY(cpr)
);

LOAD DATA LOCAL INFILE "/home/projects/pr_course/persons.csv" INTO TABLE persons
FIELDS TERMINATED BY ",";

CREATE TABLE marriage(
    male_cpr CHAR(11) NOT NULL,
    female_cpr CHAR(11) NOT NULL,
    marriage_start CHAR(8),
    marriage_end CHAR(8),
    PRIMARY KEY(male_cpr, female_cpr)
);

LOAD DATA LOCAL INFILE "/home/projects/pr_course/marriage.csv" INTO TABLE marriage
FIELDS TERMINATED BY ",";

CREATE TABLE disease(
    cpr CHAR(11) NOT NULL,
    disease_name VARCHAR(90),
    dicovery_date CHAR(8)
);

LOAD DATA LOCAL INFILE "/home/projects/pr_course/disease.csv" INTO TABLE disease
FIELDS TERMINATED BY ",";
