CREATE DATABASE  IF NOT EXISTS `modlink_database` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `modlink_database`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: modlink_database
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendances`
--

DROP TABLE IF EXISTS `attendances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendances` (
  `AttendanceID` int NOT NULL AUTO_INCREMENT,
  `StudentID` varchar(12) NOT NULL,
  `Course_code` varchar(7) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Status` enum('Present','Absent','Leave','null') DEFAULT NULL,
  PRIMARY KEY (`AttendanceID`),
  KEY `ix_attendances_AttendanceID` (`AttendanceID`),
  KEY `attendances.fk1` (`StudentID`),
  KEY `attendances.fk2_idx` (`Course_code`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendances`
--

LOCK TABLES `attendances` WRITE;
/*!40000 ALTER TABLE `attendances` DISABLE KEYS */;
INSERT INTO `attendances` VALUES (101,'63070507207','CPE452','2024-01-17','null'),(102,'63070507207','CPE452','2024-01-24','null'),(103,'63070507207','CPE452','2024-01-31','null'),(104,'63070507207','CPE452','2024-02-07','null'),(105,'63070507207','CPE452','2024-02-14','null'),(106,'63070507207','CPE452','2024-02-21','null'),(107,'63070507207','CPE452','2024-02-28','null'),(108,'63070507207','CPE452','2024-03-06','null'),(109,'63070507207','CPE452','2024-03-13','null'),(110,'63070507207','CPE452','2024-03-20','null'),(111,'63070507207','CPE452','2024-03-27','null'),(112,'63070507207','CPE452','2024-04-03','null'),(113,'63070507207','CPE452','2024-04-10','null'),(114,'63070507207','CPE452','2024-04-17','null'),(115,'63070507207','CPE452','2024-04-24','null'),(116,'63070507207','CPE452','2024-05-01','null'),(117,'63070507207','CPE452','2024-05-08','null'),(118,'63070507207','CPE452','2024-05-15','null'),(119,'63070507207','CPE452','2024-05-22','null'),(120,'63070507207','CPE452','2024-05-29','null');
/*!40000 ALTER TABLE `attendances` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_users`
--

DROP TABLE IF EXISTS `auth_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Email` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_users_ibfk_1` (`Email`),
  CONSTRAINT `auth_users_ibfk_1` FOREIGN KEY (`Email`) REFERENCES `students` (`Email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_users`
--

LOCK TABLES `auth_users` WRITE;
/*!40000 ALTER TABLE `auth_users` DISABLE KEYS */;
INSERT INTO `auth_users` VALUES (1,'tadpong.teawm@kmutt.ac.th','$2b$12$jOqYiKJMrZrMa7EQR5d5MOJBu2r9sBrK3/lWr03tL3z6fAvjzLMIa'),(2,'john.doe@example.com','$2b$12$ELKepKJyZOFk05T7k1bNJuAUrqM61QFiuhgXHjE/m3itCSk92LYSm'),(3,'jane.smith@example.com','$2b$12$fJXzU1Jjd88A1bxJyePJKOVtOhtl5FmOHt2ZPAUEoU6Cemd2XVpOi'),(4,'michael.johnson@example.com','$2b$12$DUO8dYrE1UFudZF1nH8zpOJMWtk0NHaib.dbxps4yaJiRlF.yn/26'),(5,'emily.brown@example.com','12345678'),(6,'william.taylor@example.com','12345678'),(7,'olivia.anderson@example.com','12345678'),(8,'james.martinez@example.com','12345678'),(9,'sophia.hernandez@example.com','12345678'),(11,'emma.white@example.com','12345678'),(12,'test.test@kmutt.ac.th','$2b$12$iLh9T4Jza1LTo9mBWJv2se3oD47vi3cgwWY01Cr1ll1AHD0p0iUU6');
/*!40000 ALTER TABLE `auth_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `Course_id` int NOT NULL AUTO_INCREMENT,
  `Course_code` varchar(7) NOT NULL,
  `CourseName` varchar(70) NOT NULL,
  `instructor_name` varchar(100) NOT NULL,
  `credit` int NOT NULL,
  `level` int NOT NULL,
  `term` int NOT NULL,
  `start_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `recurrence_pattern` varchar(10) NOT NULL,
  PRIMARY KEY (`Course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'CPE452','Data Mining','Teacher_A',3,4,2,'2024-01-17','18:00:00','21:00:00','Wednesday'),(2,'CPE341','Optimization Design and Evolutionary Computing','Teacher_B',3,4,2,'2024-01-16','13:30:00','16:30:00','Tuesday'),(3,'CPE343','Object Oriented Analysis and Design','Teacher_C',3,4,2,'2024-01-16','09:30:00','12:30:00','Tuesday'),(4,'CPE393','Special Topic III: Text Analytics','Teacher_D',3,4,2,'2024-01-18','18:00:00','21:00:00','Thursday'),(5,'CPE374','Human-Computer Interaction ','Teacher_E',3,4,2,'2024-01-16','13:30:00','16:30:00','Tuesday'),(6,'CPE393','Special Topic III: Fundamentals of Cybersecurity ','Teacher_F',3,4,2,'2024-01-17','18:00:00','21:00:00','Wednesday'),(7,'CPE393','Special Topic III: Machine Learning for Data Science and Artificial ','Teacher_G',3,4,2,'2024-01-20','13:00:00','16:00:00','Saturday'),(8,'CPE375','Interactive Computing and Its Applications in Art and Sciences','Teacher_H',3,4,2,'2024-01-16','09:30:00','12:30:00','Tuesday'),(9,'CPE361','Computer Graphics','Teacher_I',3,4,2,'2024-01-16','13:30:00','16:30:00','Tuesday'),(10,'CPE464','Digital Image Processing for Copyright Protection ','Teacher_J',3,4,2,'2024-01-16','09:30:00','12:30:00','Tuesday'),(11,'CPE463','Image Processing and Computer Vision ','Teacher_K',3,4,2,'2024-01-15','09:30:00','12:30:00','Monday'),(12,'CPE371','Artificial Intelligence ','Teacher_L',3,4,2,'2024-01-18','18:00:00','21:00:00','Thursday'),(13,'CPE351','High Performance Computing and Cloud Technologies ','Teacher_M',3,4,2,'2024-01-16','13:30:00','16:30:00','Tuesday'),(14,'CPE393','Special Topic III : Quantum Programming and Computing','Teacher_N',3,4,2,'2024-01-18','13:30:00','16:30:00','Thursday'),(15,'CPE402',' Computer Engineering Project II','Teacher_O',3,3,2,'2024-01-15','13:00:00','16:00:00','Monday');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollments`
--

DROP TABLE IF EXISTS `enrollments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrollments` (
  `EnrollmentID` int NOT NULL AUTO_INCREMENT,
  `StudentID` varchar(12) DEFAULT NULL,
  `Course_code` varchar(7) DEFAULT NULL,
  `GradeID` int DEFAULT NULL,
  `EnrollmentDate` date DEFAULT NULL,
  PRIMARY KEY (`EnrollmentID`),
  KEY `enrollments.fk2_idx` (`Course_code`),
  KEY `enrollments.fk1` (`StudentID`),
  CONSTRAINT `enrollments.fk1` FOREIGN KEY (`StudentID`) REFERENCES `students` (`StudentID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollments`
--

LOCK TABLES `enrollments` WRITE;
/*!40000 ALTER TABLE `enrollments` DISABLE KEYS */;
INSERT INTO `enrollments` VALUES (13,'63070507207','CPE452',NULL,'2024-01-07');
/*!40000 ALTER TABLE `enrollments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculties`
--

DROP TABLE IF EXISTS `faculties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculties` (
  `FacultyID` int NOT NULL AUTO_INCREMENT,
  `FacultyName` varchar(50) DEFAULT NULL,
  `Department` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`FacultyID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculties`
--

LOCK TABLES `faculties` WRITE;
/*!40000 ALTER TABLE `faculties` DISABLE KEYS */;
/*!40000 ALTER TABLE `faculties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grades`
--

DROP TABLE IF EXISTS `grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades` (
  `GradeID` int NOT NULL AUTO_INCREMENT,
  `Grade` varchar(50) DEFAULT NULL,
  `GPA` float DEFAULT NULL,
  PRIMARY KEY (`GradeID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` VALUES (1,'A',4),(2,'B+',3.5),(3,'B',3),(4,'C+',2.5),(5,'C',2),(6,'D+',1.5),(7,'D',1),(8,'F',0);
/*!40000 ALTER TABLE `grades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `StudentID` varchar(12) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `Roll` varchar(10) DEFAULT NULL,
  `Year` varchar(1) DEFAULT NULL,
  `DateOfBirth` date NOT NULL,
  PRIMARY KEY (`StudentID`,`Email`),
  KEY `index2` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES ('0','emily.brown@example.com','Emily','Brown','Student','1','2005-10-03'),('0','emma.white@example.com','Emma','White','Student','4','2003-07-17'),('0','james.martinez@example.com','James','Martinez','Student','1','2003-09-08'),('0','jane.smith@example.com','Jane','Smith','Staff','2','2004-08-15'),('0','john.doe@example.com','John','Doe','Student','1','2005-05-10'),('0','michael.johnson@example.com','Michael','Johnson','Student','3','2004-02-28'),('0','olivia.anderson@example.com','Olivia','Anderson','Student','3','2004-06-25'),('0','sophia.hernandez@example.com','Sophia','Hernandez','Staff','2','2004-11-12'),('0','william.taylor@example.com','William','Taylor','Staff','2','2003-12-18'),('63070507200','test.test@kmutt.ac.th','test','test','Student','4','2544-09-28'),('63070507207','tadpong.teawm@kmutt.ac.th','Tadpong','Teawmapobsuk','Student','4','2544-09-28');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `videofiles`
--

DROP TABLE IF EXISTS `videofiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `videofiles` (
  `VideoID` int NOT NULL AUTO_INCREMENT,
  `StudentID` varchar(12) DEFAULT NULL,
  `FileName` varchar(50) DEFAULT NULL,
  `FilePath` varchar(50) DEFAULT NULL,
  `UploadDate` date DEFAULT NULL,
  PRIMARY KEY (`VideoID`),
  KEY `videofiles.fk1` (`StudentID`),
  CONSTRAINT `videofiles.fk1` FOREIGN KEY (`StudentID`) REFERENCES `students` (`StudentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `videofiles`
--

LOCK TABLES `videofiles` WRITE;
/*!40000 ALTER TABLE `videofiles` DISABLE KEYS */;
/*!40000 ALTER TABLE `videofiles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-05  1:05:34
