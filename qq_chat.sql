-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: localhost    Database: qq_chat
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.16.04.1

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
-- Table structure for table `friend`
--

DROP TABLE IF EXISTS `friend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `friend` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(12) NOT NULL,
  `f_account` varchar(12) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friend`
--

LOCK TABLES `friend` WRITE;
/*!40000 ALTER TABLE `friend` DISABLE KEYS */;
INSERT INTO `friend` VALUES (17,'123456','132'),(18,'132','123456'),(21,'132','www'),(22,'www','132'),(27,'111','mmm'),(28,'mmm','111'),(31,'132','111'),(32,'111','132'),(33,'mmm','132'),(34,'132','mmm');
/*!40000 ALTER TABLE `friend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groupMember`
--

DROP TABLE IF EXISTS `groupMember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groupMember` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `groupName` varchar(12) NOT NULL,
  `member` varchar(12) NOT NULL,
  `img` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groupMember`
--

LOCK TABLES `groupMember` WRITE;
/*!40000 ALTER TABLE `groupMember` DISABLE KEYS */;
INSERT INTO `groupMember` VALUES (1,'AID1806','111','5.jpg'),(2,'AID1806','aaa','5.jpg'),(3,'AID1806','123456','5.jpg'),(4,'AID1806','www','5.jpg'),(5,'Python交流群','111','6.jpg'),(6,'Python交流群','d','6.jpg'),(7,'wtawtt','111','12.jpg'),(8,'chat','111','4.jpg'),(18,'hhh','111','22.jpg'),(19,'mmm','111','19.jpg'),(20,'bbb','132','25.jpg'),(21,'bbb','111','25.jpg'),(22,'chat','132','4.jpg'),(23,'chat','123456','4.jpg'),(24,'chat','mmm','4.jpg'),(25,'jk','132','10.jpg');
/*!40000 ALTER TABLE `groupMember` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(12) NOT NULL,
  `passwd` varchar(16) NOT NULL,
  `name` varchar(16) NOT NULL,
  `img` varchar(12) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'123456','123456','yxt','2.jpg',NULL),(2,'13572468','111111','wfs','7.jpg',NULL),(3,'1372930009','123456','小王','3.jpg',NULL),(4,'111','111','qqq','11.jpg',NULL),(5,'www','www','www','10.jpg',NULL),(6,'132','132','kkk','19.jpg',NULL),(7,'eee','eee','eee','14.jpg',NULL),(8,'ddd','ddd','ddd','11.jpg',NULL),(9,'d','d','d','18.jpg',NULL),(10,'ggg','ggg','ggg','13.jpg',NULL),(11,'bbb','bbb','bbb','1.jpg',NULL),(12,'ccc','ccc','ccc','2.jpg',NULL),(13,'zz','zz','zz','0.jpg',NULL),(14,'qww','qww','qww','1.jpg',NULL),(15,'zzz','zzz','zzz','22.jpg',NULL),(16,'vvvv','vvv','vvv','9.jpg',NULL),(17,'ttt','ttt','ttt','8.jpg',NULL),(18,'mmm','mmm','mmm','11.jpg',NULL),(19,'aaa','aaa','aaa','18.jpg',NULL),(20,'uuu','uuu','uuu','0.jpg',NULL),(21,'jjj','jjj','jjj','18.jpg',NULL),(22,'xxx','xxx','xxx','15.jpg',NULL),(23,'kkkk','kkk','kkkk','17.jpg',NULL),(24,'bf','bf','bf','11.jpg',NULL),(25,'45678932','rrr','rrr','4.jpg',NULL),(26,'69485231','ttt','ttt','15.jpg',NULL),(27,'96137548','lll','lll','17.jpg','18271925598');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-26 15:08:54
