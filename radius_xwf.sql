-- MySQL dump 10.13  Distrib 5.5.50, for debian-linux-gnu (x86_64)
--
-- Host: 0.0.0.0    Database: radius_xwf
-- ------------------------------------------------------
-- Server version	5.5.50-0ubuntu0.14.04.1

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
-- Table structure for table `accounts_accesspoint`
--

DROP TABLE IF EXISTS `accounts_accesspoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_accesspoint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `mac_address` varchar(17) NOT NULL,
  `status` varchar(3) NOT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_accesspoint_mac_address_6d4dc51135f5c411_uniq` (`mac_address`),
  UNIQUE KEY `accounts_accesspoint_name_10087264b1198c7_uniq` (`name`),
  KEY `accounts_accesspoint_0e939a4f` (`group_id`),
  CONSTRAINT `accounts_a_group_id_49240ecda741a2a3_fk_accounts_groupaccount_id` FOREIGN KEY (`group_id`) REFERENCES `accounts_groupaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_accesspoint`
--

LOCK TABLES `accounts_accesspoint` WRITE;
/*!40000 ALTER TABLE `accounts_accesspoint` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_accesspoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_groupaccount`
--

DROP TABLE IF EXISTS `accounts_groupaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_groupaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `max_no_of_users` int(11) NOT NULL,
  `data_balance` decimal(8,2) NOT NULL,
  `data_usage` decimal(8,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_groupaccount`
--

LOCK TABLES `accounts_groupaccount` WRITE;
/*!40000 ALTER TABLE `accounts_groupaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_groupaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_networkparameter`
--

DROP TABLE IF EXISTS `accounts_networkparameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_networkparameter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_ip` varchar(10) NOT NULL,
  `login_url` varchar(600) NOT NULL,
  `continue_url` varchar(50) NOT NULL,
  `ap_tags` varchar(50) NOT NULL,
  `ap_mac` varchar(20) NOT NULL,
  `ap_name` varchar(15) NOT NULL,
  `client_mac` varchar(20) NOT NULL,
  `logout_url` varchar(255) DEFAULT NULL,
  `subscriber_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subscriber_id` (`subscriber_id`),
  CONSTRAINT `account_subscriber_id_70f312f003670a55_fk_accounts_subscriber_id` FOREIGN KEY (`subscriber_id`) REFERENCES `accounts_subscriber` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_networkparameter`
--

LOCK TABLES `accounts_networkparameter` WRITE;
/*!40000 ALTER TABLE `accounts_networkparameter` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_networkparameter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_rechargeandusage`
--

DROP TABLE IF EXISTS `accounts_rechargeandusage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_rechargeandusage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(8,2) NOT NULL,
  `balance` decimal(8,2) NOT NULL,
  `action` varchar(3) NOT NULL,
  `date` datetime NOT NULL,
  `activity_id` int(11) NOT NULL,
  `radcheck_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_rechargeandusage_f39f98fa` (`radcheck_id`),
  CONSTRAINT `accounts_rechargeand_radcheck_id_7d4c1a42fd13bb44_fk_radcheck_id` FOREIGN KEY (`radcheck_id`) REFERENCES `radcheck` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_rechargeandusage`
--

LOCK TABLES `accounts_rechargeandusage` WRITE;
/*!40000 ALTER TABLE `accounts_rechargeandusage` DISABLE KEYS */;
INSERT INTO `accounts_rechargeandusage` VALUES (1,2.00,2.00,'REC','2018-06-06 13:04:08',1,4),(2,5.00,5.00,'REC','2018-06-08 14:58:38',21,5),(3,-2.00,3.00,'USG','2018-06-08 15:00:25',1,5),(4,-2.00,1.00,'USG','2018-06-08 15:04:27',1,5);
/*!40000 ALTER TABLE `accounts_rechargeandusage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_subscriber`
--

DROP TABLE IF EXISTS `accounts_subscriber`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_subscriber` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_group_admin` tinyint(1) NOT NULL,
  `country` varchar(3) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email_verified` tinyint(1) NOT NULL,
  `date_verified` datetime DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `accounts_su_group_id_9e9c6bb01c2be98_fk_accounts_groupaccount_id` (`group_id`),
  CONSTRAINT `accounts_subscriber_user_id_5715a0aedc84022f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `accounts_su_group_id_9e9c6bb01c2be98_fk_accounts_groupaccount_id` FOREIGN KEY (`group_id`) REFERENCES `accounts_groupaccount` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_subscriber`
--

LOCK TABLES `accounts_subscriber` WRITE;
/*!40000 ALTER TABLE `accounts_subscriber` DISABLE KEYS */;
INSERT INTO `accounts_subscriber` VALUES (3,0,'GHA','+233231802940',0,NULL,NULL,5),(4,0,'GHA','+233548120109',0,NULL,NULL,6);
/*!40000 ALTER TABLE `accounts_subscriber` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add site',7,'add_site'),(20,'Can change site',7,'change_site'),(21,'Can delete site',7,'delete_site'),(22,'Can add nas',8,'add_nas'),(23,'Can change nas',8,'change_nas'),(24,'Can delete nas',8,'delete_nas'),(25,'Can add radacct',9,'add_radacct'),(26,'Can change radacct',9,'change_radacct'),(27,'Can delete radacct',9,'delete_radacct'),(28,'Can add radgroupcheck',10,'add_radgroupcheck'),(29,'Can change radgroupcheck',10,'change_radgroupcheck'),(30,'Can delete radgroupcheck',10,'delete_radgroupcheck'),(31,'Can add radgroupreply',11,'add_radgroupreply'),(32,'Can change radgroupreply',11,'change_radgroupreply'),(33,'Can delete radgroupreply',11,'delete_radgroupreply'),(34,'Can add radpostauth',12,'add_radpostauth'),(35,'Can change radpostauth',12,'change_radpostauth'),(36,'Can delete radpostauth',12,'delete_radpostauth'),(37,'Can add radreply',13,'add_radreply'),(38,'Can change radreply',13,'change_radreply'),(39,'Can delete radreply',13,'delete_radreply'),(40,'Can add radusergroup',14,'add_radusergroup'),(41,'Can change radusergroup',14,'change_radusergroup'),(42,'Can delete radusergroup',14,'delete_radusergroup'),(43,'Can add radcheck',15,'add_radcheck'),(44,'Can change radcheck',15,'change_radcheck'),(45,'Can delete radcheck',15,'delete_radcheck'),(46,'Can add Group Account',16,'add_groupaccount'),(47,'Can change Group Account',16,'change_groupaccount'),(48,'Can delete Group Account',16,'delete_groupaccount'),(49,'Can add subscriber',17,'add_subscriber'),(50,'Can change subscriber',17,'change_subscriber'),(51,'Can delete subscriber',17,'delete_subscriber'),(52,'Can add network parameter',18,'add_networkparameter'),(53,'Can change network parameter',18,'change_networkparameter'),(54,'Can delete network parameter',18,'delete_networkparameter'),(55,'Can add Access Point',19,'add_accesspoint'),(56,'Can change Access Point',19,'change_accesspoint'),(57,'Can delete Access Point',19,'delete_accesspoint'),(58,'Can add recharge and usage',20,'add_rechargeandusage'),(59,'Can change recharge and usage',20,'change_rechargeandusage'),(60,'Can delete recharge and usage',20,'delete_rechargeandusage'),(61,'Can add package',21,'add_package'),(62,'Can change package',21,'change_package'),(63,'Can delete package',21,'delete_package'),(64,'Can add instant voucher',22,'add_instantvoucher'),(65,'Can change instant voucher',22,'change_instantvoucher'),(66,'Can delete instant voucher',22,'delete_instantvoucher'),(67,'Can add Package Subscription',23,'add_packagesubscription'),(68,'Can change Package Subscription',23,'change_packagesubscription'),(69,'Can delete Package Subscription',23,'delete_packagesubscription'),(70,'Can add Group Package Subscription',24,'add_grouppackagesubscription'),(71,'Can change Group Package Subscription',24,'change_grouppackagesubscription'),(72,'Can delete Group Package Subscription',24,'delete_grouppackagesubscription'),(73,'Can add group account payment',25,'add_groupaccountpayment'),(74,'Can change group account payment',25,'change_groupaccountpayment'),(75,'Can delete group account payment',25,'delete_groupaccountpayment'),(76,'Can add individual payment',26,'add_individualpayment'),(77,'Can change individual payment',26,'change_individualpayment'),(78,'Can delete individual payment',26,'delete_individualpayment');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(100) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$LiBshNf3b0Lr$wFhgrDkyLWMGQ8nTY/zTQaXpCr5iiEO5iA9iV6crUPE=','2018-06-08 14:47:16',1,'dayo@incisia.com','','','dayo@incisia.com',1,1,'2017-09-15 11:47:02'),(5,'pbkdf2_sha256$20000$KVEgzKGFE0rR$0a8nDhHnopWDeL+7PnO16X4ld5nE++umXTbdJYJvaZ8=','2018-06-06 12:30:47',0,'0231802940','','','0231802940',0,1,'2018-06-06 12:30:47'),(6,'pbkdf2_sha256$20000$7re7PA5kZ1Os$AidduqOy4neTw9DkCtmrU8d5qS0C+G7fxt9S/LQ5mmc=','2018-06-08 15:04:13',0,'0548120109','','','0548120109',0,1,'2018-06-08 14:46:02');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-06-06 12:26:51','4','0231802940',1,'',4,1),(2,'2018-06-06 12:30:18','4','0231802940',3,'',4,1),(3,'2018-06-08 14:49:35','1','256Kbps Daily 1GB',1,'',21,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (19,'accounts','accesspoint'),(16,'accounts','groupaccount'),(8,'accounts','nas'),(18,'accounts','networkparameter'),(9,'accounts','radacct'),(15,'accounts','radcheck'),(10,'accounts','radgroupcheck'),(11,'accounts','radgroupreply'),(12,'accounts','radpostauth'),(13,'accounts','radreply'),(14,'accounts','radusergroup'),(20,'accounts','rechargeandusage'),(17,'accounts','subscriber'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(24,'packages','grouppackagesubscription'),(22,'packages','instantvoucher'),(21,'packages','package'),(23,'packages','packagesubscription'),(25,'payments','groupaccountpayment'),(26,'payments','individualpayment'),(6,'sessions','session'),(7,'sites','site');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-09-15 11:39:06'),(2,'auth','0001_initial','2017-09-15 11:39:06'),(3,'packages','0001_initial','2017-09-15 11:39:06'),(4,'accounts','0001_initial','2017-09-15 11:39:06'),(5,'accounts','0002_auto_20150910_1240','2017-09-15 11:39:07'),(6,'accounts','0003_auto_20150910_1824','2017-09-15 11:39:07'),(7,'accounts','0004_auto_20150911_1914','2017-09-15 11:39:07'),(8,'accounts','0005_auto_20150911_2051','2017-09-15 11:39:07'),(9,'accounts','0006_radcheck_user','2017-09-15 11:39:07'),(10,'accounts','0007_auto_20151008_1321','2017-09-15 11:39:07'),(11,'accounts','0008_rechargeandusage','2017-09-15 11:39:07'),(12,'accounts','0009_auto_20151025_2304','2017-09-15 11:39:07'),(13,'accounts','0010_rechargeandusage_activity_id','2017-09-15 11:39:07'),(14,'accounts','0011_auto_20151027_1720','2017-09-15 11:39:07'),(15,'accounts','0012_auto_20151106_0202','2017-09-15 11:39:08'),(16,'accounts','0013_auto_20151106_0243','2017-09-15 11:39:08'),(17,'accounts','0014_auto_20151221_1040','2017-09-15 11:39:08'),(18,'accounts','0015_auto_20151221_1316','2017-09-15 11:39:08'),(19,'accounts','0016_auto_20151222_1829','2017-09-15 11:39:08'),(20,'accounts','0017_radcheck_is_logged_in','2017-09-15 11:39:08'),(21,'accounts','0018_remove_radcheck_is_logged_in','2017-09-15 11:39:08'),(22,'accounts','0019_radcheck_is_logged_in','2017-09-15 11:39:08'),(23,'accounts','0020_auto_20160624_1339','2017-09-15 11:39:08'),(24,'accounts','0021_auto_20160624_1343','2017-09-15 11:39:08'),(25,'accounts','0022_auto_20160624_1502','2017-09-15 11:39:08'),(26,'accounts','0023_radcheck_data_usage','2017-09-15 11:39:08'),(27,'accounts','0024_auto_20160627_1053','2017-09-15 11:39:09'),(28,'accounts','0025_auto_20160708_1845','2017-09-15 11:39:09'),(29,'accounts','0026_auto_20160711_1249','2017-09-15 11:39:09'),(30,'accounts','0027_groupaccount_data_balance','2017-09-15 11:39:09'),(31,'accounts','0028_auto_20160725_1718','2017-09-15 11:39:09'),(32,'accounts','0029_auto_20160725_1720','2017-09-15 11:39:09'),(33,'accounts','0030_auto_20160725_1822','2017-09-15 11:39:09'),(34,'accounts','0031_auto_20160909_1822','2017-09-15 11:39:09'),(35,'accounts','0032_networkparameter','2017-09-15 11:39:09'),(36,'accounts','0033_auto_20161110_1854','2017-09-15 11:39:09'),(37,'accounts','0034_auto_20161114_1918','2017-09-15 11:39:10'),(38,'accounts','0035_groupaccount_bill_group_member','2017-09-15 11:39:10'),(39,'accounts','0036_remove_groupaccount_bill_group_member','2017-09-15 11:39:10'),(40,'accounts','0037_radpostauth_message','2017-09-15 11:39:10'),(41,'accounts','0038_auto_20170204_1508','2017-09-15 11:39:10'),(42,'accounts','0039_auto_20170518_1533','2017-09-15 11:39:10'),(43,'admin','0001_initial','2017-09-15 11:39:10'),(44,'contenttypes','0002_remove_content_type_name','2017-09-15 11:39:10'),(45,'auth','0002_alter_permission_name_max_length','2017-09-15 11:39:10'),(46,'auth','0003_alter_user_email_max_length','2017-09-15 11:39:10'),(47,'auth','0004_alter_user_username_opts','2017-09-15 11:39:10'),(48,'auth','0005_alter_user_last_login_null','2017-09-15 11:39:10'),(49,'auth','0006_require_contenttypes_0002','2017-09-15 11:39:10'),(50,'auth','0007_auto_20161110_1820','2017-09-15 11:39:10'),(51,'packages','0002_packagesubscription','2017-09-15 11:39:10'),(52,'packages','0003_delete_packagesubscription','2017-09-15 11:39:11'),(53,'packages','0004_grouppackagesubscription','2017-09-15 11:39:11'),(54,'packages','0005_auto_20150911_1914','2017-09-15 11:39:11'),(55,'packages','0006_packagesubscription','2017-09-15 11:39:11'),(56,'packages','0007_auto_20151009_1324','2017-09-15 11:39:11'),(57,'packages','0008_auto_20151014_1252','2017-09-15 11:39:11'),(58,'packages','0009_auto_20151027_1720','2017-09-15 11:39:11'),(59,'packages','0010_auto_20151125_1113','2017-09-15 11:39:11'),(60,'packages','0011_instantvoucher','2017-09-15 11:39:11'),(61,'packages','0012_auto_20151222_1708','2017-09-15 11:39:11'),(62,'packages','0013_auto_20160615_1131','2017-09-15 11:39:12'),(63,'packages','0014_auto_20160629_1437','2017-09-15 11:39:12'),(64,'packages','0015_auto_20160707_1056','2017-09-15 11:39:12'),(65,'packages','0016_auto_20160711_2042','2017-09-15 11:39:12'),(66,'packages','0017_auto_20160718_0745','2017-09-15 11:39:12'),(67,'packages','0018_auto_20161114_1839','2017-09-15 11:39:12'),(68,'packages','0019_auto_20161116_1646','2017-09-15 11:39:12'),(69,'packages','0020_auto_20161216_0241','2017-09-15 11:39:12'),(70,'packages','0021_package_is_public','2017-09-15 11:39:12'),(71,'packages','0022_auto_20170204_1022','2017-09-15 11:39:13'),(72,'packages','0023_auto_20170504_1933','2017-09-15 11:39:13'),(73,'packages','0024_auto_20170530_2009','2017-09-15 11:39:13'),(74,'packages','0025_auto_20170914_2122','2017-09-15 11:39:13'),(75,'payments','0001_initial','2017-09-15 11:39:13'),(76,'payments','0002_auto_20160615_1201','2017-09-15 11:39:13'),(77,'sessions','0001_initial','2017-09-15 11:39:13'),(78,'sites','0001_initial','2017-09-15 11:39:13');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3q0snbadpkuwptwa772rmsj8c1rf4wiz','NTg4YTk1MDgzMTkwYmZiMDc5ODI3NGFmYzhjOWQzNzQyY2FiMzQ3Njp7Il9hdXRoX3VzZXJfaGFzaCI6ImIzMzJkZTcyN2MzMWU4NDczYzMxYjEyZDY1MGUxMjI1Y2Q3OTdhYjciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI2In0=','2018-06-22 15:04:13');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nas`
--

DROP TABLE IF EXISTS `nas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nasname` varchar(128) NOT NULL,
  `shortname` varchar(32) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `ports` int(11) DEFAULT NULL,
  `secret` varchar(60) NOT NULL,
  `server` varchar(64) DEFAULT NULL,
  `community` varchar(50) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nas`
--

LOCK TABLES `nas` WRITE;
/*!40000 ALTER TABLE `nas` DISABLE KEYS */;
/*!40000 ALTER TABLE `nas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `packages_grouppackagesubscription`
--

DROP TABLE IF EXISTS `packages_grouppackagesubscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `packages_grouppackagesubscription` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start` datetime NOT NULL,
  `stop` datetime DEFAULT NULL,
  `group_id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `purchase_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `packages_g_group_id_5b1045a4b1482d3b_fk_accounts_groupaccount_id` (`group_id`),
  KEY `packages_group_package_id_862364bb1821056_fk_packages_package_id` (`package_id`),
  CONSTRAINT `packages_group_package_id_862364bb1821056_fk_packages_package_id` FOREIGN KEY (`package_id`) REFERENCES `packages_package` (`id`),
  CONSTRAINT `packages_g_group_id_5b1045a4b1482d3b_fk_accounts_groupaccount_id` FOREIGN KEY (`group_id`) REFERENCES `accounts_groupaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packages_grouppackagesubscription`
--

LOCK TABLES `packages_grouppackagesubscription` WRITE;
/*!40000 ALTER TABLE `packages_grouppackagesubscription` DISABLE KEYS */;
/*!40000 ALTER TABLE `packages_grouppackagesubscription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `packages_instantvoucher`
--

DROP TABLE IF EXISTS `packages_instantvoucher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `packages_instantvoucher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `package_id` int(11) NOT NULL,
  `radcheck_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `packages_inst_package_id_5344902756ddd4e5_fk_packages_package_id` (`package_id`),
  KEY `packages_instantvouc_radcheck_id_3b3b34e9a00f987d_fk_radcheck_id` (`radcheck_id`),
  CONSTRAINT `packages_instantvouc_radcheck_id_3b3b34e9a00f987d_fk_radcheck_id` FOREIGN KEY (`radcheck_id`) REFERENCES `radcheck` (`id`),
  CONSTRAINT `packages_inst_package_id_5344902756ddd4e5_fk_packages_package_id` FOREIGN KEY (`package_id`) REFERENCES `packages_package` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packages_instantvoucher`
--

LOCK TABLES `packages_instantvoucher` WRITE;
/*!40000 ALTER TABLE `packages_instantvoucher` DISABLE KEYS */;
/*!40000 ALTER TABLE `packages_instantvoucher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `packages_package`
--

DROP TABLE IF EXISTS `packages_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `packages_package` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `package_type` varchar(7) NOT NULL,
  `volume` varchar(9) NOT NULL,
  `speed` varchar(5) NOT NULL,
  `price` decimal(8,2) NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packages_package`
--

LOCK TABLES `packages_package` WRITE;
/*!40000 ALTER TABLE `packages_package` DISABLE KEYS */;
INSERT INTO `packages_package` VALUES (1,'Daily','1','.256',2.00,1);
/*!40000 ALTER TABLE `packages_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `packages_packagesubscription`
--

DROP TABLE IF EXISTS `packages_packagesubscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `packages_packagesubscription` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start` datetime NOT NULL,
  `stop` datetime DEFAULT NULL,
  `package_id` int(11) NOT NULL,
  `radcheck_id` int(11) NOT NULL,
  `purchase_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `packages_pack_package_id_7966b238587ccfc8_fk_packages_package_id` (`package_id`),
  KEY `packages_packagesubscription_f39f98fa` (`radcheck_id`),
  CONSTRAINT `packages_packagesubsc_radcheck_id_b10b6e270ead5a0_fk_radcheck_id` FOREIGN KEY (`radcheck_id`) REFERENCES `radcheck` (`id`),
  CONSTRAINT `packages_pack_package_id_7966b238587ccfc8_fk_packages_package_id` FOREIGN KEY (`package_id`) REFERENCES `packages_package` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packages_packagesubscription`
--

LOCK TABLES `packages_packagesubscription` WRITE;
/*!40000 ALTER TABLE `packages_packagesubscription` DISABLE KEYS */;
INSERT INTO `packages_packagesubscription` VALUES (1,'2018-06-08 15:00:25','2018-06-09 15:00:25',1,5,'2018-06-08 15:00:25'),(2,'2018-06-09 15:00:25','2018-06-10 15:00:25',1,5,'2018-06-08 15:04:27');
/*!40000 ALTER TABLE `packages_packagesubscription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_groupaccountpayment`
--

DROP TABLE IF EXISTS `payments_groupaccountpayment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments_groupaccountpayment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `payment_for` date NOT NULL,
  `date` datetime NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_g_group_id_4b65369153e6d7da_fk_accounts_groupaccount_id` (`group_id`),
  CONSTRAINT `payments_g_group_id_4b65369153e6d7da_fk_accounts_groupaccount_id` FOREIGN KEY (`group_id`) REFERENCES `accounts_groupaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_groupaccountpayment`
--

LOCK TABLES `payments_groupaccountpayment` WRITE;
/*!40000 ALTER TABLE `payments_groupaccountpayment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_groupaccountpayment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_individualpayment`
--

DROP TABLE IF EXISTS `payments_individualpayment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments_individualpayment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(20) NOT NULL,
  `subscription_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `D87764add4dd4b2231b567beb96f40e8` (`subscription_id`),
  CONSTRAINT `D87764add4dd4b2231b567beb96f40e8` FOREIGN KEY (`subscription_id`) REFERENCES `packages_packagesubscription` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_individualpayment`
--

LOCK TABLES `payments_individualpayment` WRITE;
/*!40000 ALTER TABLE `payments_individualpayment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_individualpayment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radacct`
--

DROP TABLE IF EXISTS `radacct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radacct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `acctsessionid` varchar(64) NOT NULL,
  `acctuniqueid` varchar(32) NOT NULL,
  `username` varchar(64) NOT NULL,
  `groupname` varchar(64) NOT NULL,
  `realm` varchar(64) DEFAULT NULL,
  `nasipaddress` varchar(15) NOT NULL,
  `nasportid` varchar(15) DEFAULT NULL,
  `nasporttype` varchar(32) DEFAULT NULL,
  `acctstarttime` datetime DEFAULT NULL,
  `acctupdatetime` datetime DEFAULT NULL,
  `acctstoptime` datetime DEFAULT NULL,
  `acctinterval` int(11) DEFAULT NULL,
  `acctsessiontime` int(11) DEFAULT NULL,
  `acctauthentic` varchar(32) DEFAULT NULL,
  `connectinfo_start` varchar(50) DEFAULT NULL,
  `connectinfo_stop` varchar(50) DEFAULT NULL,
  `acctinputoctets` bigint(20) DEFAULT NULL,
  `acctoutputoctets` bigint(20) DEFAULT NULL,
  `calledstationid` varchar(50) NOT NULL,
  `callingstationid` varchar(50) NOT NULL,
  `acctterminatecause` varchar(32) NOT NULL,
  `servicetype` varchar(32) DEFAULT NULL,
  `framedprotocol` varchar(32) DEFAULT NULL,
  `framedipaddress` varchar(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `acctuniqueid` (`acctuniqueid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radacct`
--

LOCK TABLES `radacct` WRITE;
/*!40000 ALTER TABLE `radacct` DISABLE KEYS */;
/*!40000 ALTER TABLE `radacct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radcheck`
--

DROP TABLE IF EXISTS `radcheck`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radcheck` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `attribute` varchar(64) NOT NULL,
  `op` varchar(2) NOT NULL,
  `value` varchar(253) NOT NULL,
  `user_id` int(11),
  `is_logged_in` tinyint(1) NOT NULL,
  `data_balance` decimal(8,2) NOT NULL,
  `data_usage` decimal(8,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `radcheck_user_id_6fa42c0338a626a8_uniq` (`user_id`),
  CONSTRAINT `radcheck_user_id_6fa42c0338a626a8_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radcheck`
--

LOCK TABLES `radcheck` WRITE;
/*!40000 ALTER TABLE `radcheck` DISABLE KEYS */;
INSERT INTO `radcheck` VALUES (4,'0231802940','MD5-Password',':=','827ccb0eea8a706c4c34a16891f84e7b',5,0,0.00,0.00),(5,'0548120109','MD5-Password',':=','827ccb0eea8a706c4c34a16891f84e7b',6,0,2.00,0.00);
/*!40000 ALTER TABLE `radcheck` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radgroupcheck`
--

DROP TABLE IF EXISTS `radgroupcheck`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radgroupcheck` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `groupname` varchar(64) NOT NULL,
  `attribute` varchar(64) NOT NULL,
  `op` varchar(2) NOT NULL,
  `value` varchar(253) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radgroupcheck`
--

LOCK TABLES `radgroupcheck` WRITE;
/*!40000 ALTER TABLE `radgroupcheck` DISABLE KEYS */;
/*!40000 ALTER TABLE `radgroupcheck` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radgroupreply`
--

DROP TABLE IF EXISTS `radgroupreply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radgroupreply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `groupname` varchar(64) NOT NULL,
  `attribute` varchar(64) NOT NULL,
  `op` varchar(2) NOT NULL,
  `value` varchar(253) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radgroupreply`
--

LOCK TABLES `radgroupreply` WRITE;
/*!40000 ALTER TABLE `radgroupreply` DISABLE KEYS */;
/*!40000 ALTER TABLE `radgroupreply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radpostauth`
--

DROP TABLE IF EXISTS `radpostauth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radpostauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `pass` varchar(64) NOT NULL,
  `reply` varchar(32) NOT NULL,
  `authdate` datetime NOT NULL,
  `message` varchar(255) NOT NULL,
  `client_mac` varchar(17) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radpostauth`
--

LOCK TABLES `radpostauth` WRITE;
/*!40000 ALTER TABLE `radpostauth` DISABLE KEYS */;
/*!40000 ALTER TABLE `radpostauth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radreply`
--

DROP TABLE IF EXISTS `radreply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radreply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `attribute` varchar(64) NOT NULL,
  `op` varchar(2) NOT NULL,
  `value` varchar(253) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radreply`
--

LOCK TABLES `radreply` WRITE;
/*!40000 ALTER TABLE `radreply` DISABLE KEYS */;
/*!40000 ALTER TABLE `radreply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radusergroup`
--

DROP TABLE IF EXISTS `radusergroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radusergroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `groupname` varchar(64) NOT NULL,
  `priority` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radusergroup`
--

LOCK TABLES `radusergroup` WRITE;
/*!40000 ALTER TABLE `radusergroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `radusergroup` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-24 10:49:01
