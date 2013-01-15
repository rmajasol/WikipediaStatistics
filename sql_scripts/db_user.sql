--  
-- This file is part of the WikiSquilter program (WIKIpedia SQUId Log filTER)
-- Copyright (C) 2009 Antonio J. Reinoso.
--
-- This program is free software; you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation; either version 3, or (at your option)
-- any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.
-- 
-- Antonio J. Reinoso
-- Libresof Research Group
-- Universidad Rey Juan Carlos
-- C/ Tulipan s/n
-- 28933 Mostoles
-- Madrid (SPAIN)
-- ajreinoso@libresoft.es


/*CREATE DATABASE wsqdb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'wsquser'@'localhost' IDENTIFIED BY 'wsquser';
GRANT ALL PRIVILEGES ON `wsqdb` . * TO 'wsquser'@'localhost' WITH GRANT OPTION ;
GRANT ALL PRIVILEGES ON `wsqdb` . * TO 'wsquser'@'%' WITH GRANT OPTION ;*/


CREATE DATABASE squidlogs DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'ajreinoso'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON `squidlogs` . * TO 'ajreinoso'@'localhost' WITH GRANT OPTION ;
GRANT ALL PRIVILEGES ON `squidlogs` . * TO 'ajreinoso'@'%' WITH GRANT OPTION ;