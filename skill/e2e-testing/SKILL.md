---
name: e2e-testing
description: >
  End-to-end testing skill for web applications using agent-browser CLI.
  Trigger terms: e2e, end-to-end, playwright, test, testing, UI testing,
  functional testing, integration testing, responsive, mobile testing.
---

## Browser Automation Tool

This skill uses **agent-browser** CLI for all browser automation. Do NOT use Playwright MCP tools.

| Tool | Usage |
|------|-------|
| **agent-browser** | CLI-based browser automation. Use `agent-browser <command>` |

For cloud/serverless environments (Cloudflare Workers, Vercel Edge), use the platform's native browser API (e.g., `@cloudflare/puppeteer`).

## When to Use
- Testing web application features through the UI
- Verifying user flows work correctly (login, forms, navigation)
- Checking responsive design across mobile, tablet, and desktop
- Testing a specific feature before deployment
- Full regression testing of an application

## When NOT to Use
- Unit testing individual functions
- API-only testing (no UI)
- Non-web applications (mobile apps, CLI tools)
- Performance/load testing

## Inputs the Agent Should Ask For (only if missing)
- **App URL**: The URL of the web application to test
- **Specific feature** (optional): If testing a particular feature, describe it
- **Credentials** (if needed): Login credentials for authenticated areas

## Outputs / Definition of Done
- Test summary with pass/fail counts
- Screenshots of any failures
- Responsive verification at mobile, tablet, and desktop
- Console error report (if any JavaScript errors found)
- Recommendations for fixing issues

## Procedure

### 1. Gather Context
If app URL not provided, ask for it. Determine if testing:
- A specific feature (user-specified)
- The entire application (default)

### 2. Initial Exploration
```bash
# Navigate to the app
agent-browser open <url>

# Get page structure with element refs
agent-browser snapshot -i

# Check for JavaScript errors
agent-browser errors

# Identify interactive elements
agent-browser snapshot
```

### 3. Create Test Plan
**If specific feature requested:**
- Focus all tests on that feature only
- Identify the elements and flows related to that feature

**If full app testing:**
- List all visible routes/pages from navigation
- Identify all forms and their required fields
- List all interactive elements (buttons, dropdowns, modals)
- Prioritize critical user flows (auth, main features, checkout if e-commerce)

### 4. Execute Tests
For each test case:
```bash
# 1. Announce: "Testing: [description]"

# 2. Take snapshot to get current element refs
agent-browser snapshot -i

# 3. Perform actions
agent-browser click @e1              # Click element
agent-browser fill @e2 "text"        # Fill input
agent-browser press Enter            # Submit form
agent-browser open <new-url>         # Navigate

# 4. Wait if needed
agent-browser wait 1000              # Wait 1 second
agent-browser wait ".selector"       # Wait for element

# 5. Verify expected state
agent-browser snapshot -i

# 6. If failure: take screenshot
agent-browser screenshot failure-name.png

# 7. Log result: PASS or FAIL with details
```

**Test Categories** (see references/test-categories.md):
- Navigation and routing
- Form submission and validation
- Interactive elements (modals, dropdowns, toggles)
- Data display and rendering
- Error states and edge cases

### 5. Responsive Testing
For each breakpoint (see references/responsive-breakpoints.md):

```bash
# Set viewport size
agent-browser set viewport 375 667   # Mobile
agent-browser set viewport 768 1024  # Tablet
agent-browser set viewport 1280 800  # Desktop

# Or use device presets
agent-browser set device "iPhone 12"
agent-browser set device "iPad"

# Navigate to key pages
agent-browser open <url>

# Take snapshot to verify:
agent-browser snapshot -i
# - Layout doesn't break
# - Navigation is accessible
# - No horizontal scroll
# - Text is readable

# Check for overflow issues
agent-browser eval "(() => {
  const issues = [];
  document.querySelectorAll('*').forEach(el => {
    if (el.scrollWidth > el.clientWidth) {
      issues.push({tag: el.tagName, class: el.className, issue: 'horizontal-overflow'});
    }
  });
  return JSON.stringify(issues);
})()"

# Check console for errors
agent-browser errors
```

### 6. Report Results
Generate a summary:
```
## Test Results

### Summary
- Total tests: X
- Passed: Y
- Failed: Z

### Failed Tests
[For each failure, include:]
- Test name
- Expected behavior
- Actual behavior
- Screenshot (if taken)

### Responsive Issues
[List any layout/functionality issues per breakpoint]

### Console Errors
[List any JavaScript errors found]

### Recommendations
[Actionable fixes for issues found]
```

### 7. Cleanup (CRITICAL)
**You MUST close the browser and kill any servers you started:**
```bash
# Close the browser
agent-browser close

# Find and kill any localhost processes you started
lsof -ti:PORT | xargs kill -9

# Or kill by process name
pkill -f "npm run dev"

# Verify the port is free
lsof -i:PORT  # Should return nothing
```

## Checks & Guardrails
- Always take a snapshot before performing actions to understand current state
- Use `snapshot -i` for interaction refs, `screenshot` for visual evidence
- Wait for elements with `wait <selector>` or `wait <ms>` when content loads async
- Check `errors` and `console` after each major action
- Refs (@e1, @e2) are only valid until the page changes - take new snapshots after navigation
- Always close the browser with `agent-browser close` when done

## References
- [agent-browser Commands](references/agent-browser-commands.md)
- [Test Categories](references/test-categories.md)
- [Responsive Breakpoints](references/responsive-breakpoints.md)
