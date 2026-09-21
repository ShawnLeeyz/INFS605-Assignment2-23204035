# Student Services Dashboard
## INFS605 Assignment 2 — Microservices Architecture

This is an assignment in INFS605 based on creating a lightweight microservice application for an imaginary company Osborne.AI, to create a student service dashboard. In the student service dashboard includes managing student profiles, course details, and student feedback on courses.
This project is build with (Flask, PostgreSQL, Docker Compose).

## Architecture Diagram
```
┌─────────────────────────┐                                                                             
│                         │                                                                             
│                         │                                                                             
│     Admin Frontend      │                                                                             
│      Port:3000          │                                                                             
│                         │                                                                             
└───────────┬─────────────┘                                                                             
            │                                                                                           
            │                                                                                           
            │                                                                                           
            │                                                                                           
┌───────────▼─────────────┐                           ┌───────────────────────────┐                     
│                         │                           │                           │                     
│                         │                           │          [Service]        │                     
│         [Service]       │                           │        Course Catalogue   │                     
│     Student Profile     ◄────┐             ┌───────►│         Port:5002         │                     
│       Port:5001         │    │             │        │                           │                     
│                         │    │             │        │                           │                     
└───────────┬─────────────┘    │             │        └──────────────┬────────────┘                     
            │                  │             │                       │                                  
            │                  │             │                       │                                  
            │                  │             │                       │                                  
            │                  │             │                       │                                  
   ┌────────▼─────────┐        │             │            ┌──────────▼────────┐                         
   │                  │        │             │            │                   │                         
   │                  │        │             │            │                   │                         
   │    student-db    │        │             │            │    course-db      │                         
   │                  │        │             │            │                   │                         
   └──────────────────┘        │             │            └───────── ─────────┘                         
                               │             │                                                          
                               │             │                                                          
                               │             │                                                          
                               │             │                                                          
                               │             │                                                          
                               │             │                                                          
                      ┌────────┼─────────────┼────────────┐                                             
                      │                                   │                                             
                      │           [Service]               │                                             
                      │           Feedback                │                                             
                      │           Port:5003               │                                             
                      │                                   │             Notifies                        
                      └───────────────────────────────────┘───────────────────────┐                     
                                       │                                          │                     
                                       │                                          │                     
                                       │                                          │                     
                                       │                                          │                     
                                       │                                          │                     
                                       │                                          │                     
                                       │                        ┌─────────────────▼────────────────────┐
                             ┌─────────▼──────────┐             │                                      │
                             │                    │             │             [Service]                │
                             │    feedback-db     │             │             Notification             │
                             │                    │             │             Port:5004                │
                             └────────────────────┘             │                                      │
                                                                │                                      │
                                                                └───────────────────┬──────────────────┘
                                                                                    │                   
                                                                                    │                   
                                                                                    │                   
                                                                                    │                   
                                                                         ┌──────────▼──────────┐        
                                                                         │                     │        
                                                                         │                     │        
                                                                         │     notificaton-db  │        
                                                                         │                     │        
                                                                         └─────────────────────┘        
```

## Services Explanation
| Service | Port | Database | Responsibility |
|---|---|---|---|
| Student Profile | 5001 | student-db | This file implements a small HTTP API that exposes CRUD operations for a "students" resource and an endpoint for recording attendance.  |
| Course Catalogue | 5002 | course-db | This service contains the CRUD operations for a "course", it involves updating, deleting, creating and viewing the  available courses. |
| Feedback | 5003 | feedback-db | Handles submitting and retrieving student feedback about courses. Has its own database (feedback-db). Calls student-profile and course-catalogue over HTTP to check a student_id/course_id exists before accepting feedback.|
| Notification | 5004 | notification-db | This module contains the main application logic for the notification service. It contains the logic to send a notification when a feedback is submitted, and also contains the logic to get all the notifications in the notificaiton db.|

## Setup Instructions
1. Install Docker Desktop
2. download the project on github
3. If vscode is not installed, and open vscode (or any IDE)
4. Open the project folder
5. Open powershell (on windows)
6. type the command 'cd.....' to get into the folder directory e.g cd C:\Users\yzsha\Desktop\INFS605-Assignment2-23204035
7. type: " docker compose up -d --build " after being in the directory to start the containers
8. type: " docker ps" in the powershell to check if the containers are running or check docker desktop dashboard
9. Visit each service in your browser to confirm it's running:
   - http://localhost:5001 (Student Profile)
   - http://localhost:5002 (Course Catalogue)
   - http://localhost:5003 (Feedback)
   - http://localhost:5004 (Notification)
   
   Each should have a health check to show the service is working.
10. Since this project does not have an frontend except the given student profile frontend, postman is used to test the endpoints. 
    Import `postman_collection.json` (included in this repo) into Postman (desktop app - do not use the web app as localhost could not be reached). This is to test all the endpoints across all service
11. Once your done type : " docker compose down " to shut down the container

## Endpoints

### Student Profile
| Method | Route | Description |
|---|---|---|
| GET | http://localhost:5001/students | returns a list of students |
| GET | http://localhost:5001/students/1 | returns one student|
| POST | http://localhost:5001/students | creates a new student |
| PUT | http://localhost:5001/students/1 | Updates an existing student |
| DELETE | http://localhost:5001/students/1 | Deletes a student |

#### Example:
**POST body:**
``` json 
{"name": "Testing1", "email": "test1@gmail.com"} 
```

**PUT body:**
``` json 
{"name": "Updated Name"} 
```

### Course Catalogue
| Method | Route | Description |
|---|---|---|
| GET | http://localhost:5002/courses | Returns a list of all courses |
| GET | http://localhost:5002/courses/1 | Returns one course |
| POST | http://localhost:5002/courses | Creates a new course |
| PUT | http://localhost:5002/courses/1 | Updates an existing course |
| DELETE | http://localhost:5002/courses/1 | Deletes a course |

#### Example:
**POST body:**
```json
{"course_code": "CS999", "course_name": "Test Course", "description": "A test course.", "credits": 3}
```

**PUT body:**
```json
{"credits": 5}
```

**POST body - invalid credits (expected 400):**
```json
{"course_code": "CS122", "course_name": "Test Course", "description": "A test course.", "credits": -10}
```

### Feedback
| Method | Route | Description |
|---|---|---|
| GET | http://localhost:5003/feedback | Returns a list of all feedback entries |
| POST | http://localhost:5003/feedback | Submits new feedback |

#### Example:
**POST body:**
```json
{"student_id": 1, "course_id": 1, "category": "Content", "comment": "Really enjoyed this course"}
```

**POST body - invalid student (expect 404):**
```json
{"student_id": 99, "course_id": 1, "category": "Content", "comment": "Really enjoyed this course"}
```

**POST body - invalid course (expect 404):**
```json
{"student_id": 1, "course_id": 99, "category": "Content", "comment": "Really enjoyed this course"}
```

### Notification
| Method | Route | Description |
|---|---|---|
| GET | http://localhost:5004/notification | Returns a list of all logged notifications |
| POST | http://localhost:5004/notification | Logs a new notification. Called automatically by Feedback Service after a successful feedback submission |

#### Example:
**POST body:**
```json
{"student_id": 1, "message": "Standalone test notification"}
```

## Screenshots

See the `/screenshots` folder for evidence of the system running, including:
- All 9 containers running (`docker ps`)
- Example Postman requests and response (status and JSON bodies), on all 4 services and also include validation checking.