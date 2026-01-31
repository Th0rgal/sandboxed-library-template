# Test Categories

## 1. Navigation & Routing

**What to test:**
- All navigation links work and lead to correct pages
- Browser back/forward buttons work correctly
- Deep links/direct URLs load proper content
- 404 handling for invalid routes
- Redirects work as expected

**How to test:**
```
1. Snapshot page to find all links
2. Click each navigation link
3. Verify URL changed correctly
4. Verify expected content appears
5. Test browser back navigation
```

## 2. Forms & Input

**What to test:**
- Required field validation
- Input format validation (email, phone, etc.)
- Form submission success
- Error message display
- Form reset/clear functionality
- Multi-step forms (wizard flows)

**How to test:**
```
1. Submit empty form - verify required field errors
2. Submit with invalid data - verify format errors
3. Submit with valid data - verify success
4. Check error messages are clear and positioned correctly
```

## 3. Authentication (if applicable)

**What to test:**
- Login with valid credentials
- Login with invalid credentials (error handling)
- Logout functionality
- Session persistence (refresh page while logged in)
- Protected route access (redirect to login)
- Password reset flow (if testable)

**How to test:**
```
1. Navigate to login page
2. Enter invalid credentials - verify error
3. Enter valid credentials - verify redirect to dashboard
4. Refresh page - verify still logged in
5. Click logout - verify redirect to login
6. Try accessing protected route - verify redirect
```

## 4. Interactive Elements

**What to test:**
- Buttons trigger correct actions
- Modals open and close properly
- Dropdowns show options and select correctly
- Toggles/switches change state
- Accordions expand/collapse
- Tabs switch content
- Tooltips appear on hover

**How to test:**
```
1. Snapshot to find interactive elements
2. Click/interact with each
3. Verify expected state change
4. Verify animations complete (wait if needed)
5. Test keyboard navigation (Tab, Enter, Escape)
```

## 5. Data Display

**What to test:**
- Lists render all items
- Tables show correct data and columns
- Cards display expected content
- Pagination works (if present)
- Sorting works (if present)
- Filtering works (if present)
- Search returns correct results

**How to test:**
```
1. Verify initial data loads
2. Test pagination - next/prev pages
3. Test sorting - click column headers
4. Test filtering - apply filters, verify results
5. Test search - enter query, verify matches
```

## 6. State Changes & Feedback

**What to test:**
- Loading states appear during async operations
- Success messages after actions
- Error messages when operations fail
- Empty states when no data
- Optimistic updates (if applicable)

**How to test:**
```
1. Trigger async action
2. Verify loading indicator appears
3. Wait for completion
4. Verify success/error message
5. Test empty state by filtering to no results
```

## 7. Edge Cases

**What to test:**
- Very long text (overflow handling)
- Special characters in inputs
- Empty/null data handling
- Network error recovery (if testable)
- Concurrent actions
- Rapid repeated clicks (debouncing)

**How to test:**
```
1. Enter very long text in inputs
2. Enter special chars: <script>, émojis, etc.
3. Verify graceful handling, no breaking
```

## Priority Order

For time-limited testing, prioritize:

1. **Critical path** - Main user journey (signup → core feature → success)
2. **Authentication** - Login/logout if applicable
3. **Forms** - Primary data entry points
4. **Navigation** - Users can reach all sections
5. **Responsive** - Works on mobile
6. **Edge cases** - Last, if time permits
