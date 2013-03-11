-- MySQL dump 10.13  Distrib 5.5.20, for osx10.6 (i386)
--
-- Host: localhost    Database: test_squidlogs
-- ------------------------------------------------------
-- Server version	5.5.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `AllRequests`
--

DROP TABLE IF EXISTS `AllRequests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AllRequests` (
  `cr_ref_number` int(10) unsigned NOT NULL,
  `cr_date_time` datetime NOT NULL,
  `cr_wpr_id` tinyint(4) DEFAULT NULL,
  `cr_lang_id` varchar(2) CHARACTER SET ucs2 DEFAULT NULL,
  `cr_content_type` varchar(4) CHARACTER SET ucs2 DEFAULT NULL,
  `cr_url` varchar(512) CHARACTER SET ucs2 NOT NULL,
  PRIMARY KEY (`cr_ref_number`,`cr_date_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 MAX_ROWS=1000000000 AVG_ROW_LENGTH=2000;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AllRequests`
--

LOCK TABLES `AllRequests` WRITE;
/*!40000 ALTER TABLE `AllRequests` DISABLE KEYS */;
/*!40000 ALTER TABLE `AllRequests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Filtered`
--

DROP TABLE IF EXISTS `Filtered`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Filtered` (
  `f_ref_number` int(10) unsigned NOT NULL,
  `f_date_time` datetime NOT NULL,
  `f_wpr_id` tinyint(4) DEFAULT NULL,
  `f_lang_id` varchar(2) CHARACTER SET ucs2 DEFAULT NULL,
  `f_ns_id` tinyint(4) DEFAULT NULL,
  `f_title` varchar(512) CHARACTER SET ucs2 DEFAULT NULL,
  `f_action_id` tinyint(4) DEFAULT NULL,
  `f_resp_time` int(11) DEFAULT NULL,
  `f_rm_id` tinyint(4) DEFAULT NULL,
  `f_md5_hash` char(32) DEFAULT NULL,
  PRIMARY KEY (`f_ref_number`,`f_date_time`),
  KEY `ind_f_wpr_id` (`f_wpr_id`),
  KEY `ind_f_lang_id` (`f_lang_id`),
  KEY `ind_f_ns_id` (`f_ns_id`),
  KEY `ind_f_action_id` (`f_action_id`),
  KEY `ind_f_rm_id` (`f_rm_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 MAX_ROWS=1000000000 AVG_ROW_LENGTH=2000;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `Searches`
--

DROP TABLE IF EXISTS `Searches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Searches` (
  `f_ref_number` int(10) unsigned NOT NULL,
  `f_date_time` datetime NOT NULL,
  `f_lang_id` varchar(2) CHARACTER SET ucs2 DEFAULT NULL,
  `f_search` varchar(30) CHARACTER SET ucs2 DEFAULT NULL,
  `f_md5_hash` char(32) DEFAULT NULL,
  PRIMARY KEY (`f_ref_number`,`f_date_time`),
  KEY `ind_f_lang_id` (`f_lang_id`),
  KEY `ind_f_md5_hash` (`f_md5_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 MAX_ROWS=1000000000 AVG_ROW_LENGTH=2000;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `filteredActions`
--

DROP TABLE IF EXISTS `filteredActions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filteredActions` (
  `wpr_id` tinyint(3) unsigned NOT NULL,
  `action_id` tinyint(3) unsigned NOT NULL,
  `action_name` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`wpr_id`,`action_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filteredActions`
--

LOCK TABLES `filteredActions` WRITE;
/*!40000 ALTER TABLE `filteredActions` DISABLE KEYS */;
INSERT INTO `filteredActions` VALUES (0,0,'EDIT'),(0,1,'HISTORY'),(0,2,'SAVE'),(0,3,'SUBMIT'),(0,4,'SEARCH');
/*!40000 ALTER TABLE `filteredActions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filteredLanguages`
--

DROP TABLE IF EXISTS `filteredLanguages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filteredLanguages` (
  `wpr_id` tinyint(3) unsigned NOT NULL,
  `lang_id` varchar(2) NOT NULL,
  `lang_name` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`wpr_id`,`lang_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filteredLanguages`
--

LOCK TABLES `filteredLanguages` WRITE;
/*!40000 ALTER TABLE `filteredLanguages` DISABLE KEYS */;
INSERT INTO `filteredLanguages` VALUES (0,'DE','GERMAN'),(0,'EN','ENGLISH'),(0,'ES','SPANISH'),(0,'FR','FRENCH'),(0,'IT','ITALIAN'),(0,'JA','JAPANESE'),(0,'NL','DUTCH'),(0,'PL','POLISH'),(0,'PT','PORTUGUESE'),(0,'RU','RUSSIAN');
/*!40000 ALTER TABLE `filteredLanguages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filteredMWProjects`
--

DROP TABLE IF EXISTS `filteredMWProjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filteredMWProjects` (
  `wpr_id` tinyint(3) unsigned NOT NULL,
  `wpr_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`wpr_id`),
  KEY `wpr_ind_name` (`wpr_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filteredMWProjects`
--

LOCK TABLES `filteredMWProjects` WRITE;
/*!40000 ALTER TABLE `filteredMWProjects` DISABLE KEYS */;
INSERT INTO `filteredMWProjects` VALUES (0,'WIKIPEDIA');
/*!40000 ALTER TABLE `filteredMWProjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filteredNNSS`
--

DROP TABLE IF EXISTS `filteredNNSS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filteredNNSS` (
  `wpr_id` tinyint(3) unsigned NOT NULL,
  `ns_id` tinyint(3) unsigned NOT NULL,
  `ns_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`wpr_id`,`ns_id`),
  KEY `ns_ind_name` (`ns_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filteredNNSS`
--

LOCK TABLES `filteredNNSS` WRITE;
/*!40000 ALTER TABLE `filteredNNSS` DISABLE KEYS */;
INSERT INTO `filteredNNSS` VALUES (0,0,'ARTICLE'),(0,2,'ARTICLE_TALK'),(0,1,'INDEX'),(0,5,'SPECIAL'),(0,3,'USER'),(0,4,'USER_TALK');
/*!40000 ALTER TABLE `filteredNNSS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filteredReqMethods`
--

DROP TABLE IF EXISTS `filteredReqMethods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filteredReqMethods` (
  `wpr_id` tinyint(3) unsigned NOT NULL,
  `rm_id` tinyint(3) unsigned NOT NULL,
  `rm_name` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`wpr_id`,`rm_id`),
  KEY `rm_ind_name` (`rm_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filteredReqMethods`
--

LOCK TABLES `filteredReqMethods` WRITE;
/*!40000 ALTER TABLE `filteredReqMethods` DISABLE KEYS */;
INSERT INTO `filteredReqMethods` VALUES (0,6,'CONNECT'),(0,0,'GET'),(0,1,'HEAD'),(0,3,'LOCK'),(0,4,'NONE'),(0,5,'OPTIONS'),(0,2,'POST'),(0,7,'PROPFIND'),(0,8,'PURGE'),(0,9,'PUT');
/*!40000 ALTER TABLE `filteredReqMethods` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-03-08 12:25:07
