# 🚀 Finance Dashboard API - Postman Testing Guide

This document provides the exact configurations for testing **every** endpoint of the API using Postman or any other REST client.

---

## 🛠️ Global Configuration
- **Base URL:** `http://localhost:8000`
- **Headers:** `Content-Type: application/json`
- **Auth:** For protected routes, use **Bearer Token** and paste your `access_token`.

---

## 🔐 1. Authentication Module

### 1.1 Register User
- **Method:** `POST`
- **Path:** `/auth/register`
- **Body (JSON):**
```json
{
  "name": "Test Admin",
  "email": "admin@test.com",
  "password": "Password123!",
  "role": "admin"
}
```

### 1.2 Login
- **Method:** `POST`
- **Path:** `/auth/login`
- **Body (JSON):**
```json
{
  "email": "admin@test.com",
  "password": "Password123!"
}
```
> **Note:** Copy the `access_token` from the response to use in the sections below.

---

## 💰 2. Financial Records Module

### 2.1 Create Record
- **Method:** `POST`
- **Path:** `/records`
- **Auth:** Bearer Token
- **Body (JSON):**
```json
{
  "amount": 2500.00,
  "type": "income",
  "category": "Salary",
  "date": "2024-04-01",
  "notes": "Monthly Paycheck"
}
```

### 2.2 List Records
- **Method:** `GET`
- **Path:** `/records`
- **Query Params:** `page=1`, `limit=10`, `type=income` (optional)
- **Auth:** Bearer Token

### 2.3 Get Single Record
- **Method:** `GET`
- **Path:** `/records/{id}` (e.g., `/records/1`)
- **Auth:** Bearer Token

### 2.4 Update Record
- **Method:** `PUT`
- **Path:** `/records/{id}` (e.g., `/records/1`)
- **Body (JSON):**
```json
{
  "amount": 2600.00,
  "notes": "Updated after bonus"
}
```

### 2.5 Delete Record
- **Method:** `DELETE`
- **Path:** `/records/{id}`
- **Auth:** Bearer Token

---

## 👥 3. User Management Module (Admin Only)

### 3.1 List All Users
- **Method:** `GET`
- **Path:** `/users`
- **Auth:** Bearer Token (Admin role required)

### 3.2 Create Staff User
- **Method:** `POST`
- **Path:** `/users`
- **Body (JSON):**
```json
{
  "name": "Analyst User",
  "email": "analyst@test.com",
  "password": "Password123!",
  "role": "analyst"
}
```

### 3.3 Update User
- **Method:** `PATCH`
- **Path:** `/users/{id}`
- **Body (JSON):** `{"name": "New Name"}`

### 3.4 Change Status
- **Method:** `PATCH`
- **Path:** `/users/{id}/status`
- **Body (JSON):** `{"status": "inactive"}`

---

## 📈 4. Dashboard Analytics

### 4.1 Global Summary
- **Method:** `GET`
- **Path:** `/dashboard/summary`
- **Auth:** Bearer Token

### 4.2 Category Summary
- **Method:** `GET`
- **Path:** `/dashboard/category-summary`
- **Auth:** Bearer Token

### 4.3 Recent Activity
- **Method:** `GET`
- **Path:** `/dashboard/recent`
- **Auth:** Bearer Token

### 4.4 Monthly Trends
- **Method:** `GET`
- **Path:** `/dashboard/monthly-trends`
- **Auth:** Bearer Token

---

## 🛡️ Role-Based Access Control (RBAC) Quick Guide

| Endpoint | Admin | Analyst | Viewer |
| :--- | :---: | :---: | :---: |
| Create Records | ✅ | ❌ (403) | ❌ (403) |
| Edit/Del Records | ✅ | ❌ (403) | ❌ (403) |
| Manage Users | ✅ | ❌ (403) | ❌ (403) |
| View Dashboards | ✅ | ✅ | ✅ |
| View Lists | ✅ | ✅ | ✅ |
