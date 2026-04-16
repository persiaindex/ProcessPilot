# Day 7 Notes — Backend tests and API cleanup

## What I built today

I added a backend test suite for ProcessPilot using Django REST Framework's `APITestCase`.

The test suite covers:
- login
- current user endpoint
- authenticated request creation
- automatic `created_by`
- employee visibility restrictions
- reviewer visibility
- anonymous access blocking
- approval permission failures
- valid and invalid workflow transitions

## Why Day 7 matters

Day 6 made authentication and permissions work.
Day 7 proves those rules continue to work whenever I change the code later.

This is important because internal business apps rely on trust, correct access control, and predictable workflows.

## Commands

```bash
python manage.py test workflow.tests
python manage.py test workflow.tests -v 2