# Veterinary Clinic Appointment System

## Project Description

The Veterinary Clinic Appointment System is a web-based application developed using Django to help manage veterinary clinic appointments, pets, doctors, users, and appointment requests.

The system provides different roles and permissions for Admins, Receptionists, and Doctors. It also helps prevent appointment conflicts, manage appointment priorities and statuses, handle edit requests, and provide a dedicated Doctor Dashboard.

---

## Features

### Authentication & User Roles

- User login and logout
- Role-based access control
- Three user roles:
  - Admin
  - Receptionist
  - Doctor
- Different permissions and dashboards depending on the user's role

---

### Pet & Appointment Management

- Add new pet appointments
- Edit existing appointments
- Delete appointments
- View all appointments
- Assign doctors to appointments
- Add visit date and appointment time
- Add visit reason
- Add owner information
- Generate automatic appointment numbers

Example:

APT-0010

---

### Appointment Scheduling

- Select available appointment times
- Check booked appointment times
- Prevent appointment time conflicts
- Prevent overlapping appointments based on the doctor's consultation time
- Limit the maximum number of appointments per doctor per day

---

### Appointment Filters

Appointments can be filtered by:

- Doctor
- Today
- This Week
- Normal Priority
- Urgent Priority
- Emergency Priority

---

### Appointment Priority

Each appointment can have one of the following priorities:

- Normal
- Urgent
- Emergency

Priority is displayed using different visual indicators to make important appointments easier to identify.

---

### Appointment Status

Appointments can have different statuses:

- Waiting
- Arrived
- Cancelled

The system provides visual status indicators for each appointment.

---

## Doctor Dashboard

The system includes a dedicated Doctor Dashboard.

Doctors can view:

- All appointments
- Today's appointments
- This week's appointments
- Appointment number
- Appointment time
- Pet name
- Appointment priority
- Visit reason
- Total appointments for each doctor

The dashboard also supports filtering appointments by:

- All
- Today
- This Week

---

## Appointment Edit Request System

Receptionists and authorized users can submit requests to modify appointment information.

Available edit types include:

- Appointment Date
- Appointment Time
- Doctor
- Visit Reason
- Owner Phone
- Pet Name
- Priority

Each edit request includes a description explaining the reason for the requested change.

### Edit Request Status

Each request can have one of three statuses:

- Pending
- Approved
- Rejected

The Admin can review edit requests through the Django Admin Panel.

When an edit request is approved, the requested change is applied to the corresponding pet appointment.

---

## Django Admin Panel

The Django Admin Panel is used to manage:

- Users
- User Profiles
- Doctors
- Pets
- Edit Requests

Admins can:

- Manage users and roles
- Manage doctors
- View and filter appointments
- Review edit requests
- Approve or reject edit requests
- Monitor appointment information

---

## Statistics

The system provides appointment statistics including:

- Total number of pets
- Statistics by animal type
- Waiting appointments
- Arrived appointments
- Cancelled appointments

---

## Appointment PDF

The system can generate an appointment slip as a PDF containing information such as:

- Appointment Number
- Pet Name
- Owner Name
- Doctor
- Visit Date
- Appointment Time
- Priority
- Visit Reason

---

## Multilingual Support

The system supports:

- English
- Arabic

Users can switch between languages using the language switcher available in the application.

The Django Admin Panel also supports Arabic localization.

---

## Responsive Design

The application interface is designed to work on different screen sizes, including:

- Desktop
- Tablet
- Mobile

The Doctor Dashboard and appointment tables were tested using responsive browser device views.

---

## Technologies Used

- Python
- Django
- HTML5
- CSS3
- JavaScript
- SQLite
- Django Authentication
- Django Internationalization (i18n)
- ReportLab

---

## Project Structure

The project follows the Django MVC/MVT structure and includes:

- Models
- Views
- Forms
- URLs
- Templates
- Static CSS files
- Django Admin
- Authentication and Role Management

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/AmanyMoamen/Veterinary-Clinic.git

### 2. Open the Project Folder
       cd Veterinary-Clinic

### 3. Apply Database Migrations
       python manage.py migrate

### 4. Run the Development Server
       python manage.py runserver

### 5. Open the Application
      Visit:
      http://127.0.0.1:8000/pets/

Main System Roles

. Admin

. Manage users
. Manage doctors
. Manage pets and appointments
. Review edit requests
. Approve or reject edit requests
. View statistics

Receptionist

. Add appointments
. Manage pets
. View appointments
. Filter appointments
. Submit edit requests
. Manage appointment status

Doctor

. Access Doctor Dashboard
. View appointments
. Filter appointments by date
. View appointment details and priorities

Developed By
Amany Moamen