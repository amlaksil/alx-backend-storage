-- Stored procedure to compute and store the average weighted score for a student

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE total_score DECIMAL(10, 2);
    DECLARE total_weight DECIMAL(10, 2);
    DECLARE avg_weighted_score DECIMAL(10, 2);

    -- Compute the total score and total weight
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
END //

DELIMITER ;
