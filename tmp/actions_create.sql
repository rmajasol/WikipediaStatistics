DROP TABLE IF EXISTS actions2012;CREATE TABLE actions2012 (day DATE,dayWeek VARCHAR(2),action TINYINT,lang VARCHAR(2),ns TINYINT,count int);alter table actions2012 add index (day, dayWeek, lang, ns);