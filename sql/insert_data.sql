-- SQL: insert_data.sql
-- Inserts sample users and calculation rows as specified in the assignment.

-- Insert users
INSERT INTO users (username, email)
VALUES
('alice', 'alice@example.com'),
('bob', 'bob@example.com');

-- Insert calculations
INSERT INTO calculations (operation, operand_a, operand_b, result, user_id)
VALUES
('add', 2, 3, 5, 1),
('divide', 10, 2, 5, 1),
('multiply', 4, 5, 20, 2);

-- End of insert_data.sql
