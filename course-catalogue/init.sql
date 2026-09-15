/* 
 * This SQL script initializes the course catalogue database schema.
 * It creates the necessary tables and constraints for managing courses. 
 * For the course-catalogue service
 */

 /* id : id of the course
  * course_code : Unique code for the course (e.g., CS101)
  * course_name : Name of the course
  * description : Description of the course content
  * credits : Number of credits for the course
*/

CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    course_code VARCHAR(10) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    description TEXT,
    credits INT NOT NULL CHECK (credits > 0)
);


/* 
 * Sample of courses for the catalog
 */
INSERT INTO courses (course_code, course_name, description, credits) VALUES
('CS101', 'Introduction to Computer Science', 'An introductory course on computer science concepts.', 3),
('CS102', 'Data Structures and Algorithms', 'A course on fundamental data structures and algorithms.', 4),
('CS103', 'Database Systems', 'A course on relational database systems and SQL.', 3),
('CS104', 'Web Development', 'A course on building web applications using modern frameworks.', 3),
('CS105', 'Software Engineering', 'A course on software development methodologies and best practices.', 3);