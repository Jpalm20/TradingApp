CREATE TABLE `User` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `birthday` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `street_address` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `Session` (
  `session_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `token` varchar(500) NOT NULL,
  `expiration` datetime NOT NULL,
  PRIMARY KEY (`session_id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `Resetcode` (
  `resetcode_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `code` varchar(255) NOT NULL,
  `expiration` datetime NOT NULL,
  PRIMARY KEY (`resetcode_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `resetcode_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `Trade` (
  `trade_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `trade_type` varchar(255) DEFAULT NULL,
  `security_type` varchar(255) DEFAULT NULL,
  `ticker_name` varchar(255) DEFAULT NULL,
  `trade_date` varchar(255) DEFAULT NULL,
  `expiry` varchar(255) DEFAULT NULL,
  `strike` float DEFAULT NULL,
  `buy_value` float DEFAULT NULL,
  `units` int DEFAULT NULL,
  `rr` varchar(255) DEFAULT NULL,
  `pnl` float DEFAULT NULL,
  `percent_wl` float DEFAULT NULL,
  `comments` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`trade_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `trade_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `Accountvalue` (
  `accountvalue_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `accountvalue` float NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`accountvalue_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `accountvalue_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3270 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

ALTER TABLE user ADD COLUMN account_value_optin BOOLEAN DEFAULT FALSE;

UPDATE user SET account_value_optin = false;

SET GLOBAL time_zone = '+00:00';
SET time_zone = '+00:00';

CREATE EVENT CopyAccountValueEvent
ON SCHEDULE EVERY 24 HOUR
STARTS '2023-07-06 00:00:00'
DO
  CALL CopyAccountValue();

CREATE PROCEDURE `CopyAccountValue`()
BEGIN
	-- Insert account value for the current day
	INSERT INTO accountvalue (user_id, date, accountvalue)
	SELECT u.user_id, UTC_DATE(), COALESCE(av.accountvalue, 0)
	FROM user u
	LEFT JOIN accountvalue av ON av.user_id = u.user_id AND av.date = UTC_DATE() - INTERVAL 1 DAY
    WHERE NOT EXISTS (
		SELECT 1 FROM accountvalue WHERE user_id = u.user_id AND date = UTC_DATE()
	);
END

