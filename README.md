# Capstone-Project
# SkillHub – Skills & Projects Tracker

## Table of Contents
1. [Project Description](#project-description)
2. [Tech Stack](#tech-stack)
3. [User Stories](#user-stories)
4. [Entity Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
5. [Installation Guide](#installation-guide)
6. [Future Features / Stretch Goals](#future-features--stretch-goals)

---

## Project Description
**Overview:**  
SkillHub is a Django web application that allows users to track personal growth through **skills and projects**. Each skill or project can have multiple tasks, and users can add **reflections/notes** to track their learning experience. The app is designed to be visually appealing, interactive, and user-friendly, motivating users to stay organized and achieve their goals.  

**Key Features:**  
- User authentication (login, logout, registration)  
- CRUD operations for Skills, Projects, and Tasks  
- Add reflections/notes for each Skill/Project  
- Track task completion with dynamic progress bars  
- Clean, responsive, and interactive frontend  

---

## Tech Stack
- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, Django Template Language (DTL)  
- **Database:** SQLite  
- **Version Control:** Git & GitHub  

---

## User Stories

### Authentication
1. As a user, I want to register an account, so I can save my skills and projects privately.  
2. As a user, I want to log in and log out, so my data remains secure.  

### Skills
3. As a user, I want to add new skills, so I can track my learning goals.  
4. As a user, I want to update skill details, so I can adjust descriptions or categories.  
5. As a user, I want to delete skills, so I can remove outdated goals.  
6. As a user, I want to view all my skills with progress indicators, so I can track my achievements at a glance.  

### Projects
7. As a user, I want to add projects, so I can track personal or work-related projects.  
8. As a user, I want to update project details, so I can manage them effectively.  
9. As a user, I want to delete projects, so I can remove completed or canceled ones.  
10. As a user, I want to view all my projects with progress bars, so I can easily see progress.  

### Tasks
11. As a user, I want to add tasks to a skill/project, so I can break goals into actionable steps.  
12. As a user, I want to mark tasks as completed, so I can track progress.  
13. As a user, I want to edit or delete tasks, so I can update or remove them.  
14. As a user, I want progress bars to automatically update based on task completion, so I can monitor overall progress.  

### Reflections
15. As a user, I want to add reflections for each skill/project, so I can track my learning experience.  
16. As a user, I want to view all reflections for a skill/project, so I can reflect on my growth over time.  
17. As a user, I want to edit or delete reflections, so I can maintain accurate notes.  

### Stretch / Future Features
18. As a user, I want to visualize my progress across all skills/projects with charts.  
19. As a user, I want to filter skills/projects by category or priority.  
20. As a user, I want to upload files or images related to skills/projects.  

---
## ERD

![SkillHub ERD](assets/erd.png)