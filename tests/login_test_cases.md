# E-commerce Login Test Cases

| TC_ID | Title | Pre-condition | Steps | Expected Result | Priority |
|-------|-------|---------------|-------|-----------------|----------|
| TC001 | Successful login with valid credentials | User has a registered account with email `user@example.com` and password `Password123!` | 1. Navigate to the login page.
2. Enter email `user@example.com`.
3. Enter password `Password123!`.
4. Click the **Login** button. | User is redirected to the account dashboard and sees a welcome message. | High |
| TC002 | Login fails with incorrect password | User has a registered account with email `user@example.com` | 1. Navigate to the login page.
2. Enter email `user@example.com`.
3. Enter incorrect password `WrongPass!`.
4. Click the **Login** button. | An error message “Invalid email or password.” is displayed and the user remains on the login page. | Medium |
| TC003 | Login fails with unregistered email | No account exists for email `unknown@example.com` | 1. Navigate to the login page.
2. Enter email `unknown@example.com`.
3. Enter any password.
4. Click the **Login** button. | An error message “No account found for this email.” is displayed. | Medium |
| TC004 | Login fails with empty fields | None | 1. Navigate to the login page.
2. Leave email and password fields empty.
3. Click the **Login** button. | Validation messages “Email is required” and “Password is required” are displayed. | Low |
| TC005 | Password reset flow after failed login | User has a registered account with email `user@example.com` | 1. Navigate to the login page.
2. Enter email `user@example.com`.
3. Enter incorrect password `WrongPass!`.
4. Click the **Login** button.
5. Click the **Forgot Password** link.
6. Enter email `user@example.com` and submit.
7. Check email for reset link and reset password to `NewPass123!`.
8. Attempt login with new password. | User receives a password reset email, resets password successfully, and can log in with the new password. | High |

**Negative Test Cases**

| TC_ID | Title | Pre-condition | Steps | Expected Result | Priority |
|-------|-------|---------------|-------|-----------------|----------|
| TC006 | Login with SQL injection attempt | None | 1. Navigate to the login page.
2. Enter email `admin@example.com' OR '1'='1`.
3. Enter password `anything`.
4. Click the **Login** button. | The system should reject the input and display an error message “Invalid email or password.” without granting access. | High |
