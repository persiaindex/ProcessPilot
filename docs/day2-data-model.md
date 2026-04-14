# ProcessPilot - Day 2 Data Model and API Plan

## Core entities

### User
Use Django built-in User.

Relevant fields already available:
- username
- email
- is_staff
- is_superuser

Project role options:
- employee
- reviewer
- admin

### Department
Fields:
- id
- name
- code
- created_at
- updated_at

### Request
Fields:
- id
- title
- description
- status
- priority
- department
- created_by
- assigned_reviewer
- ai_suggested_category
- processing_status
- created_at
- updated_at

Status values:
- draft
- submitted
- in_review
- approved
- rejected

Priority values:
- low
- medium
- high

Processing status values:
- not_started
- running
- completed
- failed

### Comment
Fields:
- id
- request
- author
- body
- created_at
- updated_at

### StatusHistory
Fields:
- id
- request
- old_status
- new_status
- changed_by
- changed_at
- note

## Relationships
- One Department has many Requests
- One User creates many Requests
- One User can review many Requests
- One Request has many Comments
- One Request has many StatusHistory records

## API endpoint plan

### Requests
- GET /api/requests/
- POST /api/requests/
- GET /api/requests/{id}/
- PATCH /api/requests/{id}/
- DELETE /api/requests/{id}/

### Workflow actions
- POST /api/requests/{id}/submit/
- POST /api/requests/{id}/approve/
- POST /api/requests/{id}/reject/

### Comments
- GET /api/requests/{id}/comments/
- POST /api/requests/{id}/comments/

### Departments
- GET /api/departments/

### Dashboard support later
- GET /api/dashboard/summary/

## Frontend screens supported by this API plan
- Login page
- Dashboard
- Create request form
- Request list page
- Request detail page
- Reviewer action flow

## Validation rules to remember
- Only the creator can edit a draft request
- Only reviewers or admins can approve or reject
- Approved or rejected requests should no longer be freely editable
- Every status change should create a StatusHistory record