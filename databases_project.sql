-- PostgreSQL Database Dump
-- Converted from MySQL for Supabase compatibility
-- Database: databases_project

-- Remove MySQL-specific settings and use PostgreSQL equivalents
BEGIN;

--
-- Table structure for table airline
--

DROP TABLE IF EXISTS airline CASCADE;
CREATE TABLE airline (
  airline_name VARCHAR(100) NOT NULL,
  PRIMARY KEY (airline_name)
);

--
-- Dumping data for table airline
--

INSERT INTO airline (airline_name) VALUES
('JetBlue');

-- --------------------------------------------------------

--
-- Table structure for table airline_staff
--

DROP TABLE IF EXISTS airline_staff CASCADE;
CREATE TABLE airline_staff (
  username VARCHAR(100) NOT NULL,
  airline_name VARCHAR(100) NOT NULL,
  password VARCHAR(100) DEFAULT NULL,
  first_name VARCHAR(100) DEFAULT NULL,
  last_name VARCHAR(100) DEFAULT NULL,
  date_of_birth DATE DEFAULT NULL,
  PRIMARY KEY (username, airline_name),
  UNIQUE (username),
  FOREIGN KEY (airline_name) REFERENCES airline(airline_name)
);

--
-- Dumping data for table airline_staff
--

INSERT INTO airline_staff (username, airline_name, password, first_name, last_name, date_of_birth) VALUES
('admin', 'JetBlue', 'e2fc714c4727ee9395f324cd2e7f331f', 'Roe', 'Jones', '1978-05-25');

-- --------------------------------------------------------

--
-- Table structure for table airplane
--

DROP TABLE IF EXISTS airplane CASCADE;
CREATE TABLE airplane (
  airplane_id VARCHAR(100) NOT NULL,
  airline_name VARCHAR(100) NOT NULL,
  number_of_seats INTEGER DEFAULT NULL,
  manufacturing_company VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (airplane_id),
  FOREIGN KEY (airline_name) REFERENCES airline(airline_name)
);

--
-- Dumping data for table airplane
--

INSERT INTO airplane (airplane_id, airline_name, number_of_seats, manufacturing_company) VALUES
('B2374', 'JetBlue', 50, 'Boeing'),
('10', 'JetBlue', 4, 'Boeing'),
('3', 'JetBlue', 50, 'Boeing'),
('2', 'JetBlue', 4, 'Airbus'),
('1', 'JetBlue', 4, 'Boeing');

-- --------------------------------------------------------

--
-- Table structure for table airport
--

DROP TABLE IF EXISTS airport CASCADE;
CREATE TABLE airport (
  airport_code VARCHAR(100) NOT NULL,
  airport_name VARCHAR(100) DEFAULT NULL,
  city VARCHAR(100) DEFAULT NULL,
  country VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (airport_code)
);

--
-- Dumping data for table airport
--

INSERT INTO airport (airport_code, airport_name, city, country) VALUES
('HKA', 'HKA', 'Hong Kong', 'China'),
('LAX', 'LAX', 'Los Angeles', 'USA'),
('SFO', 'SFO', 'San Francisco', 'USA'),
('BEI', 'BEI', 'Beijing', 'China'),
('PVG', 'PVG', 'Shanghai', 'China'),
('BOS', 'BOS', 'Boston', 'USA'),
('JFK', 'JFK', 'NYC', 'USA'),
('SHEN', 'SHEN', 'Shenzhen', 'China'),
('CDG', 'CDG', 'Paris', 'France'),
('EWK', 'Newark Airport', 'New York', 'NJ');

-- --------------------------------------------------------

--
-- Table structure for table customers
--

DROP TABLE IF EXISTS customers CASCADE;
CREATE TABLE customers (
  email VARCHAR(100) NOT NULL,
  first_name VARCHAR(100) DEFAULT NULL,
  last_name VARCHAR(100) DEFAULT NULL,
  password VARCHAR(100) DEFAULT NULL,
  building_number INTEGER DEFAULT NULL,
  street VARCHAR(100) DEFAULT NULL,
  city VARCHAR(100) DEFAULT NULL,
  state VARCHAR(100) DEFAULT NULL,
  phone_number VARCHAR(100) DEFAULT NULL,
  passport_number VARCHAR(100) DEFAULT NULL,
  passport_country VARCHAR(100) DEFAULT NULL,
  passport_expiration DATE DEFAULT NULL,
  date_of_birth DATE DEFAULT NULL,
  PRIMARY KEY (email)
);

--
-- Dumping data for table customers
--

INSERT INTO customers (email, first_name, last_name, password, building_number, street, city, state, phone_number, passport_number, passport_country, passport_expiration, date_of_birth) VALUES
('user3@nyu.edu', 'User', '3', '81dc9bdb52d04dc20036dbd8313ed055', 1890, 'Jay St', 'Brookly', 'New York', '12343244324', '54324', 'USA', '2025-09-24', '1999-09-19'),
('user2@nyu.edu', 'User', '2', '81dc9bdb52d04dc20036dbd8313ed055', 1890, 'Jay St', 'Brooklyn', 'New York', '12343234323', '54323', 'USA', '2025-10-24', '1999-10-19'),
('user1@nyu.edu', 'User', '1', '81dc9bdb52d04dc20036dbd8313ed055', 5405, 'Jay St', 'Brooklyn', 'New York', '12343224322', '54322', 'USA', '2025-12-25', '1999-11-19'),
('testcustomer@nyu.edu', 'Test ', 'Customer 1', '81dc9bdb52d04dc20036dbd8313ed055', 1555, 'Jay St', 'Brooklyn', 'New York', '12343214321', '54321', 'USA', '2025-12-24', '1999-12-19');

-- --------------------------------------------------------

--
-- Table structure for table flight
--

DROP TABLE IF EXISTS flight CASCADE;
CREATE TABLE flight (
  airline_name VARCHAR(100) NOT NULL,
  airplane_id VARCHAR(100) NOT NULL,
  flight_number VARCHAR(100) NOT NULL,
  airport_code VARCHAR(100) NOT NULL,
  departure_date_time TIMESTAMP NOT NULL,
  arrival_date_time TIMESTAMP DEFAULT NULL,
  base_price DECIMAL(10,2) DEFAULT NULL,
  airplane_number VARCHAR(100) DEFAULT NULL,
  flight_status VARCHAR(100) DEFAULT 'On Time',
  arrival_airport_code VARCHAR(100) DEFAULT NULL,
  departure_airport_code VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (flight_number, departure_date_time),
  FOREIGN KEY (airline_name) REFERENCES airline(airline_name),
  FOREIGN KEY (airplane_id) REFERENCES airplane(airplane_id),
  FOREIGN KEY (airport_code) REFERENCES airport(airport_code)
);

--
-- Dumping data for table flight
--

INSERT INTO flight (airline_name, airplane_id, flight_number, airport_code, departure_date_time, arrival_date_time, base_price, airplane_number, flight_status, arrival_airport_code, departure_airport_code) VALUES
('JetBlue', 'B2374', '889', 'JFK', '2025-06-13 21:56:00', '2025-06-28 21:56:00', 343343.00, '446', 'On Time', 'JFK', 'MIA'),
('JetBlue', 'B2374', '754', 'LAX', '2025-06-14 20:54:00', '2025-06-14 22:54:00', 333.00, '446', 'Delayed', 'LAX', 'MIA'),
('JetBlue', '10', '388', 'JFK', '2025-05-07 19:25:00', '2025-05-07 21:25:00', 100.00, '10', 'On Time', 'CDG', 'JFK'),
('JetBlue', '3', '839', 'SHEN', '2024-05-26 13:25:25', '2024-05-26 16:50:25', 300.00, NULL, 'on-time', 'BEI', 'SHEN'),
('JetBlue', '1', '715', 'PVG', '2025-02-28 10:25:25', '2025-02-28 13:50:25', 500.00, NULL, 'delayed', 'BEI', 'PVG'),
('JetBlue', '1', '296', 'PVG', '2025-05-30 13:25:25', '2025-05-30 16:50:25', 3000.00, NULL, 'Delayed', 'SFO', 'PVG'),
('JetBlue', '3', '134', 'JFK', '2024-12-12 13:25:25', '2024-12-12 16:50:25', 300.00, NULL, 'delayed', 'BOS', 'JFK'),
('JetBlue', '2', '207', 'LAX', '2025-08-02 13:25:25', '2025-08-02 16:50:25', 300.00, NULL, 'on-time', 'SFO', 'LAX'),
('JetBlue', '2', '206', 'SFO', '2025-07-01 13:25:25', '2025-07-01 16:50:25', 400.00, NULL, 'On Time', 'LAX', 'SFO'),
('JetBlue', '3', '106', 'SFO', '2025-01-09 13:25:25', '2025-01-09 16:50:25', 350.00, NULL, 'delayed', 'LAX', 'SFO'),
('JetBlue', '3', '104', 'PVG', '2025-03-07 13:25:25', '2025-03-07 16:50:25', 300.00, NULL, 'on-time', 'BEI', 'PVG'),
('JetBlue', '3', '102', 'SFO', '2025-02-12 13:25:25', '2025-02-12 16:50:25', 300.00, NULL, 'on-time', 'LAX', 'SFO');

-- --------------------------------------------------------

--
-- Table structure for table ticket
--

DROP TABLE IF EXISTS ticket CASCADE;
CREATE TABLE ticket (
  ticket_id VARCHAR(100) NOT NULL,
  airline_name VARCHAR(100) NOT NULL,
  flight_number VARCHAR(100) DEFAULT NULL,
  departure_date_time TIMESTAMP NOT NULL,
  sold_price DECIMAL(10,2) DEFAULT NULL,
  is_purchased BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (ticket_id),
  FOREIGN KEY (flight_number, departure_date_time) REFERENCES flight(flight_number, departure_date_time)
);

--
-- Dumping data for table ticket
--

INSERT INTO ticket (ticket_id, airline_name, flight_number, departure_date_time, sold_price, is_purchased) VALUES
('274', 'JetBlue', '206', '2025-07-01 13:25:25', 480.00, TRUE),
('273', 'JetBlue', '207', '2025-08-02 13:25:25', 300.00, TRUE),
('272', 'JetBlue', '207', '2025-08-02 13:25:25', NULL, FALSE),
('271', 'JetBlue', '296', '2025-05-30 13:25:25', NULL, FALSE),
('270', 'JetBlue', '296', '2025-05-30 13:25:25', NULL, FALSE),
('269', 'JetBlue', '715', '2025-02-28 10:25:25', NULL, FALSE),
('268', 'JetBlue', '715', '2025-02-28 10:25:25', NULL, FALSE),
('267', 'JetBlue', '715', '2025-02-28 10:25:25', NULL, FALSE),
('20', 'JetBlue', '296', '2025-05-30 13:25:25', 3000.00, TRUE),
('19', 'JetBlue', '296', '2025-05-30 13:25:25', 3000.00, TRUE),
('18', 'JetBlue', '207', '2025-08-02 13:25:25', 300.00, FALSE),
('17', 'JetBlue', '207', '2025-08-02 13:25:25', 300.00, TRUE),
('16', 'JetBlue', '206', '2025-07-01 13:25:25', 400.00, TRUE),
('15', 'JetBlue', '206', '2025-07-01 13:25:25', 400.00, TRUE),
('14', 'JetBlue', '206', '2025-07-01 13:25:25', 400.00, TRUE),
('12', 'JetBlue', '715', '2025-02-28 10:25:25', 500.00, TRUE),
('11', 'JetBlue', '134', '2024-12-12 13:25:25', 300.00, TRUE),
('9', 'JetBlue', '102', '2025-02-12 13:25:25', 300.00, TRUE),
('8', 'JetBlue', '839', '2024-05-26 13:25:25', 300.00, TRUE),
('7', 'JetBlue', '106', '2025-01-09 13:25:25', 350.00, TRUE),
('6', 'JetBlue', '106', '2025-01-09 13:25:25', 350.00, TRUE),
('5', 'JetBlue', '104', '2025-03-07 13:25:25', 300.00, TRUE),
('4', 'JetBlue', '104', '2025-03-07 13:25:25', 300.00, TRUE),
('3', 'JetBlue', '102', '2025-02-12 13:25:25', 300.00, TRUE),
('2', 'JetBlue', '102', '2025-02-12 13:25:25', 300.00, TRUE),
('1', 'JetBlue', '102', '2025-02-12 13:25:25', 300.00, TRUE);

-- --------------------------------------------------------

--
-- Table structure for table purchase
--

DROP TABLE IF EXISTS purchase CASCADE;
CREATE TABLE purchase (
  email VARCHAR(100) NOT NULL,
  ticket_id VARCHAR(100) NOT NULL,
  first_name VARCHAR(100) DEFAULT NULL,
  last_name VARCHAR(100) DEFAULT NULL,
  date_of_birth DATE DEFAULT NULL,
  card_type VARCHAR(100) DEFAULT NULL,
  card_number VARCHAR(100) DEFAULT NULL,
  name_on_card VARCHAR(100) DEFAULT NULL,
  expiration_date DATE DEFAULT NULL,
  purchase_date_time TIMESTAMP DEFAULT NULL,
  PRIMARY KEY (email, ticket_id),
  FOREIGN KEY (email) REFERENCES customers(email),
  FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)
);

--
-- Dumping data for table purchase
--

INSERT INTO purchase (email, ticket_id, first_name, last_name, date_of_birth, card_type, card_number, name_on_card, expiration_date, purchase_date_time) VALUES
('user3@nyu.edu', '14', 'User', '3', '1999-09-19', 'credit', '1111222233335555', 'User 3', '2024-03-20', '2025-04-20 11:55:55'),
('testcustomer@nyu.edu', '12', 'Test', 'Customer1', '1999-12-19', 'credit', '1111222233334444', 'Test Customer 1', '2024-03-19', '2024-10-19 11:55:55'),
('user3@nyu.edu', '11', 'User', '3', '1999-09-19', 'credit', '1111222233335555', 'User 3', '2027-03-23', '2024-10-23 11:55:55'),
('user3@nyu.edu', '9', 'User', '3', '1999-09-19', 'credit', '1111222233335555', 'User 3', '2024-03-11', '2024-12-11 11:55:55'),
('user3@nyu.edu', '8', 'User', '3', '1999-09-19', 'credit', '1111222233335555', 'User 3', '2024-03-08', '2024-05-08 11:55:55'),
('user3@nyu.edu', '7', 'User', '3', '1999-09-19', 'credit', '1111222233335555', 'User 3', '2027-03-07', '2024-12-07 11:55:55'),
('testcustomer@nyu.edu', '6', 'Test', 'Customer1', '1999-12-19', 'credit', '1111222233334444', 'Test Customer 1', '2027-03-07', '2025-01-07 11:55:55'),
('testcustomer@nyu.edu', '5', 'Test', 'Customer1', '1999-12-19', 'credit', '1111222233334444', 'Test Customer 1', '2027-03-28', '2025-02-28 11:55:55'),
('user1@nyu.edu', '4', 'User', '1', '1999-11-19', 'credit', '1111222233335555', 'User 1', '2024-03-21', '2025-01-21 11:55:55'),
('user2@nyu.edu', '3', 'User', '2', '1999-10-19', 'credit', '1111222233335555', 'User 2', '2027-03-08', '2025-02-08 11:55:55'),
('user1@nyu.edu', '2', 'User', '1', '1999-11-19', 'credit', '1111222233335555', 'User 1', '2027-03-09', '2025-01-09 11:55:55'),
('testcustomer@nyu.edu', '1', 'Test', 'Customer1', '1999-12-19', 'credit', '1111222233334444', 'Test Customer 1', '2027-03-01', '2025-01-10 11:55:55'),
('user1@nyu.edu', '15', 'User', '1', '1999-11-19', 'credit', '1111222233335555', 'User 1', '2024-03-21', '2025-04-21 11:55:55'),
('user2@nyu.edu', '16', 'User', '2', '1999-10-19', 'credit', '1111222233335555', 'User 2', '2024-03-19', '2024-02-19 11:55:55'),
('user1@nyu.edu', '17', 'User', '1', '1999-11-19', 'credit', '1111222233335555', 'User 1', '2024-03-11', '2025-01-11 11:55:55'),
('testcustomer@nyu.edu', '273', 'Anthony', 'Lamelas', '2025-06-06', 'credit', '2423442', 'ds', '2025-07-01', '2025-06-06 21:46:23'),
('user1@nyu.edu', '19', 'User', '1', '1999-11-19', 'credit', '1111222233334444', 'Test Customer 1', '2024-03-22', '2025-04-22 11:55:55'),
('testcustomer@nyu.edu', '20', 'Test', 'Customer1', '1999-12-19', 'credit', '1111222233334444', 'Test Customer 1', '2024-03-16', '2024-12-16 11:55:55'),
('testcustomer@nyu.edu', '274', 'Test', 'Customer', '2025-04-30', 'credit', '1234567890', 'TEst customer', '2025-12-01', '2025-05-06 19:29:30');

-- --------------------------------------------------------

--
-- Table structure for table review
--

DROP TABLE IF EXISTS review CASCADE;
CREATE TABLE review (
  email VARCHAR(100) NOT NULL,
  ticket_id VARCHAR(100) NOT NULL,
  comments VARCHAR(100) DEFAULT NULL,
  rating INTEGER DEFAULT NULL,
  PRIMARY KEY (email, ticket_id),
  FOREIGN KEY (email) REFERENCES customers(email),
  FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)
);

--
-- Dumping data for table review
--

INSERT INTO review (email, ticket_id, comments, rating) VALUES
('testcustomer@nyu.edu', '5', 'Customer Care services are not good', 1),
('user2@nyu.edu', '3', 'Satisfied and will use the same flight again', 3),
('user1@nyu.edu', '2', 'Relaxing, check-in and onboarding very professional', 5),
('testcustomer@nyu.edu', '1', 'Very Comfortable', 4),
('user1@nyu.edu', '4', 'Comfortable journey and Professional', 5),
('testcustomer@nyu.edu', '12', 'Good', 5),
('testcustomer@nyu.edu', '20', 'Great flight', 5);

-- --------------------------------------------------------

--
-- Table structure for table staff_email
--

DROP TABLE IF EXISTS staff_email CASCADE;
CREATE TABLE staff_email (
  username VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  PRIMARY KEY (username, email),
  FOREIGN KEY (username) REFERENCES airline_staff(username)
);

--
-- Dumping data for table staff_email
--

INSERT INTO staff_email (username, email) VALUES
('admin', 'staff@nyu.edu');

-- --------------------------------------------------------

--
-- Table structure for table staff_phone
--

DROP TABLE IF EXISTS staff_phone CASCADE;
CREATE TABLE staff_phone (
  username VARCHAR(100) NOT NULL,
  phone_number VARCHAR(100) NOT NULL,
  PRIMARY KEY (username, phone_number),
  FOREIGN KEY (username) REFERENCES airline_staff(username)
);

--
-- Dumping data for table staff_phone
--

INSERT INTO staff_phone (username, phone_number) VALUES
('admin', '11122223333'),
('admin', '44455556666');

COMMIT;
