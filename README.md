# Veterinary Clinic Appointment System

## Project Description

The Veterinary Clinic Appointment System is a web-based application developed using Django to help manage veterinary clinic appointments, pets, doctors, users, branches, doctor schedules, and appointment requests.

The system provides different roles and permissions for Admins, Receptionists, and Doctors. It also helps prevent appointment conflicts, manage appointment priorities and statuses, control doctor availability, limit the maximum number of appointments per doctor per day, handle edit requests, and provide a dedicated Doctor Dashboard.

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
- Doctors and other system users can be linked to Django User accounts

---

### Branch Management

The system supports multiple veterinary clinic branches.

Currently supported branches include:

- Cairo Branch
- Alexandria Branch
- Minia Branch

Each doctor is assigned to a specific branch, and each receptionist is also assigned to a specific branch.

#### Branch-Based Access

- Receptionists can view and book appointments with doctors belonging to their assigned branch only.
- Doctors are associated with their assigned branch.
- Admins can view and manage doctors, receptionists, appointments, and data across all branches.
- Doctors can be filtered by branch through the Django Admin Panel.
- Appointments are associated with the corresponding branch.

This ensures that each branch manages its own doctors and appointments while the Admin has access to all branches.

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
- Associate appointments with the appropriate clinic branch
- Record the user who created each appointment

Example:

APT-0010

---

## Doctor Schedule Management

The system provides a dedicated Doctor Schedule management feature.

Each doctor can have a schedule for a specific date and branch.

A doctor schedule contains:

- Doctor
- Branch
- Date
- Shift
- Start Time
- End Time

### Available Shifts

The system supports two shifts:

- Morning Shift
- Evening Shift

For example, a doctor can have:

- Morning Shift: 09:00 - 13:00
- Evening Shift: 17:00 - 21:00

A doctor can have both shifts on the same day.

The system prevents duplicate schedules for the same doctor, date, and shift.

---

## Appointment Scheduling

The appointment scheduling system is based on the doctor's schedule.

The system:

- Displays appointment times based on the selected doctor's schedule.
- Supports multiple shifts during the same day.
- Generates available appointment slots between the doctor's start and end times.
- Takes the doctor's consultation time into consideration when generating appointment slots.
- Checks existing appointments before displaying a time as available.
- Prevents overlapping appointments.
- Prevents booking outside the doctor's scheduled working hours.
- Prevents booking on dates where the doctor does not have a schedule.
- Displays booked and available appointment times separately.
- Excludes cancelled appointments when checking appointment availability.
- Limits the maximum number of appointments per doctor per day.

### Appointment Time Conflicts

The system checks whether a new appointment overlaps with an existing appointment based on the doctor's consultation time.

This prevents two appointments from being scheduled at overlapping times.

For example, if a doctor's consultation time is 30 minutes, the system checks the complete appointment period rather than checking only the appointment start time.

---

## Maximum Appointments Per Day

Each doctor can have a configured maximum number of appointments per day.

For example:

```text
Doctor: Dr. Malek
Maximum appointments per day: 3
```


If Dr. Malek already has three appointments on the selected date, the system prevents creating a fourth appointment.

The system displays an appropriate message:

> This doctor already has the maximum number of appointments for this day.

This prevents the doctor from being overbooked even if there are still available time slots in the schedule.

---

## Appointment Filters

Appointments can be filtered by:

- Doctor
- Today
- This Week
- Normal Priority
- Urgent Priority
- Emergency Priority

---

## Appointment Priority

Each appointment can have one of the following priorities:

- Normal
- Urgent
- Emergency

Priority is displayed using different visual indicators to make important appointments easier to identify.

---

## Appointment Status

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
- Branches
- Doctors
- Doctor Schedules
- Pets
- Edit Requests
- Appointments

Admins can:

- Manage users and roles
- Manage clinic branches
- Assign doctors to branches
- Assign receptionists to branches
- Manage doctors
- Manage doctor schedules
- Define doctor working dates and shifts
- Define schedule start and end times
- View doctors by branch
- View and filter appointments
- View appointments across all branches
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
- Doctor Schedule Management
- Appointment Scheduling and Availability Management

---

## How to Run the Project

### 1. Clone the Repository
    
```bash
git clone 
https://github.com/AmanyMoamen/Veterinary-Clinic.git
```


### 2. Open the Project Folder
     
```bash
cd Veterinary-Clinic
```


### 3. Apply Database Migrations
    
```bash
python manage.py migrate
```


### 4. Run the Development Server
    
```bash
python manage.py runserver
```


### 5. Open the Application

Visit:
    
```text
http://127.0.0.1:8000/pets/
```


---

## Main System Roles

### Admin

- Manage users
- Manage roles
- Manage clinic branches
- Assign doctors to branches
- Assign receptionists to branches
- Manage doctors
- Manage doctor schedules
- Define doctor working dates and shifts
- Manage pets and appointments across all branches
- Review edit requests
- Approve or reject edit requests
- View statistics

### Receptionist

- Add appointments
- Manage pets
- View appointments
- View doctors in the assigned branch
- View available appointment times
- Book appointments based on doctor availability
- Filter appointments
- Submit edit requests
- Manage appointment status

### Doctor

- Access Doctor Dashboard
- View appointments
- Filter appointments by date
- View appointment details and priorities
- View appointments related to the doctor's branch

---

## Developed By

*Amany Moamen*