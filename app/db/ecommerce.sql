/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP TABLE IF EXISTS `Categories`;
CREATE TABLE `Categories` (
  `categoryId` int NOT NULL,
  `categoryName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`categoryId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `Customers`;
CREATE TABLE `Customers` (
  `customerId` int NOT NULL,
  `firstName` varchar(50) DEFAULT NULL,
  `lastName` varchar(50) DEFAULT NULL,
  `addressState` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`customerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `Orders`;
CREATE TABLE `Orders` (
  `orderId` int NOT NULL,
  `customerId` int DEFAULT NULL,
  `productId` int DEFAULT NULL,
  `orderDate` date DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`orderId`),
  KEY `customerId` (`customerId`),
  KEY `productId` (`productId`),
  CONSTRAINT `Orders_ibfk_1` FOREIGN KEY (`customerId`) REFERENCES `Customers` (`customerId`) ON DELETE CASCADE,
  CONSTRAINT `Orders_ibfk_2` FOREIGN KEY (`productId`) REFERENCES `Products` (`productId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `Products`;
CREATE TABLE `Products` (
  `productId` int NOT NULL,
  `productName` varchar(100) DEFAULT NULL,
  `categoryId` int DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`productId`),
  KEY `categoryId` (`categoryId`),
  CONSTRAINT `Products_ibfk_1` FOREIGN KEY (`categoryId`) REFERENCES `Categories` (`categoryId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `Reviews`;
CREATE TABLE `Reviews` (
  `reviewId` int NOT NULL,
  `customerId` int DEFAULT NULL,
  `productId` int DEFAULT NULL,
  `rating` int DEFAULT NULL,
  PRIMARY KEY (`reviewId`),
  KEY `customerId` (`customerId`),
  KEY `productId` (`productId`),
  CONSTRAINT `Reviews_ibfk_1` FOREIGN KEY (`customerId`) REFERENCES `Customers` (`customerId`),
  CONSTRAINT `Reviews_ibfk_2` FOREIGN KEY (`productId`) REFERENCES `Products` (`productId`),
  CONSTRAINT `Reviews_chk_1` CHECK ((`rating` between 1 and 10))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `Categories` (`categoryId`, `categoryName`) VALUES
(1, 'Electronics');
INSERT INTO `Categories` (`categoryId`, `categoryName`) VALUES
(2, 'Books');
INSERT INTO `Categories` (`categoryId`, `categoryName`) VALUES
(3, 'Automotive');
INSERT INTO `Categories` (`categoryId`, `categoryName`) VALUES
(4, 'Office Supplies');

INSERT INTO `Customers` (`customerId`, `firstName`, `lastName`, `addressState`) VALUES
(1, 'John', 'Doe', 'Illinois');
INSERT INTO `Customers` (`customerId`, `firstName`, `lastName`, `addressState`) VALUES
(2, 'Jane', 'Smith', 'Indiana');
INSERT INTO `Customers` (`customerId`, `firstName`, `lastName`, `addressState`) VALUES
(3, 'Michael', 'Brown', 'Wisconsin');
INSERT INTO `Customers` (`customerId`, `firstName`, `lastName`, `addressState`) VALUES
(4, 'Emily', 'Johnson', 'Michigan'),
(5, 'Robert', 'Davis', 'Illinois'),
(6, 'Linda', 'Garcia', 'Indiana'),
(7, 'William', 'Martinez', 'Wisconsin'),
(8, 'Elizabeth', 'Taylor', 'Michigan'),
(9, 'David', 'Wilson', 'Illinois'),
(10, 'Susan', 'Anderson', 'Indiana'),
(11, 'Joseph', 'Thomas', 'Wisconsin'),
(12, 'Karen', 'Jackson', 'Michigan'),
(13, 'Charles', 'White', 'Illinois'),
(14, 'Patricia', 'Harris', 'Indiana'),
(15, 'Christopher', 'Martin', 'Wisconsin'),
(16, 'Barbara', 'Thompson', 'Michigan'),
(17, 'Daniel', 'Garcia', 'Illinois'),
(18, 'Jessica', 'Martinez', 'Indiana'),
(19, 'Matthew', 'Rodriguez', 'Wisconsin'),
(20, 'Sarah', 'Lewis', 'Michigan'),
(21, 'Anthony', 'Lee', 'Illinois'),
(22, 'Mary', 'Walker', 'Indiana'),
(23, 'Mark', 'Hall', 'Wisconsin'),
(24, 'Jennifer', 'Allen', 'Michigan'),
(25, 'Paul', 'Young', 'Illinois'),
(26, 'Sandra', 'Hernandez', 'Indiana'),
(27, 'George', 'King', 'Wisconsin'),
(28, 'Laura', 'Wright', 'Michigan'),
(29, 'Andrew', 'Lopez', 'Illinois'),
(30, 'Betty', 'Hill', 'Indiana'),
(31, 'Joshua', 'Scott', 'Wisconsin'),
(32, 'Dorothy', 'Green', 'Michigan'),
(33, 'Ryan', 'Adams', 'Illinois'),
(34, 'Sharon', 'Baker', 'Indiana'),
(35, 'Jacob', 'Gonzalez', 'Wisconsin'),
(36, 'Nancy', 'Nelson', 'Michigan'),
(37, 'Gary', 'Carter', 'Illinois'),
(38, 'Betty', 'Mitchell', 'Indiana'),
(39, 'Walter', 'Perez', 'Wisconsin'),
(40, 'Lisa', 'Roberts', 'Michigan');

INSERT INTO `Orders` (`orderId`, `customerId`, `productId`, `orderDate`, `quantity`) VALUES
(1, 1, 1, '2021-01-15', 2);
INSERT INTO `Orders` (`orderId`, `customerId`, `productId`, `orderDate`, `quantity`) VALUES
(2, 2, 3, '2021-03-20', 1);
INSERT INTO `Orders` (`orderId`, `customerId`, `productId`, `orderDate`, `quantity`) VALUES
(3, 3, 5, '2021-05-25', 3);
INSERT INTO `Orders` (`orderId`, `customerId`, `productId`, `orderDate`, `quantity`) VALUES
(4, 4, 2, '2021-07-30', 2),
(5, 5, 4, '2021-09-10', 1),
(6, 6, 6, '2021-11-01', 2),
(7, 7, 7, '2022-01-15', 1),
(8, 8, 8, '2022-02-18', 1),
(9, 9, 9, '2022-03-25', 2),
(10, 10, 10, '2022-04-10', 3),
(11, 11, 11, '2022-05-20', 1),
(12, 12, 12, '2022-06-15', 2),
(13, 13, 13, '2022-07-01', 1),
(14, 14, 14, '2022-08-08', 3),
(15, 15, 15, '2022-09-19', 2),
(16, 16, 1, '2022-10-10', 1),
(17, 17, 2, '2022-11-15', 3),
(18, 18, 3, '2022-12-05', 1),
(19, 19, 4, '2022-12-20', 2),
(20, 20, 5, '2022-01-01', 1),
(21, 21, 6, '2021-02-14', 3),
(22, 22, 7, '2021-03-30', 1),
(23, 23, 8, '2021-04-20', 2),
(24, 24, 9, '2021-05-15', 1),
(25, 25, 10, '2021-06-30', 3),
(26, 26, 11, '2021-07-18', 2),
(27, 27, 12, '2021-08-15', 1),
(28, 28, 13, '2021-09-25', 2),
(29, 29, 14, '2021-10-05', 1),
(30, 30, 15, '2021-11-12', 3),
(31, 31, 1, '2021-12-20', 2),
(32, 32, 2, '2022-01-25', 1),
(33, 33, 3, '2022-02-15', 3),
(34, 34, 4, '2022-03-10', 2),
(35, 35, 5, '2022-04-18', 1),
(36, 36, 6, '2022-05-22', 3),
(37, 37, 7, '2022-06-05', 2),
(38, 38, 8, '2022-07-25', 1),
(39, 39, 9, '2022-08-10', 2),
(40, 40, 10, '2022-09-15', 1),
(41, 1, 11, '2021-01-25', 3),
(42, 2, 12, '2021-02-20', 2),
(43, 3, 13, '2021-03-15', 1),
(44, 4, 14, '2021-04-10', 2),
(45, 5, 15, '2021-05-05', 3),
(46, 6, 1, '2021-06-15', 1),
(47, 7, 2, '2021-07-10', 2),
(48, 8, 3, '2021-08-05', 1),
(49, 9, 4, '2021-09-25', 2),
(50, 10, 5, '2021-10-15', 3),
(51, 11, 6, '2021-11-10', 1),
(52, 12, 7, '2021-12-20', 2),
(53, 13, 8, '2022-01-15', 1),
(54, 14, 9, '2022-02-05', 3),
(55, 15, 10, '2022-03-10', 2),
(56, 16, 11, '2022-04-20', 1),
(57, 17, 12, '2022-05-25', 3),
(58, 18, 13, '2022-06-15', 2),
(59, 19, 14, '2022-07-05', 1),
(60, 20, 15, '2022-08-10', 3),
(61, 21, 1, '2021-01-18', 2),
(62, 22, 2, '2021-02-14', 1),
(63, 23, 3, '2021-03-25', 2),
(64, 24, 4, '2021-04-12', 1),
(65, 25, 5, '2021-05-20', 3),
(66, 26, 6, '2021-06-18', 2),
(67, 27, 7, '2021-07-15', 1),
(68, 28, 8, '2021-08-25', 2),
(69, 29, 9, '2021-09-10', 1),
(70, 30, 10, '2021-10-22', 3),
(71, 31, 11, '2021-11-11', 2),
(72, 32, 12, '2021-12-15', 1),
(73, 33, 13, '2022-01-30', 2),
(74, 34, 14, '2022-02-20', 1),
(75, 35, 15, '2022-03-12', 3),
(76, 36, 1, '2022-04-25', 2),
(77, 37, 2, '2022-05-15', 1),
(78, 38, 3, '2022-06-10', 3),
(79, 39, 4, '2022-07-20', 2),
(80, 40, 5, '2022-08-08', 1),
(81, 1, 6, '2021-09-12', 2),
(82, 2, 7, '2021-10-10', 1),
(83, 3, 8, '2021-11-05', 3),
(84, 4, 9, '2021-12-20', 2),
(85, 5, 10, '2022-01-18', 1),
(86, 6, 11, '2022-02-15', 2),
(87, 7, 12, '2022-03-10', 3),
(88, 8, 13, '2022-04-20', 1),
(89, 9, 14, '2022-05-25', 2),
(90, 10, 15, '2022-06-18', 1),
(91, 11, 1, '2022-07-12', 3),
(92, 12, 2, '2022-08-22', 2),
(93, 13, 3, '2022-09-10', 1),
(94, 14, 4, '2022-10-05', 2),
(95, 15, 5, '2022-11-01', 3),
(96, 16, 6, '2022-12-10', 1),
(97, 17, 7, '2021-01-08', 2),
(98, 18, 8, '2021-02-12', 1),
(99, 19, 9, '2021-03-18', 3),
(100, 20, 10, '2021-04-22', 2);

INSERT INTO `Products` (`productId`, `productName`, `categoryId`, `price`) VALUES
(1, 'Smartphone', 1, '699.99');
INSERT INTO `Products` (`productId`, `productName`, `categoryId`, `price`) VALUES
(2, 'Laptop', 1, '1199.99');
INSERT INTO `Products` (`productId`, `productName`, `categoryId`, `price`) VALUES
(3, 'Bluetooth Speaker', 1, '49.99');
INSERT INTO `Products` (`productId`, `productName`, `categoryId`, `price`) VALUES
(4, 'Noise Canceling Headphones', 1, '249.99'),
(5, 'Fiction Novel', 2, '14.99'),
(6, 'Science Textbook', 2, '79.99'),
(7, 'History Book', 2, '19.99'),
(8, 'Car Seat Cover', 3, '49.99'),
(9, 'Windshield Wipers', 3, '15.99'),
(10, 'Tire Inflator', 3, '29.99'),
(11, 'Car Vacuum Cleaner', 3, '39.99'),
(12, 'Desk Organizer', 4, '19.99'),
(13, 'Ballpoint Pens - Pack of 20', 4, '5.99'),
(14, 'Wireless Mouse', 4, '12.99'),
(15, 'Notebook - Pack of 5', 4, '8.99');

INSERT INTO `Reviews` (`reviewId`, `customerId`, `productId`, `rating`) VALUES
(1, 1, 1, 8);
INSERT INTO `Reviews` (`reviewId`, `customerId`, `productId`, `rating`) VALUES
(2, 2, 3, 7);
INSERT INTO `Reviews` (`reviewId`, `customerId`, `productId`, `rating`) VALUES
(3, 3, 5, 9);
INSERT INTO `Reviews` (`reviewId`, `customerId`, `productId`, `rating`) VALUES
(4, 4, 2, 6),
(5, 5, 4, 10),
(6, 6, 6, 5),
(7, 7, 7, 4),
(8, 8, 8, 7),
(9, 9, 9, 6),
(10, 10, 10, 8),
(11, 11, 11, 7),
(12, 12, 12, 3),
(13, 13, 13, 9),
(14, 14, 14, 4),
(15, 15, 15, 2),
(16, 16, 1, 6),
(17, 17, 2, 10),
(18, 18, 3, 5),
(19, 19, 4, 9),
(20, 20, 5, 7),
(21, 21, 6, 3),
(22, 22, 7, 8),
(23, 23, 8, 5),
(24, 24, 9, 6),
(25, 25, 10, 7),
(26, 26, 11, 4),
(27, 27, 12, 10),
(28, 28, 13, 3),
(29, 29, 14, 6),
(30, 30, 15, 8),
(31, 31, 1, 5),
(32, 32, 2, 7),
(33, 33, 3, 9),
(34, 34, 4, 6),
(35, 35, 5, 8),
(36, 36, 6, 7),
(37, 37, 7, 2),
(38, 38, 8, 4),
(39, 39, 9, 10),
(40, 40, 10, 1),
(41, 1, 11, 9),
(42, 2, 12, 3),
(43, 3, 13, 5),
(44, 4, 14, 7),
(45, 5, 15, 6),
(46, 6, 1, 8),
(47, 7, 2, 4),
(48, 8, 3, 6),
(49, 9, 4, 5),
(50, 10, 5, 9),
(51, 11, 6, 7),
(52, 12, 7, 3),
(53, 13, 8, 6),
(54, 14, 9, 10),
(55, 15, 10, 2),
(56, 16, 11, 8),
(57, 17, 12, 7),
(58, 18, 13, 4),
(59, 19, 14, 5),
(60, 20, 15, 9);


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;