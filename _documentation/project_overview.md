# Project Update - 12 Feb 25

## 1.&nbsp;&nbsp;&nbsp;Overview
### Introduction
Backlogger is a project management tool built on a robust API, offering users a flexible and scalable platform to manage projects efficiently. It supports self-registration, enabling individuals and teams to create accounts, join existing subscriptions, or establish new ones tailored to their project needs.
### Organisation/Subscription
The **Organisation/Subscription** is the top-level entity that all other objects are linked to. Once a user is authenticated, they create their **organisation**, which comes with a **default hierarchical structure**. This structure is flexible—users can choose a **simple Kanban setup** for task management or enable a **more advanced framework like Scrum or Waterfall** as needed.  

### Subscription Tiers  
Each subscription tier determines the available features and project structure:  

1. **Basic** (Free) – Shared database with limited functionality. Defaults to a **simple task-based system** (e.g., a Kanban board with tasks).  
2. **Standard** (Paid) – Shared database with **limited users** and **self-administered data checkpointing**. Users can enable additional project management features.  
3. **Premier** (Paid) – Exclusive database, allowing full control over **custom hierarchies** and expanded project structures.  
4. **Enterprise** (Paid) – Includes **all three project management frameworks** (**Waterfall, Kanban, and Scrum**) with **unlimited domain-based users** and full access to advanced hierarchical layers like **Objectives, Initiatives, Platforms, and Applications** for enterprise-scale management.  

---

### Key Features  

#### Customizable Hierarchical Structure  
Upon setup, an organisation includes default objects that can be expanded based on the user’s needs:  
- **Basic Setup** – **Task-based workflow** for Kanban users.  
- **Advanced Setup** – Objects like **App, Feature, Epic, User Story, and Technical Enabler** can be enabled for structured Scrum workflows.  
- **Enterprise-Level Setup** – Additional layers like **Objective, Initiative, Platform, and Application**, supporting both **Agile (Kanban & Scrum)** and **Waterfall** methodologies.  

#### Flexible Project Management Frameworks  
Supports:  
- **Waterfall** – Linear project progression for structured planning.  
- **Kanban (Agile)** – Continuous flow task management.  
- **Scrum (Agile)** – Iteration-based development with Epics, Features, and User Stories.  

#### Scalability  
Designed for **individuals, small teams, and large enterprises**, ensuring projects can start simple and expand as needed.  

#### Subscription-Based Model  
Users can **start with basic functionality** and progressively unlock more advanced features **as their needs grow**.  

### Target Audience
- Software Development Teams: Teams following agile or traditional project management methodologies.
- Startups & Enterprises: Organizations seeking a structured yet flexible project management tool.
- Freelancers & Consultants: Independent professionals managing multiple client projects.
### Competitive Advantage
- API-Centric Architecture: Enables seamless integration with third-party tools and custom extensions.
- Self-Service Model: Users can register and start managing projects without requiring administrative intervention.
- Customizable Workflow: Offers a choice of project management frameworks to suit diverse needs.
## 2.&nbsp;&nbsp;&nbsp;Development Environment

### API Development
| Package             | Version |
| ------------------- | ------- |
| asgiref             | 3.8.1 |
| distlib             | 0.3.9 |
| Django              | 5.1.6 |
| django-ratelimit    | 4.1.0 |
| djangorestframework | 3.15.2 |
| filelock            | 3.17.0 |
| iniconfig           | 2.0.0 |
| packaging           | 24.2 |
| pip                 | 25.0 |
| platformdirs        | 4.3.6 |
| pluggy              | 1.5.0 |
| psycopg2-binary     | 2.9.10 |
| pytest              | 8.3.4 |
| pytest-django       | 4.9.0 |
| sqlparse            | 0.5.3 |
| virtualenv          | 20.29.1 | 

## Project Structure
### API
```
backlogger_api/
├── _documentation/
│   ├── project_overview.md
│   ├── todo.md
│   ├── tree_source.txt
│   └── tree.txt
├── authentications/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── managers.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   ├── validators.py
│   └── views.py
├── backlogger_api/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tests/
│   ├── authentications/
│   │   ├── __init__.py
│   │   ├── test_serializers.py
│   │   ├── test_validators.py
│   │   ├── test_views.py
│   │   └── tests.py
│   └── __init__.py
├── conftest.py
├── .env
├── .gitignore
├── manage.py 
└── pytest.ini
```
