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
