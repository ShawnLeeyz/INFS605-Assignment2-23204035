/* 
 * This SQL script initializes the feedback schema.
 * It creates the necessary tables and constraints for managing feedback.
 * For the course-feedback service
 */

/* id : id of the feedback entry 
 * course_id : ID of the course for which feedback is provided
 * student_id : ID of the student providing the feedback
 * comment : Additional comments about the course
 * category : Category of the feedback (e.g., "Content", "Instructor", "Overall")
 * created_at : Timestamp when the feedback was submitted
 */

CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    course_id INT NOT NULL,
    student_id INT NOT NULL,
    comment TEXT,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* 
 * Sample of feedback on the courses
 */
INSERT INTO feedback (course_id, student_id, comment, category) VALUES
(1, 1, 'Great course! Very informative.', 'Content'),
(1, 2, 'Good introduction to the field.', 'Instructor'),
(2, 1, 'Excellent coverage of data structures.', 'Content'),
(2, 3, 'Challenging but rewarding.', 'Overall'),
(3, 2, 'Helpful for understanding databases.', 'Content'),
(3, 4, 'Good practical examples.', 'Instructor'),
(4, 3, 'Well-structured and easy to follow.', 'Overall'),
(4, 5, 'Nice introduction to web development.', 'Content'),
(5, 4, 'Very useful for my career development.', 'Overall'),
(5, 5, 'Good overview of software engineering principles.', 'Instructor');