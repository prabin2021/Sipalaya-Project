# Sipalaya Info Tech - Educational Platform Documentation

## 1. Introduction

Sipalaya Info Tech's Educational Platform is a comprehensive web application designed to facilitate online learning and training management. The platform serves as a bridge between students seeking IT education and experienced instructors, offering a wide range of courses, interactive learning materials, and administrative tools.

### Purpose
- Provide accessible IT education
- Streamline course management
- Enable efficient student-instructor interaction
- Track student progress and performance
- Facilitate online payments and enrollments

## 2. Project Overview

The platform is built as a Django-based web application with multiple interconnected apps, each serving specific functionalities:

### Core Apps
1. **Users App**
   - Custom user authentication
   - Role-based access control
   - Profile management

2. **Courses App**
   - Course management
   - Module and lesson organization
   - Assignment handling
   - Progress tracking

3. **Instructor App**
   - Course creation and management
   - Student progress monitoring
   - Assignment grading
   - Resource management

4. **Student App**
   - Course enrollment
   - Progress tracking
   - Assignment submission
   - Learning resource access

5. **Blog App**
   - Content management
   - SEO optimization
   - Category and tag organization

6. **Careers App**
   - Job placement services
   - Company partnerships
   - Alumni success stories

7. **Feedback App**
   - Testimonials
   - Course reviews
   - Rating system

## 3. Technology Stack

### Frontend
- HTML5
- CSS3 (Tailwind CSS)
- JavaScript
- Alpine.js
- Chart.js (for analytics)

### Backend
- Python 3.x
- Django 5.0.2
- Django REST Framework

### Database
- SQLite (Development)
- MySQL/PostgreSQL (Production)

### Payment Integration
- eSewa
- Khalti

### Version Control
- Git

## 4. System Architecture

The application follows a Model-View-Template (MVT) architecture pattern:

### Models
- Represent database structure
- Handle data relationships
- Implement business logic

### Views
- Process user requests
- Handle business logic
- Return appropriate responses

### Templates
- Define UI structure
- Handle data presentation
- Implement responsive design

## 5. Application Structure

### Core App
```python
core/
├── models.py
│   ├── Banner
│   ├── Testimonial
│   ├── Statistic
│   ├── Service
│   ├── CompanyInfo
│   ├── Milestone
│   └── Partnership
├── views.py
└── admin.py
```

### Courses App
```python
courses/
├── models.py
│   ├── Category
│   ├── Course
│   ├── Module
│   ├── Lesson
│   ├── Assignment
│   ├── Submission
│   ├── DemoClass
│   ├── Enrollment
│   └── LessonProgress
├── views.py
└── admin.py
```

### Users App
```python
users/
├── models.py
│   └── CustomUser
├── views.py
└── admin.py
```

## 6. Database Schema

### Core Tables
- **Users**
  - id (PK)
  - email
  - password
  - first_name
  - last_name
  - role
  - is_active

- **Courses**
  - id (PK)
  - title
  - slug
  - description
  - instructor (FK to Users)
  - price
  - duration
  - level
  - created_at

- **Enrollments**
  - id (PK)
  - student (FK to Users)
  - course (FK to Courses)
  - enrolled_at
  - payment_status
  - progress

### Relationships
- One-to-Many:
  - User -> Courses (Instructor)
  - Course -> Modules
  - Module -> Lessons
  - Course -> Enrollments

- Many-to-Many:
  - Users <-> Courses (through Enrollments)
  - Lessons <-> Students (through LessonProgress)

## 7. Features and Functionality

### User Management
- Registration and authentication
- Role-based access control
- Profile management
- Password reset functionality

### Course Management
- Course creation and editing
- Module and lesson organization
- Resource upload and management
- Progress tracking
- Assignment submission and grading

### Payment System
- Integration with eSewa and Khalti
- Payment tracking
- Invoice generation
- Installment management

### Content Management
- Blog post creation and management
- SEO optimization
- Media handling
- Category and tag organization

### Analytics and Reporting
- Student progress tracking
- Course performance metrics
- Financial reports
- Enrollment statistics

## 8. API Documentation

### Authentication Endpoints
```
POST /api/auth/login/
POST /api/auth/register/
POST /api/auth/password/reset/
```

### Course Endpoints
```
GET /api/courses/
GET /api/courses/<id>/
POST /api/courses/
PUT /api/courses/<id>/
DELETE /api/courses/<id>/
```

### Enrollment Endpoints
```
POST /api/enrollments/
GET /api/enrollments/student/<id>/
GET /api/enrollments/course/<id>/
```

## 9. Installation and Setup

### Prerequisites
- Python 3.x
- pip
- virtualenv

### Installation Steps
1. Clone the repository
   ```bash
   git clone <repository-url>
   ```

2. Create and activate virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. Run migrations
   ```bash
   python manage.py migrate
   ```

6. Create superuser
   ```bash
   python manage.py createsuperuser
   ```

7. Run development server
   ```bash
   python manage.py runserver
   ```


## 10. Security Measures

### Authentication
- Custom user model
- JWT token authentication
- Password hashing
- Session management

### Data Protection
- CSRF protection
- XSS prevention
- SQL injection prevention
- File upload validation

### Payment Security
- Secure payment gateway integration
- Payment data encryption
- Transaction logging

## 11. Conclusion

The Sipalaya Info Tech Educational Platform is a robust and scalable solution for online education management. The system successfully implements all required features while maintaining security, performance, and user experience.

### Future Enhancements
1. Mobile application development
2. Live classroom features
3. AI-powered learning recommendations
4. Advanced analytics dashboard
5. Integration with more payment gateways

### Contact Information
For technical support or inquiries:
- Email: infotech@sipalaya.com
- Phone: 9851344071 | 9806393939
- Address: Narephat 32- Koteshwor, Kathmandu 