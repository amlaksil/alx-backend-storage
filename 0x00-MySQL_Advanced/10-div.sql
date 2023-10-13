-- Function to safely divide two numbers

DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS DECIMAL(10, 2)
BEGIN
    DECLARE result DECIMAL(10, 2);

    IF b = 0 THEN
        SET result = 0;
    ELSE
        SET result = CAST(a AS DECIMAL(10, 2)) / CAST(b AS DECIMAL(10, 2));
    END IF;

    RETURN result;
END //

DELIMITER ;
