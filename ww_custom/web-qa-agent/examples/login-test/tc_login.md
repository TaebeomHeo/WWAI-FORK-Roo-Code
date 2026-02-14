# Login Feature Test Cases

## Overview

- **Feature:** User Authentication
- **Target:** E-commerce Login System
- **Total TCs:** 5

---

## TC_LOGIN_001: Valid Credentials Login

**Priority:** High
**Type:** Positive

### Pre-conditions

- Valid test account exists
- User is logged out

### Test Data

| Field    | Value            |
| -------- | ---------------- |
| email    | test@example.com |
| password | Test123!         |

### Steps

| #   | Action           | Tool             | Target         |
| --- | ---------------- | ---------------- | -------------- |
| 1   | Go to homepage   | browser_navigate | /              |
| 2   | Click login link | browser_click    | Login button   |
| 3   | Enter email      | browser_type     | Email field    |
| 4   | Enter password   | browser_type     | Password field |
| 5   | Click sign in    | browser_click    | Submit button  |
| 6   | Capture result   | browser_snapshot | -              |

### Expected Result

- Redirect to account dashboard
- "Welcome, [Username]" displayed
- "Logout" link visible

---

## TC_LOGIN_002: Invalid Password

**Priority:** High
**Type:** Negative

### Pre-conditions

- Valid email exists
- User is logged out

### Test Data

| Field    | Value            |
| -------- | ---------------- |
| email    | test@example.com |
| password | WrongPassword!   |

### Steps

| #   | Action               | Tool             | Target         |
| --- | -------------------- | ---------------- | -------------- |
| 1   | Go to login page     | browser_navigate | /login         |
| 2   | Enter valid email    | browser_type     | Email field    |
| 3   | Enter wrong password | browser_type     | Password field |
| 4   | Click sign in        | browser_click    | Submit button  |
| 5   | Capture error        | browser_snapshot | -              |

### Expected Result

- Stay on login page
- Error message: "Invalid email or password"
- Password field cleared

---

## TC_LOGIN_003: Empty Fields Submission

**Priority:** Medium
**Type:** Negative

### Pre-conditions

- User is on login page

### Test Data

| Field    | Value   |
| -------- | ------- |
| email    | (empty) |
| password | (empty) |

### Steps

| #   | Action             | Tool             | Target        |
| --- | ------------------ | ---------------- | ------------- |
| 1   | Go to login page   | browser_navigate | /login        |
| 2   | Click sign in      | browser_click    | Submit button |
| 3   | Capture validation | browser_snapshot | -             |

### Expected Result

- Form not submitted
- Validation errors displayed:
    - "Email is required"
    - "Password is required"

---

## TC_LOGIN_004: Invalid Email Format

**Priority:** Medium
**Type:** Negative

### Pre-conditions

- User is on login page

### Test Data

| Field    | Value         |
| -------- | ------------- |
| email    | invalid-email |
| password | Test123!      |

### Steps

| #   | Action              | Tool             | Target         |
| --- | ------------------- | ---------------- | -------------- |
| 1   | Go to login page    | browser_navigate | /login         |
| 2   | Enter invalid email | browser_type     | Email field    |
| 3   | Enter password      | browser_type     | Password field |
| 4   | Click sign in       | browser_click    | Submit button  |
| 5   | Capture validation  | browser_snapshot | -              |

### Expected Result

- Form not submitted
- Validation error: "Please enter a valid email address"

---

## TC_LOGIN_005: Remember Me Functionality

**Priority:** Low
**Type:** Positive

### Pre-conditions

- Valid test account exists
- Browser cookies cleared

### Test Data

| Field       | Value            |
| ----------- | ---------------- |
| email       | test@example.com |
| password    | Test123!         |
| remember_me | checked          |

### Steps

| #   | Action            | Tool              | Target            |
| --- | ----------------- | ----------------- | ----------------- |
| 1   | Go to login page  | browser_navigate  | /login            |
| 2   | Enter credentials | browser_fill_form | Email, Password   |
| 3   | Check remember me | browser_click     | Remember checkbox |
| 4   | Click sign in     | browser_click     | Submit button     |
| 5   | Close browser     | browser_close     | -                 |
| 6   | Reopen site       | browser_navigate  | /                 |
| 7   | Check login state | browser_snapshot  | -                 |

### Expected Result

- User remains logged in after browser restart
- Session persists based on "Remember Me" selection
