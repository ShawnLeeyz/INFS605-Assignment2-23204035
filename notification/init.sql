/* 
 * This SQL script initializes the notification database schema.
 * It creates the necessary tables and constraints for managing notifications.
 * For the notification service
 */

 /* id : id of the notification
  * student_id : The student of the id that gets the notification
  * message : The message in the notification
  * sent_at : time that the notification was sent
*/

CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    message TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
