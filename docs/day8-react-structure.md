# Day 8 Notes — React structure, routes, layout, and API service layer

## What I built today

I created the base React application structure for ProcessPilot.

The frontend now includes:
- routing with `react-router-dom`
- a shared application layout
- a sidebar for navigation
- placeholder pages for dashboard, requests, create request, request detail, and login
- a reusable page header component
- a base API service layer for backend communication

## Why Day 8 matters

Day 8 gives the project a maintainable frontend shape.

Without this structure, later features would become messy and repetitive.
With this structure, new pages and API calls can be added in a clean and predictable way.

## Main lesson

A good frontend is not only about visuals.
It also needs clear separation between:
- routes
- layout
- pages
- shared components
- API communication

## Commands

```bash
npm install
npm install react-router-dom
npm run dev