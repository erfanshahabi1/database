# Library Management System

**University Database Project | Full-Stack Web Application & Relational Database Design**

## Overview
A university coursework project exploring library operations through relational database design and web interfaces. The repository includes a Microsoft SQL Server schema script, a Django-based backend, and a separate HTML/CSS/JavaScript frontend prototype. These components illustrate complementary approaches to managing books, members, borrowing records, and administrative tasks; they are **not presented as one fully integrated, production-ready application**.

**Early Development Files:** A few additional files are retained from the initial project phase, when SQLite was considered for the database implementation. The team later changed the database approach, so these files are included for historical reference and are not part of the final implementation.

## Technologies
- **Database:** Microsoft SQL Server (T-SQL); Django models configured for MySQL
- **Backend:** Python, Django 4.2, Django ORM, forms, and views
- **Frontend:** HTML, CSS, JavaScript, jQuery, and Firebase Authentication/Firestore

## Database Design
The SQL Server script defines tables for **books, members, authors, publishers, employees, librarians, managers, cleaners, membership status, and activity logs**. Primary and foreign keys model relationships between library records.

### Entity–Relationship Diagram (EERD)

The database was conceptually modeled using an Enhanced Entity–Relationship Diagram (EERD), illustrating key entities, attributes, relationships, and specialization hierarchies within the library management system.

![Library Management System EERD](eerd.png)

**SQL views:** `View book` (books with fewer than five available copies), `View member` (member information), `View_logbook` (book activity logs), and `View_logmember` (member activity logs).

**Database logic:** `CalculateDebt` functions calculate a date-based debt amount; `len` and `lend` stored procedures update book/member records during lending. The script also includes table constraints and database configuration statements.

## Application Components
- **Django backend (`BackEnd/`):** Models for books, authors, publishers, members, employees, membership, and borrowing; routes and forms for adding, lending, and returning books, calculating late-return fines, viewing borrowed books, and identifying low inventory.
- **Frontend (`FrontEnd/`):** Pages for administrator and user login, dashboards, book listings, and book-management interactions. JavaScript uses Firebase services for authentication and data access.

## Notes
This repository documents an **academic project**, not a deployed production service. The SQL Server script and the Django/MySQL/Firebase components use different data technologies and may require configuration or adaptation to run together. Remove or replace any embedded credentials and environment-specific settings before publishing or deploying.
