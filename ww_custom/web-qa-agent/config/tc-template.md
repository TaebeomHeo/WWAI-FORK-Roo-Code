# Test Case Template

## TC*[FEATURE]*[NUM]: [Title]

**Priority:** High | Medium | Low
**Type:** Positive | Negative | Boundary | Security
**Feature:** Login | Search | Cart | Checkout | Other
**Created:** [Date]
**Last Updated:** [Date]

---

## Pre-conditions

- [ ] Condition 1
- [ ] Condition 2

## Test Data

| Field    | Value            | Notes              |
| -------- | ---------------- | ------------------ |
| email    | test@example.com | Valid test account |
| password | Test123!         | Meets requirements |

---

## Test Steps

| #   | Action           | Playwright Tool  | Target/Input   | Expected        |
| --- | ---------------- | ---------------- | -------------- | --------------- |
| 1   | Navigate to page | browser_navigate | /login         | Page loads      |
| 2   | Enter email      | browser_type     | email input    | Value entered   |
| 3   | Enter password   | browser_type     | password input | Masked input    |
| 4   | Click submit     | browser_click    | login button   | Form submits    |
| 5   | Verify result    | browser_snapshot | -              | Dashboard shown |

---

## Expected Result

- [ ] User redirected to dashboard
- [ ] Username displayed in header
- [ ] Logout button visible

## Verification Method

```
<browser_wait_for>
<text>Welcome</text>
</browser_wait_for>

<browser_snapshot />
```

---

## Execution History

| Date       | Executor | Result | Notes |
| ---------- | -------- | ------ | ----- |
| 2024-01-15 | Agent    | Pass   | -     |

---

## Related Items

- Related TC: TC_LOGIN_002
- Bug: BUG_001 (if found)
- Requirement: REQ_AUTH_001
