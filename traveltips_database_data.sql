-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Creato il: Lug 25, 2021 alle 10:06
-- Versione del server: 8.0.24
-- Versione PHP: 7.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `traveltips_database`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `Experience`
--

CREATE TABLE `Experience` (
  `id` int NOT NULL,
  `title` varchar(64) NOT NULL,
  `text` varchar(128) NOT NULL,
  `longText` text NOT NULL,
  `locality` int NOT NULL,
  `idUser` int NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `Experience`
--

INSERT INTO `Experience` (`id`, `title`, `text`, `longText`, `locality`, `idUser`, `date`) VALUES
(7, 'qwe', 'qwe', 'qwe', 2, 3, '2021-06-10 10:00:00'),
(17, 'hg', 'ghf', 'gf', 27, 2, '2021-06-02 19:29:40'),
(18, 'Bel Kebab', 'sdf', 'hg', 28, 3, '2021-06-03 10:35:14'),
(19, 'Titolone 2', 'hg', 'hg', 31, 3, '2021-06-03 10:46:33');

-- --------------------------------------------------------

--
-- Struttura della tabella `ExperienceBooks`
--

CREATE TABLE `ExperienceBooks` (
  `idUser` int NOT NULL,
  `idExperience` int NOT NULL,
  `date` datetime NOT NULL,
  `places` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `ExperienceBooks`
--

INSERT INTO `ExperienceBooks` (`idUser`, `idExperience`, `date`, `places`) VALUES
(3, 18, '2021-06-20 13:00:00', 4);

-- --------------------------------------------------------

--
-- Struttura della tabella `ExperienceDates`
--

CREATE TABLE `ExperienceDates` (
  `idExperience` int NOT NULL,
  `date` datetime NOT NULL,
  `availablePlaces` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `ExperienceDates`
--

INSERT INTO `ExperienceDates` (`idExperience`, `date`, `availablePlaces`) VALUES
(17, '2021-06-03 10:12:20', 10),
(17, '2021-06-03 10:40:07', 12),
(17, '2021-06-03 11:00:07', 11),
(17, '2021-06-06 21:30:00', 10),
(18, '2021-06-06 13:00:00', 14),
(18, '2021-06-13 13:00:00', 14),
(18, '2021-06-20 13:00:00', 14),
(18, '2021-06-27 13:00:00', 14),
(19, '2021-06-18 10:23:00', 20),
(19, '2021-06-24 10:23:00', 20);

-- --------------------------------------------------------

--
-- Struttura della tabella `ExperienceImages`
--

CREATE TABLE `ExperienceImages` (
  `idExperience` int NOT NULL,
  `image` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `ExperienceImages`
--

INSERT INTO `ExperienceImages` (`idExperience`, `image`) VALUES
(17, 'experience_17_0.jpeg'),
(18, 'experience_18_0.jpeg'),
(19, 'experience_19_0.png'),
(19, 'experience_19_1.png');

-- --------------------------------------------------------

--
-- Struttura della tabella `ExperienceLanguages`
--

CREATE TABLE `ExperienceLanguages` (
  `idExperience` int NOT NULL,
  `language` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `ExperienceLanguages`
--

INSERT INTO `ExperienceLanguages` (`idExperience`, `language`) VALUES
(17, 'gf'),
(18, 'g'),
(19, 'gh');

-- --------------------------------------------------------

--
-- Struttura della tabella `ExperienceTags`
--

CREATE TABLE `ExperienceTags` (
  `idExperience` int NOT NULL,
  `tag` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `ExperienceTags`
--

INSERT INTO `ExperienceTags` (`idExperience`, `tag`) VALUES
(17, 'gf'),
(18, 'gh'),
(19, 'hg');

-- --------------------------------------------------------

--
-- Struttura della tabella `ExperienceVotes`
--

CREATE TABLE `ExperienceVotes` (
  `idExperience` int NOT NULL,
  `idUser` int NOT NULL,
  `vote` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `ExperienceVotes`
--

INSERT INTO `ExperienceVotes` (`idExperience`, `idUser`, `vote`) VALUES
(17, 3, 4);

-- --------------------------------------------------------

--
-- Struttura della tabella `Itinerary`
--

CREATE TABLE `Itinerary` (
  `id` int NOT NULL,
  `title` varchar(64) NOT NULL,
  `text` varchar(128) NOT NULL,
  `longText` text NOT NULL,
  `locality` int NOT NULL,
  `idUser` int NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `Itinerary`
--

INSERT INTO `Itinerary` (`id`, `title`, `text`, `longText`, `locality`, `idUser`, `date`) VALUES
(1, 'Weekand a Milano', 'Bel giretto per le vie di milano', 'Primo giorno\nasdasdasd\n\nSecondo Giorno\nasdasd\n\nTerzo giorno\nasdcas', 7, 3, '2021-05-04 04:22:50');

-- --------------------------------------------------------

--
-- Struttura della tabella `ItineraryImages`
--

CREATE TABLE `ItineraryImages` (
  `idItinerary` int NOT NULL,
  `image` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `ItineraryImages`
--

INSERT INTO `ItineraryImages` (`idItinerary`, `image`) VALUES
(1, 'itinerary_1_0.png'),
(1, 'itinerary_1_1.png'),
(1, 'itinerary_1_2.png');

-- --------------------------------------------------------

--
-- Struttura della tabella `ItineraryLanguages`
--

CREATE TABLE `ItineraryLanguages` (
  `idItinerary` int NOT NULL,
  `language` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `ItineraryLanguages`
--

INSERT INTO `ItineraryLanguages` (`idItinerary`, `language`) VALUES
(1, 'italiano');

-- --------------------------------------------------------

--
-- Struttura della tabella `ItineraryTags`
--

CREATE TABLE `ItineraryTags` (
  `idItinerary` int NOT NULL,
  `tag` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `ItineraryTags`
--

INSERT INTO `ItineraryTags` (`idItinerary`, `tag`) VALUES
(1, 'city'),
(1, 'weekand');

-- --------------------------------------------------------

--
-- Struttura della tabella `ItineraryVotes`
--

CREATE TABLE `ItineraryVotes` (
  `idItinerary` int NOT NULL,
  `idUser` int NOT NULL,
  `vote` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `ItineraryVotes`
--

INSERT INTO `ItineraryVotes` (`idItinerary`, `idUser`, `vote`) VALUES
(1, 3, 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `Locality`
--

CREATE TABLE `Locality` (
  `id` int NOT NULL,
  `country` varchar(64) NOT NULL DEFAULT '""',
  `province` varchar(64) NOT NULL DEFAULT '""',
  `city` varchar(64) NOT NULL DEFAULT '""',
  `counter` int NOT NULL COMMENT 'Increment any time this locality is used in other table'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `Locality`
--

INSERT INTO `Locality` (`id`, `country`, `province`, `city`, `counter`) VALUES
(5, 'Italia2', 'Milano2', 'Milano2', 2),
(7, 'Italia', 'Milano', 'Milano', 13),
(11, 'Italia', 'Milano', 'Milano2', 1),
(12, 'Asd', 'Asd', 'Asd', 1),
(18, 'Italia', 'Lombardia', 'Milano', 2),
(19, 'String', 'String', 'String', 1),
(20, 'Italia', 'Sondrio', 'Sondrio', 2),
(25, 'Uy', 'Y', 'Y', 2),
(26, 'I', 'I', 'I', 5),
(27, 'Gf', 'Gf', 'Gf', 3),
(28, 'G', 'Hg', 'H', 1),
(31, 'H', 'Gh', 'G', 1),
(32, 'Italia', 'Torino', 'Orbassano', 2),
(33, 'Italia', 'Torino', 'Torino', 8),
(34, 'Italia', 'Milano', '', 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `LocalityVisited`
--

CREATE TABLE `LocalityVisited` (
  `idUser` int NOT NULL,
  `idLocality` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `LocalityVisited`
--

INSERT INTO `LocalityVisited` (`idUser`, `idLocality`) VALUES
(3, 18);

-- --------------------------------------------------------

--
-- Struttura della tabella `Place`
--

CREATE TABLE `Place` (
  `id` int NOT NULL,
  `title` varchar(64) NOT NULL,
  `text` varchar(300) NOT NULL,
  `locality` int NOT NULL,
  `language` varchar(32) NOT NULL,
  `confirmed` tinyint(1) NOT NULL DEFAULT '0',
  `idUser` int NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `Place`
--

INSERT INTO `Place` (`id`, `title`, `text`, `locality`, `language`, `confirmed`, `idUser`, `date`) VALUES
(12, 'Mole', 'Blla', 33, 'italiano', 0, 3, '2021-06-18 07:24:21');

-- --------------------------------------------------------

--
-- Struttura della tabella `PlaceImages`
--

CREATE TABLE `PlaceImages` (
  `idPlace` int NOT NULL,
  `image` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `PlaceImages`
--

INSERT INTO `PlaceImages` (`idPlace`, `image`) VALUES
(12, 'place_12_0.png'),
(12, 'place_12_1.png');

-- --------------------------------------------------------

--
-- Struttura della tabella `PlaceLanguages`
--

CREATE TABLE `PlaceLanguages` (
  `idPlace` int NOT NULL,
  `language` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `PlaceLanguages`
--

INSERT INTO `PlaceLanguages` (`idPlace`, `language`) VALUES
(12, 'italiano');

-- --------------------------------------------------------

--
-- Struttura della tabella `PlaceReviews`
--

CREATE TABLE `PlaceReviews` (
  `id` int NOT NULL,
  `idPlace` int NOT NULL,
  `idUser` int NOT NULL,
  `text` varchar(300) NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `PlaceReviews`
--

INSERT INTO `PlaceReviews` (`id`, `idPlace`, `idUser`, `text`, `date`) VALUES
(9, 12, 3, 'Prova', '2021-06-20 12:28:44');

-- --------------------------------------------------------

--
-- Struttura della tabella `PlaceReviewsLikes`
--

CREATE TABLE `PlaceReviewsLikes` (
  `idReview` int NOT NULL,
  `idUser` int NOT NULL,
  `like` int NOT NULL DEFAULT '0' COMMENT '0 = none\r\n1 = like\r\n-1 = unlike'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `PlaceTags`
--

CREATE TABLE `PlaceTags` (
  `idPlace` int NOT NULL,
  `tag` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `PlaceTags`
--

INSERT INTO `PlaceTags` (`idPlace`, `tag`) VALUES
(12, 'cinema'),
(12, 'mole');

-- --------------------------------------------------------

--
-- Struttura della tabella `PlaceVotes`
--

CREATE TABLE `PlaceVotes` (
  `idUser` int NOT NULL,
  `idPlace` int NOT NULL,
  `vote` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `PlaceVotes`
--

INSERT INTO `PlaceVotes` (`idUser`, `idPlace`, `vote`) VALUES
(3, 12, 4);

-- --------------------------------------------------------

--
-- Struttura della tabella `Tip`
--

CREATE TABLE `Tip` (
  `id` int NOT NULL,
  `title` varchar(64) NOT NULL,
  `text` varchar(300) NOT NULL,
  `locality` int NOT NULL,
  `idUser` int NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `Tip`
--

INSERT INTO `Tip` (`id`, `title`, `text`, `locality`, `idUser`, `date`) VALUES
(2, 'Bel Kebaba a', 'sda', 20, 3, '2021-05-02 21:39:09');

-- --------------------------------------------------------

--
-- Struttura della tabella `TipLanguages`
--

CREATE TABLE `TipLanguages` (
  `idTip` int NOT NULL,
  `language` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `TipLanguages`
--

INSERT INTO `TipLanguages` (`idTip`, `language`) VALUES
(2, 'italiano');

-- --------------------------------------------------------

--
-- Struttura della tabella `TipTags`
--

CREATE TABLE `TipTags` (
  `idTip` int NOT NULL,
  `tag` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `TipTags`
--

INSERT INTO `TipTags` (`idTip`, `tag`) VALUES
(2, 'city'),
(2, 'kebab');

-- --------------------------------------------------------

--
-- Struttura della tabella `TipVotes`
--

CREATE TABLE `TipVotes` (
  `idTip` int NOT NULL,
  `idUser` int NOT NULL,
  `vote` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `TipVotes`
--

INSERT INTO `TipVotes` (`idTip`, `idUser`, `vote`) VALUES
(2, 3, 4);

-- --------------------------------------------------------

--
-- Struttura della tabella `User`
--

CREATE TABLE `User` (
  `id` int NOT NULL,
  `email` varchar(64) NOT NULL,
  `username` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL,
  `token` varchar(32) DEFAULT NULL,
  `profileImagePath` varchar(32) DEFAULT NULL,
  `home` int DEFAULT NULL,
  `role` int NOT NULL DEFAULT '0' COMMENT '0 = basic user\r\n3 = admin',
  `lastLogin` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `User`
--

INSERT INTO `User` (`id`, `email`, `username`, `password`, `token`, `profileImagePath`, `home`, `role`, `lastLogin`) VALUES
(2, 'falci@live.it', 'falci', '0000', NULL, NULL, 18, 0, NULL),
(3, '***************', 'Angelo Falci', 'agosto1994', '3ygKINMGh0edEfnfL9guxwjhRFnl1hgC', 'profile_3.jpeg', 34, 0, '2021-05-01 09:25:18');

-- --------------------------------------------------------

--
-- Struttura della tabella `UserInterests`
--

CREATE TABLE `UserInterests` (
  `idUser` int NOT NULL,
  `interest` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `UserInterests`
--

INSERT INTO `UserInterests` (`idUser`, `interest`) VALUES
(3, 'bici');

-- --------------------------------------------------------

--
-- Struttura della tabella `UserLanguages`
--

CREATE TABLE `UserLanguages` (
  `idUser` int NOT NULL,
  `language` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `UserPasswordCode`
--

CREATE TABLE `UserPasswordCode` (
  `id` int NOT NULL,
  `token` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `UserStar`
--

CREATE TABLE `UserStar` (
  `idUser` int NOT NULL,
  `idUserFollowed` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `UserStar`
--

INSERT INTO `UserStar` (`idUser`, `idUserFollowed`) VALUES
(2, 3),
(3, 2);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `Experience`
--
ALTER TABLE `Experience`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idUser` (`idUser`),
  ADD KEY `locality` (`locality`);

--
-- Indici per le tabelle `ExperienceBooks`
--
ALTER TABLE `ExperienceBooks`
  ADD PRIMARY KEY (`idUser`,`idExperience`,`date`),
  ADD KEY `idExperience` (`idExperience`,`date`) USING BTREE;

--
-- Indici per le tabelle `ExperienceDates`
--
ALTER TABLE `ExperienceDates`
  ADD PRIMARY KEY (`idExperience`,`date`),
  ADD UNIQUE KEY `idExperience` (`idExperience`,`date`);

--
-- Indici per le tabelle `ExperienceImages`
--
ALTER TABLE `ExperienceImages`
  ADD PRIMARY KEY (`idExperience`,`image`);

--
-- Indici per le tabelle `ExperienceLanguages`
--
ALTER TABLE `ExperienceLanguages`
  ADD PRIMARY KEY (`idExperience`,`language`);

--
-- Indici per le tabelle `ExperienceTags`
--
ALTER TABLE `ExperienceTags`
  ADD PRIMARY KEY (`idExperience`,`tag`);

--
-- Indici per le tabelle `ExperienceVotes`
--
ALTER TABLE `ExperienceVotes`
  ADD PRIMARY KEY (`idExperience`,`idUser`),
  ADD KEY `idUser` (`idUser`);

--
-- Indici per le tabelle `Itinerary`
--
ALTER TABLE `Itinerary`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idUser` (`idUser`),
  ADD KEY `locality` (`locality`);

--
-- Indici per le tabelle `ItineraryImages`
--
ALTER TABLE `ItineraryImages`
  ADD PRIMARY KEY (`idItinerary`,`image`);

--
-- Indici per le tabelle `ItineraryLanguages`
--
ALTER TABLE `ItineraryLanguages`
  ADD PRIMARY KEY (`idItinerary`,`language`);

--
-- Indici per le tabelle `ItineraryTags`
--
ALTER TABLE `ItineraryTags`
  ADD PRIMARY KEY (`idItinerary`,`tag`);

--
-- Indici per le tabelle `ItineraryVotes`
--
ALTER TABLE `ItineraryVotes`
  ADD PRIMARY KEY (`idItinerary`,`idUser`),
  ADD KEY `idUser` (`idUser`);

--
-- Indici per le tabelle `Locality`
--
ALTER TABLE `Locality`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `country` (`country`,`province`,`city`);

--
-- Indici per le tabelle `LocalityVisited`
--
ALTER TABLE `LocalityVisited`
  ADD PRIMARY KEY (`idUser`,`idLocality`),
  ADD KEY `idLocality` (`idLocality`);

--
-- Indici per le tabelle `Place`
--
ALTER TABLE `Place`
  ADD PRIMARY KEY (`id`),
  ADD KEY `locality` (`locality`),
  ADD KEY `idUser` (`idUser`);

--
-- Indici per le tabelle `PlaceImages`
--
ALTER TABLE `PlaceImages`
  ADD PRIMARY KEY (`idPlace`,`image`);

--
-- Indici per le tabelle `PlaceLanguages`
--
ALTER TABLE `PlaceLanguages`
  ADD PRIMARY KEY (`idPlace`,`language`);

--
-- Indici per le tabelle `PlaceReviews`
--
ALTER TABLE `PlaceReviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idPlace` (`idPlace`,`idUser`),
  ADD KEY `idUser` (`idUser`);

--
-- Indici per le tabelle `PlaceReviewsLikes`
--
ALTER TABLE `PlaceReviewsLikes`
  ADD KEY `idReview` (`idReview`,`idUser`),
  ADD KEY `idUser` (`idUser`);

--
-- Indici per le tabelle `PlaceTags`
--
ALTER TABLE `PlaceTags`
  ADD PRIMARY KEY (`idPlace`,`tag`);

--
-- Indici per le tabelle `PlaceVotes`
--
ALTER TABLE `PlaceVotes`
  ADD KEY `idUser` (`idUser`,`idPlace`),
  ADD KEY `idPlace` (`idPlace`);

--
-- Indici per le tabelle `Tip`
--
ALTER TABLE `Tip`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idUser` (`idUser`),
  ADD KEY `locality` (`locality`);

--
-- Indici per le tabelle `TipLanguages`
--
ALTER TABLE `TipLanguages`
  ADD PRIMARY KEY (`idTip`,`language`);

--
-- Indici per le tabelle `TipTags`
--
ALTER TABLE `TipTags`
  ADD PRIMARY KEY (`idTip`,`tag`);

--
-- Indici per le tabelle `TipVotes`
--
ALTER TABLE `TipVotes`
  ADD PRIMARY KEY (`idTip`,`idUser`),
  ADD KEY `idUser` (`idUser`);

--
-- Indici per le tabelle `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `home` (`home`);

--
-- Indici per le tabelle `UserInterests`
--
ALTER TABLE `UserInterests`
  ADD PRIMARY KEY (`idUser`,`interest`);

--
-- Indici per le tabelle `UserLanguages`
--
ALTER TABLE `UserLanguages`
  ADD PRIMARY KEY (`idUser`,`language`);

--
-- Indici per le tabelle `UserPasswordCode`
--
ALTER TABLE `UserPasswordCode`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `UserStar`
--
ALTER TABLE `UserStar`
  ADD PRIMARY KEY (`idUser`,`idUserFollowed`),
  ADD KEY `UserStar_ibfk_1` (`idUser`),
  ADD KEY `UserStar_ibfk_2` (`idUserFollowed`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `Experience`
--
ALTER TABLE `Experience`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT per la tabella `Itinerary`
--
ALTER TABLE `Itinerary`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT per la tabella `Locality`
--
ALTER TABLE `Locality`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT per la tabella `Place`
--
ALTER TABLE `Place`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT per la tabella `PlaceReviews`
--
ALTER TABLE `PlaceReviews`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT per la tabella `Tip`
--
ALTER TABLE `Tip`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT per la tabella `User`
--
ALTER TABLE `User`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `Experience`
--
ALTER TABLE `Experience`
  ADD CONSTRAINT `Experience_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `ExperienceBooks`
--
ALTER TABLE `ExperienceBooks`
  ADD CONSTRAINT `ExperienceBooks_ibfk_1` FOREIGN KEY (`idExperience`) REFERENCES `Experience` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ExperienceBooks_ibfk_2` FOREIGN KEY (`idExperience`,`date`) REFERENCES `ExperienceDates` (`idExperience`, `date`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ExperienceBooks_ibfk_3` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `ExperienceDates`
--
ALTER TABLE `ExperienceDates`
  ADD CONSTRAINT `ExperienceDates_ibfk_1` FOREIGN KEY (`idExperience`) REFERENCES `Experience` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `ExperienceImages`
--
ALTER TABLE `ExperienceImages`
  ADD CONSTRAINT `ExperienceImages_ibfk_1` FOREIGN KEY (`idExperience`) REFERENCES `Experience` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `ExperienceLanguages`
--
ALTER TABLE `ExperienceLanguages`
  ADD CONSTRAINT `ExperienceLanguages_ibfk_1` FOREIGN KEY (`idExperience`) REFERENCES `Experience` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `ExperienceTags`
--
ALTER TABLE `ExperienceTags`
  ADD CONSTRAINT `ExperienceTags_ibfk_1` FOREIGN KEY (`idExperience`) REFERENCES `Experience` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `ExperienceVotes`
--
ALTER TABLE `ExperienceVotes`
  ADD CONSTRAINT `ExperienceVotes_ibfk_1` FOREIGN KEY (`idExperience`) REFERENCES `Experience` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ExperienceVotes_ibfk_2` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `Itinerary`
--
ALTER TABLE `Itinerary`
  ADD CONSTRAINT `Itinerary_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `ItineraryImages`
--
ALTER TABLE `ItineraryImages`
  ADD CONSTRAINT `ItineraryImages_ibfk_1` FOREIGN KEY (`idItinerary`) REFERENCES `Itinerary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `ItineraryLanguages`
--
ALTER TABLE `ItineraryLanguages`
  ADD CONSTRAINT `ItineraryLanguages_ibfk_1` FOREIGN KEY (`idItinerary`) REFERENCES `Itinerary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `ItineraryTags`
--
ALTER TABLE `ItineraryTags`
  ADD CONSTRAINT `ItineraryTags_ibfk_1` FOREIGN KEY (`idItinerary`) REFERENCES `Itinerary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `ItineraryVotes`
--
ALTER TABLE `ItineraryVotes`
  ADD CONSTRAINT `ItineraryVotes_ibfk_1` FOREIGN KEY (`idItinerary`) REFERENCES `Itinerary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ItineraryVotes_ibfk_2` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `LocalityVisited`
--
ALTER TABLE `LocalityVisited`
  ADD CONSTRAINT `LocalityVisited_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `Place`
--
ALTER TABLE `Place`
  ADD CONSTRAINT `Place_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `PlaceImages`
--
ALTER TABLE `PlaceImages`
  ADD CONSTRAINT `PlaceImages_ibfk_1` FOREIGN KEY (`idPlace`) REFERENCES `Place` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `PlaceLanguages`
--
ALTER TABLE `PlaceLanguages`
  ADD CONSTRAINT `PlaceLanguages_ibfk_1` FOREIGN KEY (`idPlace`) REFERENCES `Place` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `PlaceReviews`
--
ALTER TABLE `PlaceReviews`
  ADD CONSTRAINT `PlaceReviews_ibfk_1` FOREIGN KEY (`idPlace`) REFERENCES `Place` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `PlaceReviews_ibfk_2` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `PlaceReviewsLikes`
--
ALTER TABLE `PlaceReviewsLikes`
  ADD CONSTRAINT `PlaceReviewsVotes_ibfk_1` FOREIGN KEY (`idReview`) REFERENCES `PlaceReviews` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `PlaceReviewsVotes_ibfk_2` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `PlaceTags`
--
ALTER TABLE `PlaceTags`
  ADD CONSTRAINT `PlaceTags_ibfk_1` FOREIGN KEY (`idPlace`) REFERENCES `Place` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `PlaceVotes`
--
ALTER TABLE `PlaceVotes`
  ADD CONSTRAINT `PlaceVotes_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `PlaceVotes_ibfk_2` FOREIGN KEY (`idPlace`) REFERENCES `Place` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `Tip`
--
ALTER TABLE `Tip`
  ADD CONSTRAINT `Tip_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `TipLanguages`
--
ALTER TABLE `TipLanguages`
  ADD CONSTRAINT `TipLanguages_ibfk_1` FOREIGN KEY (`idTip`) REFERENCES `Tip` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `TipTags`
--
ALTER TABLE `TipTags`
  ADD CONSTRAINT `TipTags_ibfk_1` FOREIGN KEY (`idTip`) REFERENCES `Tip` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `TipVotes`
--
ALTER TABLE `TipVotes`
  ADD CONSTRAINT `TipVotes_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `TipVotes_ibfk_2` FOREIGN KEY (`idTip`) REFERENCES `Tip` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `User`
--
ALTER TABLE `User`
  ADD CONSTRAINT `User_ibfk_1` FOREIGN KEY (`home`) REFERENCES `Locality` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `UserInterests`
--
ALTER TABLE `UserInterests`
  ADD CONSTRAINT `UserInterests_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `UserLanguages`
--
ALTER TABLE `UserLanguages`
  ADD CONSTRAINT `UserLanguages_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `UserPasswordCode`
--
ALTER TABLE `UserPasswordCode`
  ADD CONSTRAINT `UserPasswordCode_ibfk_1` FOREIGN KEY (`id`) REFERENCES `User` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Limiti per la tabella `UserStar`
--
ALTER TABLE `UserStar`
  ADD CONSTRAINT `UserStar_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `UserStar_ibfk_2` FOREIGN KEY (`idUserFollowed`) REFERENCES `User` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
