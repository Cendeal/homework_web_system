-- MySQL dump 10.13  Distrib 5.5.60, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: homework
-- ------------------------------------------------------
-- Server version	5.5.60-0ubuntu0.14.04.1

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
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses` (
  `id` varchar(64) NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  `fk_tid` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `fk_tid` (`fk_tid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES ('01','视听说','041609'),('09','数据库概论','041609'),('03','大英','041609'),('04','计算机网络','041609'),('1001','数学建模啦！','520131'),('1002','建模群通知','520131'),('07','软件工程导论','041609'),('08','操作系统','041609'),('11','期末考试时间','041609'),('唔知','文学通论','071610'),('12','其它重要通知','041609'),('21','NC大创','000000');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `houseworks`
--

DROP TABLE IF EXISTS `houseworks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `houseworks` (
  `createdate` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) DEFAULT NULL,
  `content` text,
  `state` int(11) DEFAULT NULL,
  `fk_tid` varchar(64) DEFAULT NULL,
  `fk_cid` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_tid` (`fk_tid`),
  KEY `fk_cid` (`fk_cid`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `houseworks`
--

LOCK TABLES `houseworks` WRITE;
/*!40000 ALTER TABLE `houseworks` DISABLE KEYS */;
INSERT INTO `houseworks` VALUES ('2018-06-19 15:11:32',1,'我们进赛了','Happy，无敌的我们，稳稳的',1,'520131','1001'),('2018-06-19 15:19:14',3,'参加国赛队伍须知',' 通知：获得全国赛参赛资格的队伍请注意：\r\n1、请移步到吉珠2018数模国赛群： 799970656。今后关于数模国赛的相关培训和通知都将\r\n在该群发布。\r\n2、本学期不再安排培训，大家接下来安心准备各科期末考试。\r\n3、暑假不留校，但暑假有两次模拟训练的安排，会通过网络与大家沟通，届时会对每一个队伍有针对性的训练提高。暑假安排计划表会在放假前发布。\r\n4、晋级全国赛是大家新的学习阶段的开始，开学我们要和全国一千多所高校三万多支队伍九万多名大学生同台竞技，那才是我们真正的赛场。坚持学习才能不断进步。\r\n以上安排望知晓。',0,'520131','1002'),('2018-06-19 15:24:06',4,'预测帝有要秃头了','20118-6-19林晓芳预言帝有在大四前会秃头',0,'520131','1001'),('2018-06-19 16:48:31',5,'操作系统期末考试通知','地点：D304\r\n考试时间：7月10日 14:00-16:00',0,'041609','08'),('2018-06-19 16:50:10',6,'计算机网络期末考试通知','地点：A206\r\n考试时间：7月4日 10:30-12:30\r\n形式：机考',1,'041609','04'),('2018-06-19 16:52:25',7,'数据库概论期末考试通知','地点：A206 \r\n考试时间：7月6日 10:30-12:30\r\n形式：机考',0,'041609','09'),('2018-06-19 16:54:20',8,'大英期末考试通知','地点：D206\r\n考试时间：7月7日 16:30-18:30',0,'041609','03'),('2018-06-19 16:55:55',9,'软件工程期末考试通知','地点：D205\r\n考试时间：7月08日 16:30-18:30',0,'041609','07'),('2018-06-19 16:56:55',11,'期末考试通知','地点：D402\r\n考试时间：6月22日星期五 3-4节\r\n形式：视听说考试要求，务必认真看！！！\r\n各位同学本着对自己负责的原则认真阅读下面的【每】【一】【个】【字】\r\n【期末口语考试】\r\n总共10分（包括在视听说平时成绩的20分里），包括2个题目\r\n1）演讲（5分）\r\n时间长度为60-90秒，不足60秒或超出90秒都会扣分，我会用秒表严格计时，所以为了确保不超出这个范围，唯一的办法就是背得滚瓜烂熟，还要借助秒表多次演练。没有任何借口做不到； \r\n\r\n内容只能是演讲（不能是新闻、故事等其他题材，违者计0分）且要求完全正确，无任何错误，所以必须去网上找名人演讲的讲稿，禁止自己写稿；必须提醒大家，60-90秒非常非常短，一不小心就超出了，事实上你们只需要找名人演讲的一段话，甚至一段话中的一小部分就够了\r\n\r\n考试当天必须把事先打印好的纸质讲稿带来，在考试之前交给我，不交讲稿或讲稿不符合要求的，该部分计0分（纸质讲稿要求：A4纸打印，字体为Times New Roman，字号为三号字或16号字（写法不同而已，其实是一码事），纸最上方是姓名-专业-学号。禁止手写）\r\n\r\n评分依据：发音准确性（口头），语法正确性（口头，书面），拼写正确性（书面），对错误零容忍。错3个词扣1分，扣到0分为止。\r\n\r\n2）问答题（5分）\r\n演讲结束后马上进入问答环节。老师用英语提一个问题，学生立即用英语作答。如果学生没听懂，老师再给一次机会，问第二个问题。没有第三次机会。问题范围是跟大学生日常生活密切相关的话题。\r\n\r\n注意这次口试都是一对一的形式，不需要找搭档！\r\n\r\n口语考试为随堂考试，和平时上课时间完全相同。随机点名，不按学号顺序，所以任何一个同学都可能第一个被点到，请一定在考试时间之前就做好准备！',1,'041609','01'),('2018-06-20 00:02:29',12,'2018期末时间表','############################################\r\n\r\n考试日期   考试时间	科目		地点	\r\n2018年7月4日	10:30-12:30	计算机网络	A206	\r\n2018年7月6日	10:30-12:30	数据库概论	A206	\r\n2018年7月7日	16:30-18:30	大学英语BⅣ	D206\r\n2018年7月8日	16:30-18:30	软件工程导论	D205\r\n2018年7月10日	14:00-16:00	操作系统  	D304								',0,'041609','11'),('2018-06-27 13:29:51',13,'软件工程修读要求','1.必修要求   必修\r\n2.系选修学分要求   13.5分\r\n3.院公选课要求     8分或8分以上',0,'041609','12'),('2018-07-02 17:37:59',14,'自主学习平台','负责人：陈帝有\r\n参与人：孙名扬\r\n级   别：省级',0,'000000','21'),('2018-07-02 17:39:25',15,'随便e天','负责人：黄家璇 \r\n参与人：梁冬柔\r\n级   别：省级',0,'000000','21'),('2018-07-02 17:41:11',16,'饮料瓶智能环保回收机','负责人：陈晓涛 \r\n参与人： 王珊珊 邱源茂\r\n级   别：校级',0,'000000','21'),('2018-07-02 17:42:18',17,'懒人购物车','负责人：俄琳 \r\n参与人：黄楚涵 吴一弘 吉祥\r\n级   别：校级',0,'000000','21');
/*!40000 ALTER TABLE `houseworks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students` (
  `id` varchar(64) NOT NULL,
  `perm` int(11) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES ('04160901',0,'pbkdf2:sha256:50000$kvNyE8lY$368f71b149c2a516402dc15ae135b93f2cf3213183e428e17ba46b52ef143eb9','钟毓萍','841265735@qq.com'),('04160902',0,'pbkdf2:sha256:50000$KKfwUgeh$544e3dba133b7b2686285ff473831c4234f0b6adc9503e0f8ac04f8bf4b2cfdc','阿走','1192522605@qq.com'),('04160903',0,'pbkdf2:sha256:50000$ujTSyu0D$5166f49dfd97707ef5d0ac52428468b42454faee3f28021da7272a0805464209','刘杰东','liujiedong@126.com'),('04160906',0,'pbkdf2:sha256:50000$JCP0t8IX$32160ad36491452bbc22f57586e35c9ea0c9c30864d49b68efe88b4af9c360bc','吴文宜','1017049763@qq.com'),('04160908',8,'pbkdf2:sha256:50000$Glm5B4EO$ba89c5b22a683cbd0075dfd814c043adb34ff602dfd97ece4ef65ec2fd3b5b58','阮铠','626753724@qq.com'),('04160909',16,'pbkdf2:sha256:50000$nwMQnr7v$83e6a840a83c145d1c17335adc20103aefd1645c0294510a4ea8c8919cdc70e1','陈帝有','1798062051@qq.com'),('04160917',0,'pbkdf2:sha256:50000$gfe3MLzT$7ad86e856a89ae340025c3b54b2bd5b7b57b65682f0031f8b59af469af32f014','栾天翔','1481168887@qq.com'),('04160921',0,'pbkdf2:sha256:50000$Qkb9y2st$10c907b738e5244fd3fc2e281e9aebe15625250c1693d4e6ec0cbd78d8042daf','陈建威','460959642@qq.com'),('04160926',0,'pbkdf2:sha256:50000$XFtZ8j8d$cb2b534a4ed046dd5389b75103aaf9e8216c0133da5d09251845267bb7617229','谢桂填','1491048863@qq.com'),('04160971',0,'pbkdf2:sha256:50000$JNaAS463$859c3d9e5be4d3e2683c27b549ec403ea49c597402a1a6d3b2adaf9e23889851','Shannon ','123456789@qq.com'),('04161806',16,'pbkdf2:sha256:50000$GNthvVkv$a44b5b4a3fd91a27f1e6347bfa1eccb341206e524003d25ad1206e46ea1560e1','葫芦娃','1371990633@qq.com'),('06160422',0,'pbkdf2:sha256:50000$JXtpGEIw$84f2abe5d5d2e9cb219e423bedf5c0803425ee8bcc136085a7540c04bb8a40bf','张晓辉','www.1305403965@qq.com'),('02160809',0,'pbkdf2:sha256:50000$8F071Wic$6d4e131ea42557d428205187d24c30d9c69125049106ee6b57d558dad36c879b','林晓芳','673724379@qq.com'),('52013141',8,'pbkdf2:sha256:50000$R8XMd3ky$5dadbe6ded176a9df2e6d11c8c728cb49a2847035e1bf35f89851b3d67a54720','陈帝有','52013141@qq.com'),('52013142',8,'pbkdf2:sha256:50000$Kq449tcV$49f14dbe392801547b67410cc5a81304f98f39092470b8f5130e4ffe4f89a5e1','林晓芳','275026629@qq.com'),('04160915',0,'pbkdf2:sha256:50000$D3dP83KW$4d9c0a1e6422169ff0639d9512317ba42add3306ffe15d63c9f2767a93037b33','王鹏','1091804172@qq.com'),('07161004',8,'pbkdf2:sha256:50000$CvXsmFoa$d18efeaf1948b02b24236dc8497425585e22fed781259259f332475f1356b09d','ldr','1036589807@qq.com'),('00000001',8,'pbkdf2:sha256:50000$GJBPSoPZ$0b71dcfcb26bc6ab4751c86a5151fd45992d519f000a54b70e7d387db2ead1ac','NC','000001@nc.com');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teamnumbers`
--

DROP TABLE IF EXISTS `teamnumbers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teamnumbers` (
  `id` varchar(64) NOT NULL,
  `fk_sid` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_sid` (`fk_sid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teamnumbers`
--

LOCK TABLES `teamnumbers` WRITE;
/*!40000 ALTER TABLE `teamnumbers` DISABLE KEYS */;
INSERT INTO `teamnumbers` VALUES ('041609',NULL),('041618',NULL),('061604',NULL),('111111',NULL),('041610',NULL),('021608',NULL),('520131',NULL),('071610',NULL),('000000',NULL);
/*!40000 ALTER TABLE `teamnumbers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-05  4:11:10
