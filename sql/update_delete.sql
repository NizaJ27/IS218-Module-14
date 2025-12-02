-- SQL: update_delete.sql
-- Update and delete examples as required.

-- Update a record (example changes result for id = 1)
UPDATE calculations
SET result = 6
WHERE id = 1;

-- Delete a record (example removes id = 2)
DELETE FROM calculations
WHERE id = 2;

-- End of update_delete.sql
