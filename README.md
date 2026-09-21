# Student Services Dashboard
### INFS605 Assignment 2 — Microservices Architecture

This is an assignment in INFS605 based on creating a lightweight microservice application for an imaginary company Osborne.AI, to create a student service dashboard. In the student service dasboard includes managing student profiles, course details, and student feedback on courses.
This project is build with (Flask, PostgreSQL, Docker Compose).

### Architecture Diagram
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

