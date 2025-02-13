# Project Update - 12 Feb 25

## 1.&nbsp;&nbsp;&nbsp;Overview
### Introduction
Backlogger is a project management tool built on a robust API, offering users a flexible and scalable platform to manage projects efficiently. It supports self-registration, enabling individuals and teams to create accounts, join existing subscriptions, or establish new ones tailored to their project needs.
### Key Features
- Flexible Project Management Frameworks: Users can manage projects using Waterfall, Kanban, or Scrum, adapting to their preferred workflow.
- Hierarchical Structure: Supports a multi-layered approach with objects such as:
  - Objective/Initiative
  - Platform
  - Project/Application
  - Feature
  - Epic
  - User Story, Technical Enabler, Spike, Bug, Sub-task
- Subscription-Based Model: Users can opt for different subscription tiers based on their project complexity and team size.
- Scalability: Designed to accommodate both small teams and large enterprises with advanced project tracking needs.
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
├── authentication/
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
│   ├── authentication/
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
