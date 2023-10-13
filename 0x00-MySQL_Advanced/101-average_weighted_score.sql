-- Stored procedure to compute and store the average weighted score for all students

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE total_score DECIMAL(10, 2);
    DECLARE total_weight DECIMAL(10, 2);
    DECLARE avg_weighted_score DECIMAL(10, 2);

    -- Declare cursor to iterate over user IDs
    DECLARE user_cursor CURSOR FOR
        SELECT id FROM users;

    -- Open cursor
    OPEN user_cursor;

    -- Fetch first user ID
    FETCH NEXT FROM user_cursor INTO user_id;

    -- Loop through each user ID
    WHILE user_id IS NOT NULL DO
        -- Compute the total score and total weight for the user
        SELECT SUM(score * weight), SUM(weight)
        INTO total_score, total_weight
        FROM scores
        WHERE user_id = user_id;

        -- Compute the average weighted score
        IF total_weight > 0 THEN
            SET avg_weighted_score = total_score / total_weight;
        ELSE
            SET avg_weighted_score = 0;
        END IF;

        -- Update the average weighted score for the user
        UPDATE users
        SET average_weighted_score = avg_weighted_score
        WHERE id = user_id;

        -- Fetch next user ID
        FETCH NEXT FROM user_cursor INTO user_id;
    END WHILE;

    -- Close cursor
    CLOSE user_cursor;
END //

DELIMITER ;
