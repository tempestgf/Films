-- MySQL dump 10.13  Distrib 8.4.0, for Win64 (x86_64)
--
-- Host: localhost    Database: resenas_series
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `resenyes`
--

DROP TABLE IF EXISTS `resenyes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resenyes` (
  `ResenyaID` int NOT NULL AUTO_INCREMENT,
  `TemporadaID` int DEFAULT NULL,
  `NomUsuari` varchar(255) DEFAULT NULL,
  `Critica` text,
  `DataResenya` date DEFAULT NULL,
  `Puntuacio` decimal(3,1) DEFAULT NULL,
  PRIMARY KEY (`ResenyaID`),
  KEY `TemporadaID` (`TemporadaID`),
  CONSTRAINT `resenyes_ibfk_1` FOREIGN KEY (`TemporadaID`) REFERENCES `temporades` (`TemporadaID`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resenyes`
--

LOCK TABLES `resenyes` WRITE;
/*!40000 ALTER TABLE `resenyes` DISABLE KEYS */;
INSERT INTO `resenyes` VALUES (21,15,'test','Bona serie','2024-05-23',5.0),(22,16,'Guillem','M\'ha agradat','2024-05-23',3.0),(23,15,'da','me guto','2024-05-23',4.0),(24,15,'hola','Bona serie','2024-05-23',4.0),(25,33,'Mama','Llarga i repetitiva','2024-05-23',3.0);
/*!40000 ALTER TABLE `resenyes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `series`
--

DROP TABLE IF EXISTS `series`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `series` (
  `SerieID` int NOT NULL AUTO_INCREMENT,
  `Plataforma` varchar(255) DEFAULT NULL,
  `Tematica` varchar(255) DEFAULT NULL,
  `NomSerie` varchar(255) DEFAULT NULL,
  `AnyInici` date DEFAULT NULL,
  `AnyFi` date DEFAULT NULL,
  `Premis` text,
  `Repartiment` text,
  `Regio` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`SerieID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `series`
--

LOCK TABLES `series` WRITE;
/*!40000 ALTER TABLE `series` DISABLE KEYS */;
INSERT INTO `series` VALUES (19,'HBO','Aventura','Game Of Thrones','2011-07-23',NULL,'12','Sean Bean, Peter Dinklage','Spain'),(20,'Netflix','Acció','Daredevil','2015-01-08',NULL,'3','Charlie Cox, Elden Henson','Estats Units'),(21,'Netflix','Acció','Gambito de Dama','2020-06-23',NULL,'6','Ana Taylor Joy','Estats Units'),(22,'Netflix','Acció','Peaky Blinders','2013-02-23',NULL,'3','Cillian Murphy','Regne Unit'),(23,'Netflix','Crim','Por 13 Razones','2017-02-23',NULL,'3','Dylan Minnette','Estats Units'),(24,'Netflix','Misteri','Stranger Things','2016-01-23',NULL,'4','David Harbour','Estats Units'),(25,'Netflix','Ciència ficció','Black Mirror','2011-06-23',NULL,'3','Rory Kinnear','Regne Unit'),(26,'HBO','Terror','From','2022-05-23',NULL,'3','Harold Perrineau','Estats Units'),(28,'HBO','Acció','The Head','2020-06-23',NULL,'1','John Lynch','Espanya'),(31,'HBO','Terror','The Last Of Us','2023-02-23',NULL,'1','Pedro Pascal','Estats Units'),(32,'Disney Plus','Drama','Dopesick','2021-01-23',NULL,'2','Michael Keaton','Estats Units'),(33,'Disney Plus','Drama','The Product','2022-02-23',NULL,'3','Amanda Seyfried','Estats Units'),(34,'Disney Plus','Acció','Nos vemos en otra vida','2024-05-16',NULL,'3','Roberto Gutierrez','Espanya'),(35,'Disney Plus','Acció','Punisher','2014-06-23',NULL,'3','Jon Bernthal','Estats Units'),(36,'Disney Plus','Acció','Shogun','2024-05-01',NULL,'2','Hiroyuki Sanada','Canada'),(37,'Disney Plus','Comèdia','Nada','2024-05-02',NULL,'2','Luis Bardoni','Argentina'),(38,'HBO','Terror','Riverdale','2021-02-01',NULL,'2','Madeline Petsh','Estats Units'),(39,'HBO','Drama','Outsider','2014-06-23',NULL,'1','Jared Leto','Estats Units');
/*!40000 ALTER TABLE `series` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temporades`
--

DROP TABLE IF EXISTS `temporades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temporades` (
  `TemporadaID` int NOT NULL AUTO_INCREMENT,
  `SerieID` int DEFAULT NULL,
  `NumTemporada` int DEFAULT NULL,
  `Descripcio` text,
  `ImatgeTemporada` varchar(255) DEFAULT NULL,
  `TrailerTemporada` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`TemporadaID`),
  KEY `SerieID` (`SerieID`),
  CONSTRAINT `temporades_ibfk_1` FOREIGN KEY (`SerieID`) REFERENCES `series` (`SerieID`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temporades`
--

LOCK TABLES `temporades` WRITE;
/*!40000 ALTER TABLE `temporades` DISABLE KEYS */;
INSERT INTO `temporades` VALUES (14,19,1,'Serie de TV (2011-2019). 8 temporadas. 73 episodios. La historia se desarrolla en un mundo ficticio de carácter medieval donde hay Siete Reinos. Hay tres líneas argumentales principales: la crónica de la guerra civil dinástica por el control de Poniente entre varias familias nobles que aspiran al Trono de Hierro; la creciente amenaza de \"los otros\", seres desconocidos que viven al otro lado de un inmenso muro de hielo que protege el Norte de Poniente; y el viaje de Daenerys Targaryen, la hija exiliada del rey que fue asesinado en una guerra civil anterior, y que pretende regresar a Poniente para reclamar sus derechos dinásticos. Tras un largo verano de varios años, el temible invierno se acerca a los Siete Reinos. Lord Eddard \'Ned\' Stark, señor de Invernalia, deja sus dominios para ir a la corte de su amigo, el rey Robert Baratheon, en Desembarco del Rey, la capital de los Siete Reinos. Stark se convierte en la Mano del Rey e intenta desentrañar una maraña de intrigas que pondrá en peligro su vida y la de todos los suyos. Mientras tanto, diversas facciones conspiran con un solo objetivo: apoderarse del trono. ','GOT.jpg','t1.mp4'),(15,20,1,'Serie de TV (2015-2018). 3 temporadas. 39 episodios. Adaptación televisiva de los cómics del abogado de día, Matt Murdock, y superhéroe de noche, Daredevil','daredevil.jpg','t1.mp4'),(16,21,1,'Miniserie de 7 episodios. Kentucky, años 60. En plena Guerra Fría, la joven Beth Harmon (Anya Taylor-Joy) es una huérfana con una aptitud prodigiosa para el ajedrez, que lucha contra sus adicciones mientras trata de convertirse en la mejor jugadora del mundo ganando a los grandes maestros, en especial a los rusos.','gambitodedama.png','t1.mp4'),(17,22,1,'Serie de TV (2013-2022). 6 temporadas. 36 episodios. Una familia de gánsters asentada en Birmingham tras la Primera Guerra Mundial (1914-1918), dirige un local de apuestas hípicas. Las actividades del ambicioso jefe de la banda llaman la atención del Inspector jefe Chester Campbell, un detective de la Real Policía Irlandesa que es enviado desde Belfast para limpiar la ciudad y acabar con la banda.','peakyblinders.jpg','t1.mp4'),(18,23,1,'Serie de TV (2017-2020). 4 temporadas. 49 episodios. El adolescente Clay Jensen (Dylan Minnette) vuelve un día a casa después del colegio y encuentra una misteriosa caja con su nombre. Dentro descubre una cinta grabada por Hannah Baker (Katherine Langford), una compañera de clase por la que sentía algo especial y que se suicidó tan solo dos semanas atrás. En la cinta, Hannah cuenta que hay trece razones por las que ha decidido quitarse la vida. ¿Será Clay una de ellas? Si lo escucha, tendrá oportunidad de conocer cada motivo de su lista.','por13razones.jpg','t1.mp4'),(19,24,1,'Serie de TV (2016). 8 episodios. Homenaje a los clásicos misterios sobrenaturales de los años 80, \"Stranger Things\" es la historia de un niño que desaparece en el pequeño pueblo de Hawkins, Indiana, sin dejar rastro en 1983. En su búsqueda desesperada, tanto sus amigos y familiares como el sheriff local se ven envueltos en un enigma extraordinario: experimentos ultrasecretos, fuerzas paranormales terroríficas y una niña muy, muy rara...','stranger_things-875025085-large.jpg','t1.mp4'),(20,25,1,'Serie de TV (2011-2023). 6 temporadas. Serie antológica creada por Charlie Brooker (\"Dead Set\") que muestra el lado oscuro de la tecnología y cómo esta afecta y puede alterar nuestra vida, a veces con consecuencias tan impredecibles como aterradoras. \"Black Mirror\" comenzó su emisión en 2011 en el canal británico Channel 4, con dos temporadas de tres episodios cada una, y tras producirse un especial de Navidad la serie fue comprada y renovada por Netflix, que ya ha producido tres temporadas más.','blackmirror.jpg','t1.mp4'),(21,26,1,'El misterio de un pueblo de pesadilla en el centro de América, que atrapa a todos los que entran. Sus habitantes luchan por mantener una apariencia de normalidad, pero también deben lidiar con las amenazas del bosque circundante; incluidas las aterradoras criaturas que salen cuando se pone el sol.','from.jpg','t1.mp4'),(23,28,1,'Serie de TV (2020-). 2 temporadas. 12 episodios. La serie se ubica en la estación internacional Polaris VI, en la Antártida. Un reducido grupo de científicos de varios países se encargará de mantener la base en funcionamiento durante la larga noche polar. Pero en mitad del invierno la estación deja de comunicarse con el exterior.','Thehead.jpg','t1.mp4'),(26,31,1,'Serie de TV (2023-). 1 temporada. 9 episodios. Veinte años después de la destrucción de la civilización moderna a causa de un hongo -el cordyceps- que se adueña del cuerpo de los humanos, uno de los supervivientes, Joel, recibe el encargo de sacar a la joven Ellie de una opresiva zona de cuarentena. Juntos cruzan Estados Unidos ayudándose mutuamente para intentar sobrevivir... Adaptación del aclamado videojuego homónimo de Naughty Dog.','thelastofus.jpeg','t1.mp4'),(27,32,1,'Miniserie que transporta a los espectadores al epicentro de la lucha contra la adicción a los opioides que se libra en Estados Unidos, desde la sala de juntas de Purdue Pharma a una castigada comunidad minera de Virginia, pasando por los despachos de la DEA.','dopesick.jpeg','t1.mp4'),(28,33,1,'Serie de televisión que narra el intento de la fundadora de Theranos, Elizabeth Holmes, de revolucionar la industria de la salud después de abandonar la universidad y comenzar una empresa de tecnología.\r\nPosición en rankings FA\r\n87 Ranking: Top 100 Series de TV del 2022','thedropout.jpeg','t1.mp4'),(29,34,1,'El 11 de marzo de 2004, varios puntos de la red de Cercanías madrileña fueron sacudidos por ataques terroristas, provocando la muerte de más de 190 personas. Adaptación de \'Nos vemos en esta vida o en la otra\', el libro de Manuel Jabois en el que radiografiaba la figura de Gabriel Montoya Vidal, apodado \'Baby\', que sería el primer condenado por los atentados por transportar los explosivos desde Asturias a Madrid.','nosvemosenotravida.jpeg','t1.mp4'),(30,35,1,'Frank Castle (Thomas Jane), un agente secreto del FBI con un historial intachable, decide un día abandonar una profesión tan peligrosa para poder tener una vida familiar normal. Pero, precisamente entonces, su vida se hace añicos al cumplirse el peor de sus temores: su familia es asesinada como venganza por su último trabajo. Buscando castigar a los asesinos, al final encuentra lo que menos esperaba: la redención.','punisher.jpeg','t1.mp4'),(31,36,1,'Ambientada en el Japón del siglo XVII, lord Yoshii Toranaga lucha por su vida mientras que sus enemigos en el Consejo de regentes se alían contra él cuando un misterioso barco europeo aparece abandonado cerca de un pueblo pesquero.','shogun.jpeg','t1.mp4'),(32,37,1,'Un icónico vividor, que apenas tiene recursos para mantener su acomodado estilo de vida, contrata a una joven paraguaya para sustituir a la criada recientemente fallecida que le cuidó durante más de 40 años. ','nada.jpeg','t1.mp4'),(33,38,1,'Episodio 4 de la sexta temporada de \'Riverdale\' que realiza un crossover con el personaje de Sabrina Spellman. En el episodio, Cheryl (Madelaine Petsch) estará llevando a cabo un peligroso conjuro que podría marcar la diferencia entre la vida y la muerte de un querido miembro de la familia Blossom. Afortunadamente, la joven va a recibir la ayuda de una experta, la bruja veinteañera más famosa e icónica para varias generaciones, que llegará directa desde Greendale.','riverdale.jpg','t1.mp4'),(34,39,1,'Un soldado estadounidense encarcelado en el Japón de la posguerra entra en el oscuro mundo de la yakuza y adopta su estilo de vida como pago por su libertad.','outsider.jpeg','t1.mp4');
/*!40000 ALTER TABLE `temporades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `surname` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'test','test','test','test@test.test','test',NULL),(2,'','','','','sdfsdf',NULL),(3,'test','test','test','test@test.test','sdfsdf',NULL),(4,'test12','test','test','a@a.es','test',NULL),(5,'test321','test123','test','asdfasdf@asdfasedf.es','scrypt:32768:8:1$o2nocyy4qT1V7qXC$9201bb5d95c27910acfca370c8a879d03ac0807f9b953e0553ba3c2017b1e3fb7e8fc4ab073d2c84b3757ed92b68c43e488daf56ebe0bae4b3c30720c5b0cacf',NULL),(6,'ls','ls','ls','ls@ls.ls','$2b$12$9tUPm5l5E1Tkjk9NHLcS7.yQIDEvaT5mW..8BccZc4Jfh3lv59cNK',NULL),(7,'test1234','test','test','test1234@test.test','$2b$12$Y3vZbkMYDyf.I1wb/0YOWetM/Tgx8aufzhht1Zej2Gj902i2/2GNa',NULL),(8,'test12345','test','test','test12345@test.test','$2b$12$tbYPjAHjudb4Rbjx5Glih.snTtvQQ/FlsLaAIKERxiYrtTtHEpBnm',NULL),(9,'Guillem','Guillem','Farriols','guillem.farriols@outlook.es','guillem123',NULL),(10,'admin','Admin','Admin','admin@guiljanielFilms.es','admin',NULL),(11,'asdf','Guillem','Farriols','testing@test.com','asdf',NULL),(12,'da','da','da','da@gmail.com','da',NULL),(13,'daniel11','daniel11','daniel11','daniel11@gmail.com','daniel11',NULL),(14,'hola','hola','sadf','sdf@gma.com','hola',NULL),(15,'Mama','Carmen','Segura','melinvento@e.e','mama',NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-23 21:50:37
