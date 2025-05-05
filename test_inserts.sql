-- Add airline
INSERT INTO airline (airline_name)
VALUES ('JetBlue');

-- Add airline staff
INSERT INTO airline_staff (username, password, first_name, last_name, date_of_birth, airline_name)
VALUES ('admin', 'abcd', 'Roe', 'Jones', '1978-05-25', 'JetBlue');

-- Add staff emails
INSERT INTO staff_email (username, email)
VALUES ('admin', 'staff@nyu.edu');

-- Add staff phone numbers
INSERT INTO staff_phone (username, phone_number)
VALUES ('admin', '111-2222-3333'),
       ('admin', '444-5555-6666');

-- Add airplanes
INSERT INTO airplane (airplane_id, airline_name, number_of_seats, manufacturing_company)
VALUES (1, 'JetBlue', 4, 'Boeing'),
       (2, 'JetBlue', 4, 'Airbus'),
       (3, 'JetBlue', 50, 'Boeing');

-- Add airports
INSERT INTO airport (airport_code, airport_name, city, country)
VALUES 
('JFK', 'JFK', 'NYC', 'USA'),
('BOS', 'BOS', 'Boston', 'USA'),
('PVG', 'PVG', 'Shanghai', 'China'),
('BEI', 'BEI', 'Beijing', 'China'),
('SFO', 'SFO', 'San Francisco', 'USA'),
('LAX', 'LAX', 'Los Angeles', 'USA'),
('HKA', 'HKA', 'Hong Kong', 'China'),
('SHEN', 'SHEN', 'Shenzhen', 'China');

-- Add Customers
INSERT INTO customers (
    email, password, first_name, last_name,
    building_number, street, city, state,
    phone_number, passport_number, passport_expiration,
    passport_country, date_of_birth
) VALUES 
('testcustomer@nyu.edu', '1234', 'Test', 'Customer1', '1555', 'Jay St', 'Brooklyn', 'New York',
 '123-4321-4321', '54321', '2025-12-24', 'USA', '1999-12-19'),

('user1@nyu.edu', '1234', 'User', '1', '5405', 'Jay Street', 'Brooklyn', 'New York',
 '123-4322-4322', '54322', '2025-12-25', 'USA', '1999-11-19'),

('user2@nyu.edu', '1234', 'User', '2', '1702', 'Jay Street', 'Brooklyn', 'New York',
 '123-4323-4323', '54323', '2025-10-24', 'USA', '1999-10-19'),

('user3@nyu.edu', '1234', 'User', '3', '1890', 'Jay Street', 'Brooklyn', 'New York',
 '123-4324-4324', '54324', '2025-09-24', 'USA', '1999-09-19');

--Add flights
INSERT INTO flight (
    airline_name, flight_number, airport_code, departure_airport_code, departure_date_time,
    arrival_airport_code, arrival_date_time, base_price, flight_status, airplane_id
) VALUES 
('JetBlue', 102, 'SFO', 'SFO', '2025-02-12 13:25:25', 'LAX', '2025-02-12 16:50:25', 300, 'on-time', 3),
('JetBlue', 104, 'PVG', 'PVG', '2025-03-07 13:25:25', 'BEI', '2025-03-07 16:50:25', 300, 'on-time', 3),
('JetBlue', 106, 'SFO', 'SFO', '2025-01-09 13:25:25', 'LAX', '2025-01-09 16:50:25', 350, 'delayed', 3),
('JetBlue', 206, 'SFO', 'SFO', '2025-07-01 13:25:25', 'LAX', '2025-07-01 16:50:25', 400, 'on-time', 2),
('JetBlue', 207, 'LAX', 'LAX', '2025-08-02 13:25:25', 'SFO', '2025-08-02 16:50:25', 300, 'on-time', 2),
('JetBlue', 134, 'JFK', 'JFK', '2024-12-12 13:25:25', 'BOS', '2024-12-12 16:50:25', 300, 'delayed', 3),
('JetBlue', 296, 'PVG', 'PVG', '2025-05-30 13:25:25', 'SFO', '2025-05-30 16:50:25', 3000, 'on-time', 1),
('JetBlue', 715, 'PVG', 'PVG', '2025-02-28 10:25:25', 'BEI', '2025-02-28 13:50:25', 500, 'delayed', 1),
('JetBlue', 839, 'SHEN', 'SHEN', '2024-05-26 13:25:25', 'BEI', '2024-05-26 16:50:25', 300, 'on-time', 3);

--Add tickets
INSERT INTO ticket (ticket_id, airline_name, flight_number, departure_date_time, sold_price, is_purchased)
VALUES
(1,  'JetBlue', 102, '2025-02-12 13:25:25', NULL, FALSE),
(2,  'JetBlue', 102, '2025-02-12 13:25:25', NULL, FALSE),
(3,  'JetBlue', 102, '2025-02-12 13:25:25', NULL, FALSE),
(4,  'JetBlue', 104, '2025-03-07 13:25:25', NULL, FALSE),
(5,  'JetBlue', 104, '2025-03-07 13:25:25', NULL, FALSE),
(6,  'JetBlue', 106, '2025-01-09 13:25:25', NULL, FALSE),
(7,  'JetBlue', 106, '2025-01-09 13:25:25', NULL, FALSE),
(8,  'JetBlue', 839, '2024-05-26 13:25:25', NULL, FALSE),
(9,  'JetBlue', 102, '2025-02-12 13:25:25', NULL, FALSE),
(11, 'JetBlue', 134, '2024-12-12 13:25:25', NULL, FALSE),
(12, 'JetBlue', 715, '2025-02-28 10:25:25', NULL, FALSE),
(14, 'JetBlue', 206, '2025-07-01 13:25:25', NULL, FALSE),
(15, 'JetBlue', 206, '2025-07-01 13:25:25', NULL, FALSE),
(16, 'JetBlue', 206, '2025-07-01 13:25:25', NULL, FALSE),
(17, 'JetBlue', 207, '2025-08-02 13:25:25', NULL, FALSE),
(18, 'JetBlue', 207, '2025-08-02 13:25:25', NULL, FALSE),
(19, 'JetBlue', 296, '2025-05-30 13:25:25', NULL, FALSE),
(20, 'JetBlue', 296, '2025-05-30 13:25:25', NULL, FALSE);


--Add Purchase and Update Ticket 
INSERT INTO purchase (
    email, ticket_id, first_name, last_name, date_of_birth,
    card_type, card_number, name_on_card, expiration_date, purchase_date_time
) VALUES
('testcustomer@nyu.edu', 1, 'Test', 'Customer1', '1999-12-19', 'credit', '1111222233334444', 'Test Customer 1', '2027-03-01', '2025-01-10 11:55:55'),
('user1@nyu.edu', 2, 'User', '1', '1999-11-19', 'credit', '1111222233335555', 'User 1', '2027-03-09', '2025-01-09 11:55:55'),
('user2@nyu.edu', 3, 'User', '2', '1999-10-19', 'credit', '1111222233335555', 'User 2', '2027-03-08', '2025-02-08 11:55:55'),
('user1@nyu.edu', 4, 'User', '1', '1999-11-19', 'credit', '1111222233335555', 'User 1', '2024-03-21', '2025-01-21 11:55:55'),
('testcustomer@nyu.edu', 5, 'Test', 'Customer1', '1999-12-19', 'credit', '1111222233334444', 'Test Customer 1', '2027-03-28', '2025-02-28 11:55:55'),
('testcustomer@nyu.edu', 6, 'Test', 'Customer1', '1999-12-19', 'credit', '1111222233334444', 'Test Customer 1', '2027-03-07', '2025-01-07 11:55:55'),
('user3@nyu.edu', 7, 'User', '3', '1999-09-19', 'credit', '1111222233335555', 'User 3', '2027-03-07', '2024-12-07 11:55:55'),
('user3@nyu.edu', 8, 'User', '3', '1999-09-19', 'credit', '1111222233335555', 'User 3', '2024-03-08', '2024-05-08 11:55:55'),
('user3@nyu.edu', 9, 'User', '3', '1999-09-19', 'credit', '1111222233335555', 'User 3', '2024-03-11', '2024-12-11 11:55:55'),
('user3@nyu.edu', 11, 'User', '3', '1999-09-19', 'credit', '1111222233335555', 'User 3', '2027-03-23', '2024-10-23 11:55:55'),
('testcustomer@nyu.edu', 12, 'Test', 'Customer1', '1999-12-19', 'credit', '1111222233334444', 'Test Customer 1', '2024-03-19', '2024-10-19 11:55:55'),
('user3@nyu.edu', 14, 'User', '3', '1999-09-19', 'credit', '1111222233335555', 'User 3', '2024-03-20', '2025-04-20 11:55:55'),
('user1@nyu.edu', 15, 'User', '1', '1999-11-19', 'credit', '1111222233335555', 'User 1', '2024-03-21', '2025-04-21 11:55:55'),
('user2@nyu.edu', 16, 'User', '2', '1999-10-19', 'credit', '1111222233335555', 'User 2', '2024-03-19', '2024-02-19 11:55:55'),
('user1@nyu.edu', 17, 'User', '1', '1999-11-19', 'credit', '1111222233335555', 'User 1', '2024-03-11', '2025-01-11 11:55:55'),
('testcustomer@nyu.edu', 18, 'Test', 'Customer1', '1999-12-19', 'credit', '1111222233334444', 'Test Customer 1', '2024-03-25', '2025-02-25 11:55:55'),
('user1@nyu.edu', 19, 'User', '1', '1999-11-19', 'credit', '1111222233334444', 'Test Customer 1', '2024-03-22', '2025-04-22 11:55:55'),
('testcustomer@nyu.edu', 20, 'Test', 'Customer1', '1999-12-19', 'credit', '1111222233334444', 'Test Customer 1', '2024-03-16', '2024-12-16 11:55:55');


-- Update corresponding tickets
UPDATE ticket SET sold_price = 300, is_purchased = TRUE WHERE ticket_id IN (1, 2, 3, 4, 5, 9, 11, 17, 18);
UPDATE ticket SET sold_price = 350, is_purchased = TRUE WHERE ticket_id IN (6, 7);
UPDATE ticket SET sold_price = 400, is_purchased = TRUE WHERE ticket_id IN (14, 15, 16);
UPDATE ticket SET sold_price = 500, is_purchased = TRUE WHERE ticket_id = 12;
UPDATE ticket SET sold_price = 3000, is_purchased = TRUE WHERE ticket_id IN (19, 20);
UPDATE ticket SET sold_price = 300, is_purchased = TRUE WHERE ticket_id = 8;


-- Reviews
-- Flight 102 on 2025-02-12
INSERT INTO review (email, ticket_id, comments, rating)
VALUES 
('testcustomer@nyu.edu', 1, 'Very Comfortable', 4),
('user1@nyu.edu', 2, 'Relaxing, check-in and onboarding very professional', 5),
('user2@nyu.edu', 3, 'Satisfied and will use the same flight again', 3);

-- Flight 104 on 2025-03-07
INSERT INTO review (email, ticket_id, comments, rating)
VALUES 
('testcustomer@nyu.edu', 5, 'Customer Care services are not good', 1),
('user1@nyu.edu', 4, 'Comfortable journey and Professional', 5);
