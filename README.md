# minItaly Booking System

![minItaly Booking System](image)

Welcome to Minitaly, a stylish and intuitive restaurant booking platform built with Django. Designed to offer a smooth experience for both customers and staff, it allows users to book, manage, and cancel reservations while providing staff with administrative tools and a real-time dashboard.

Visit the deployed site: [minItaly](https://minitaly-booking-system-de8b5948572a.herokuapp.com/)


## CONTENTS

* [Introduction](#introduction)
* [Strategy Plane](#strategy-plane)
    * [Project Goals](#project-goals)
* [Scope Plane](#Scope-plans)
    * [Feature Planning](#feature-planning)
* [Future Scope](#future-scope)
* [Structure Plane](#structure-plane)
    * [User Stories](#user-stories)
    * [Database Schema](#database-chema)
* [Skeleton Plane](#skeleton-plane)
    * [Wireframes](#wireframes)
* [Surface Plane](#surface-plane)
    * [Colour Scheme](#colour-scheme)
    * [Typography](#typography)
    * [Imagery](#imagery)
* [Features](#features)
* [Accessibility](#accessibility)
* [Technologies Used](#technologies-used)
    * [Languages Used](#languages-used)
    * [Frameworks, Libraries & Programs Used](#frameworks-libraries--programs-used)
* [Deployment & Local Development](#deployment--local-development)
  * [Deployment](#deployment)
  * [Local Development](#local-development)
  * [How to Fork](#how-to-fork)
  * [How to Clone](#how-to-clone)
* [Testing](#testing)
  * [Solved Bugs](#solved-bugs)
  * [Known Bugs](#known-bugs)
* [Credits](#credits)
  * [Code Used](#code-used)
  * [Content](#content)
  * [Acknowledgments](#acknowledgments)

- - -

## Introduction


## Strategy Plane

The aim of Minitaly is to deliver a polished and responsive restaurant booking system that caters to the needs of four distinct user groups: non-member guests, registered customers, staff members, and admin/superusers.

### Project Goals

* Non-Member Guests
    * Access a responsive, visually appealing landing page that reflects the brand identity.
    * View the restaurant's digital menu to explore offerings before booking.
    * Register for an account in order to make and manage reservations.

* Registered Customers
    * Book a table online based on date, time, and number of guests.
    * Receive confirmation and reminder emails for reservations.
    * View and manage upcoming and past bookings through a personalized dashboard.
    * Edit or cancel reservations with ease.
    * Opt-in for email reminders about upcoming reservations.

* Staff Members
    * Access a dedicated staff dashboard with all upcoming bookings.
    * Filter bookings by date, time, or customer name.
    * Edit or cancel any customer booking.
    * Create new bookings on behalf of any registered customer.
    * Oversee booking logic, time slot availability, and table capacity.

* Admins/Superusers
    * Have full control over all models via the Django admin panel.
    * Access all customer and booking data.
    * Manage menu items and categories.
    * Bypass booking rules if needed (for testing, debugging, or data correction purposes).

* Business Objectives
    * Streamline the booking process to reduce phone calls and human error.
    * Empower both staff and customers with self-service features.
    * Enhance customer satisfaction with timely communication and a seamless UX.
    * Showcase the restaurant brand through design, accessibility, and responsiveness.


## Scope Plane

### Feature Planning

* Core Features

    * For Non-Member Guests
        * View the landing page with restaurant branding.
        * Browse the structured digital menu by category.
        * Access sign-up and login links to create an account.
    
    * For Registered Customers
        * Book a table
        * View upcoming and past reservations, edit, and cancel bookings via a user-friendly dashboard.
        * Automatically receive booking confirmation and cancellation emails.
        * Receive reminder emails 24 hours before a reservation (if opted in).
        * Form validations to prevent bookings in the past or overlapping time slots.
    
    * For Staff Members
        * Access a secure staff dashboard restricted to staff users.
        * View all upcoming reservations with filters by date, time, and customer.
        * Create new bookings, and edit and cancel any bookings on behalf of customers.
    
    * For Admins/Superusers
        * Access Django admin panel to manage users, bookings, menu items, and categories.
        * Ability to override validations via the admin interface (if needed for manual corrections).

## Future Scope
Several features were considered during the planning phase but were excluded due to project scope and time constraints. These may be included in future iterations:

* Intelligent Table Assignment
    * Automatically assign tables based on party size and availability.
    * Allow table sharing for small parties at larger tables.
    * Prioritize optimal space usage (e.g., placing 4 guests at a 4-person table when possible).
* Table Occupancy Tracking
    * Allow staff to manually mark tables as "occupied."
    * Prevent bookings for tables currently marked as occupied. The system already prevents double bookings per time slot, but future enhancements may allow marking individual tables as "occupied" for real-time floor management.
    * Automatically update a table’s status when a booking begins.
* Additional Ideas
    * Integrate Google Calendar or other APIs for reservation syncing.
    * Add online payment and deposit functionality for reservations.
    * Allow customers to mark favorite menu items or leave feedback.
    * QR code scanning for menu at table.
    

## Structure Plane
The project follows an Agile methodology with clearly defined user stories tailored to different user roles. Each user story includes a goal and acceptance criteria to guide implementation.
To ensure a focused and deliverable MVP, user stories were prioritized using the MoSCoW method:
* Must Have – Core functionality that is critical for the app to function (e.g., booking, editing, user authentication).
* Should Have – Important features that enhance usability but are not vital for launch (e.g., reminder emails, booking history).
* Could Have – Nice-to-have features that add polish or optional convenience (e.g., styled modals, visual enhancements).
* Won’t Have (for now) – Future features out of scope due to time constraints (e.g., smart table assignment). 

### User Stories

1. As a Guest I want to view the restaurant’s landing page, so I can learn about the brand and its offerings. (Must)

2. As a guest, I want to register an account, so that I can make and manage bookings online. (Must)
    * Acceptance criteria 1: A user can sign up with an email and password. (Must)
    * Acceptance criteria 2: The system prevents duplicate accounts using the same email. (Must)
    * Acceptance criteria 3: After successful registration, the user is redirected to the login page. (Must)

3. As a registered customer or admin, I want to log in securely, so that I can access my profile and manage bookings. (Must)
    * Acceptance criteria 1: Users must enter a valid email and password. (Must)
    * Acceptance criteria 2: Passwords are securely stored and validated. (Must)
    * Acceptance criteria 3: Users are redirected to the dashboard upon successful login. (Must)
    * Acceptance criteria 4: Incorrect login attempts show an error message. (Must)

4. As a registered customer, I want to book a table, so that I can secure a spot at the restaurant. (Must)
    * Acceptance criteria 1: The booking form allows users to select a date, time, and number of guests. (Must)
    * Acceptance criteria 2: The system prevents double bookings for the same table. (Must)
    * Acceptance criteria 3: Users receive a confirmation email upon successful booking. (Must)
    * Acceptance criteria 4: The system does not allow past dates for reservations. (Must)

5. As a guest or customer, I want to see available booking slots, so that I can plan when to visit. (Must)
    * Acceptance criteria 1: The system displays available time slots for a selected date. (Must)
    * Acceptance criteria 2: Fully booked time slots are marked as unavailable. (Must)
    * Acceptance criteria 3: Users cannot book beyond the restaurant’s operating hours. (Must)

6. As a system, I want to prevent double bookings, so that each table is assigned only once per time slot. (Must)
    * Acceptance criteria 1: The system checks table availability before confirming a booking. (Must)
    * Acceptance criteria 2: A booking is only confirmed if a table is available. (Must)
    * Acceptance criteria 3: Users cannot book the same table at the same time. (Must)

7. As a registered customer or admin, I want to cancel a booking, so that the table becomes available for others. (Must)
    * Acceptance criteria 1: Users can cancel a booking from their dashboard. (Must)
    * Acceptance criteria 2: Admins can cancel any booking and provide a reason. (Must)
    * Acceptance criteria 3: Users receive an email confirming the cancellation. (Must)

8. As a registered customer, I want to update my booking (change time, number of guests), so that I can modify my reservation as needed. (Must)
    * Acceptance criteria 1: Users can change their booking details (date, time, number of guests). (Must)
    * Acceptance criteria 2: The system checks table availability before confirming changes. (Must)
    * Acceptance criteria 3: Users receive an email with the updated booking details. (Must)

9. As a restaurant admin, I want to view all upcoming bookings, so that I can prepare for reservations. (Must)
    * Acceptance criteria 1: Admins can see all upcoming bookings in a list format. (Must)
    * Acceptance criteria 2: Bookings can be filtered by date, time, and customer name. (Must)
    * Acceptance criteria 3: Admins can cancel or modify bookings from the dashboard. (Must)

10. As a registered customer, I want to see my booking history, so that I can keep track of past visits. (Should)
    * Acceptance criteria 1: Users can view a list of all past bookings. (Should)
    * Acceptance criteria 2: The history includes date, time, and number of guests. (Should)
    * Acceptance criteria 3: Users can see cancellations with reasons. (Should)

11. As a guest, I want to view the restaurant's menu, so that I can decide what to order. (Must)
    * Acceptance criteria 1: The menu is displayed in a structured format (categories, prices, descriptions). (Must)
    * Acceptance criteria 3: The menu is responsive and accessible on all devices. (Must)

12. As a registered customer, I want to receive a reminder email before my reservation, so that I don’t forget my booking. (Could)
    * Acceptance criteria 1: The system sends an email reminder 24 hours before the booking. (Could)
    * Acceptance criteria 2: The email contains booking details (date, time, table number). (Could)
    * Acceptance criteria 3: Users can opt out of reminders in their settings. (Could)

13. As a restaurant admin, I want to create a booking on behalf of a customer, so that I can assist with offline or phone reservations. (Should)
    * Acceptance criteria 1: Admins can choose an existing registered customer from a dropdown list when creating a booking. (Should)
    * Acceptance criteria 2: The rest of the booking form (date, time, number of guests, special requests) behaves the same as the customer form with validations for availability. (Should)
    * Acceptance criteria 3: Upon submission, the booking is saved under the selected customer's account. (Should)
    * Acceptance criteria 4: A booking confirmation email is sent to the selected customer. (Should)
    * Acceptance criteria 5: Admins are redirected to the staff dashboard with a success message confirming the booking. (Should)

14. As a system, I want to assign tables automatically, so that the space is utilized efficiently. (Won’t)
    * Acceptance criteria 1: he system assigns tables based on party size. (Won’t)
    * Acceptance criteria 2: Multiple small parties can share a larger table if needed. (Won’t)
    * Acceptance criteria 3: The system prioritizes optimal table use (e.g., seating 4 people at a 4-person table instead of a 6-person table). (Won’t)

15. As a restaurant admin, I want to mark a table as occupied, so that the system knows which tables are in use. (Won’t)
    * Acceptance criteria 1: Admins can manually mark tables as occupied. (Won’t)
    * Acceptance criteria 2: Tables marked as occupied do not appear as available in the system. (Won’t)
    * Acceptance criteria 3: The system automatically marks a table as occupied when a booking starts. (Won’t)

### Database Schema

The data schema for the Minitaly booking system has been designed to support the key features of the application, including user authentication, reservation logic, staff controls, and menu display. It uses relational database models with appropriate foreign key and many-to-many relationships to maintain data integrity and allow efficient queries.

Below are the Entity Relationship Diagrams (ERDs) represented in table format, outlining the structure and relationships between all models used in the project:

* Table
    | Field | Type | Attributes |
    | --- | --- | --- |
    | id | AutoField | Primary Key |
    | number | PositiveIntegerField | Unique |
    | capacity | PositiveIntegerField |  |

* Booking
    | Field | Type | Attributes |
    | --- | --- | --- |
    | id | AutoField | Primary Key |
    | user | ForeignKey to User | on_delete=CASCADE, related_name='bookings' |
    | tables | ManyToManyField to Table |  |
    | date | DateField |  |
    | time | TimeField |  |
    | num_guests | PositiveIntegerField |  |
    | special_request | TextField | blank=True, null=True |
    | is_cancelled | BooleanField | default=False |
    | cancellation_reason | TextField | blank=True, null=True |
    | send_reminder | BooleanField | default=True |

* Category (Menu)
    | Field | Type | Attributes |
    | --- | --- | --- |
    | id | AutoField | Primary Key |
    | name | CharField(100) |  |

* MenuItem
    | Field | Type | Attributes |
    | --- | --- | --- |
    | id | AutoField | Primary Key |
    | category | ForeignKey to Category | on_delete=CASCADE, related_name='menu_items' |
    | name | CharField(100) |  |
    | description | TextField | blank=True |
    | price | DecimalField | max_digits=6, decimal_places=2 |

* User: The User model is predefined by Django as part of django.contrib.auth.models.User
    | Field | Type | Attributes |
    | --- | --- | --- |
    | id |	AutoField |	Primary key |
    | username | CharField | Unique username |
    | email | EmailField | Email address |
    | password | CharField | Hashed password |
    | first_name | CharField | Optional first name |
    | last_name | CharField | Optional last name |
    | is_staff | BooleanField | True if the user can access admin site |
    | is_superuser | BooleanField | True if the user has all permissions |
    | is_active | BooleanField | Active user flag |
    | last_login | DateTimeField | Last login timestamp |
    | date_joined |	DateTimeField |	Account creation timestamp |

A User (from Django's built-in model) can have many Booking entries; One-to-many relationship.
A Booking can be associated with one or more Table objects, and a Table can belong to many Booking entries; many-to-many relationship.
A Category can have many MenuItem entries, and a MenuItem belongs to one Category; one-to-many relationship.


## Skeleton Plane



### Wireframes



## Surface Plane

The Surface Plane focuses on the visual and sensory design of the website — what users see, feel, and interact with. It includes the choice of colors, typography, layout, and imagery, all working together to reflect the brand identity of Minitaly and create a seamless and pleasant user experience.

The following sections outline the Color Scheme, Typography, and Imagery used throughout the project, ensuring consistency, accessibility, and aesthetic appeal across all devices and screen sizes.

### Colour Scheme

Minitaly uses a color palette inspired by the Italian flag and cuisine culture to reflect the brand identity and warmth of an Italian dining experience. The scheme includes vibrant greens and reds paired with clean whites and elegant grays for accessibility and clarity.

![minItaly, Colour Scheme](readme-assets\images\color-scheme.png)

| Color Role | Hex Code | Usage |
| --- | --- | --- |
| Italian Green | #009246 | Primary accent color for branding, buttons, links, active nav items, checkboxes |
| Italian Red | #CE2B37 | Used for branding, cancel buttons, menu card borders |
| Soft Red Hover | #f07f9d | Used for cancel buttons |
| Soft Green Hover | #afeecd | Used for edit and submit buttons |
| Light Green Tint | #e6f4ec | Accordion active background |
| Black | #000000 | Default text, nav links, social icons |
| White | #ffffff | Backgrounds, button label texts, base layout |


### Typography

* Headings & Emphasis Text:

    Roboto, imported from Google Fonts, is used for all headings (h1–h6), .display-4 elements, and paragraph text to create a bold and modern tone.

* Body Text:

    Lato, also imported from Google Fonts, is used as the base font for the body, providing a clean and readable style that contrasts subtly with the headings.

Both fonts are sans-serif and ensure a cohesive and elegant look across all devices.


### Imagery

To set the mood and style for visitors, reinforcing the Minitaly brand through visual storytelling, the project uses a single, carefully selected hero image on the landing page to immediately convey the essence of the restaurant. Image taken from this [Source](https://www.tastingtable.com/img/gallery/20-italian-dishes-you-need-to-try-at-least-once/l-intro-1643403830.jpg)

Description: A vibrant and inviting photograph of authentic Italian cuisine, showcasing rich colors like Italian green and Italian red—perfectly aligned with the brand’s color scheme.

The image is hosted locally in the static files and styled to appear full-width with a semi-transparent overlay and centered text.

To optimize the image for the website and improve loading times for users, I used [Image Resizer.com](https://imageresizer.com/) to resize and compress the image.

## Features
## Accessibility
## Technologies Used
### Languages Used
### Frameworks, Libraries & Programs Used
## Deployment & Local Development
### Deployment
### Local Development
### How to Fork
### How to Clone

## Testing
### Solved Bugs
### Known Bugs

## Credits
### Code Used
### Content
### Acknowledgments

