# agent-browser Commands Reference

## Navigation

### open
Navigate to a URL.
```bash
agent-browser open <url>
agent-browser open https://example.com
```

### back / forward / reload
Standard navigation.
```bash
agent-browser back
agent-browser forward
agent-browser reload
```

## Page Analysis

### snapshot
Capture accessibility tree with element refs. **Preferred over screenshot for understanding page structure.**
```bash
agent-browser snapshot              # Full tree
agent-browser snapshot -i           # Interactive elements only (recommended)
agent-browser snapshot -c           # Compact (remove empty)
agent-browser snapshot -d 5         # Limit depth
agent-browser snapshot -s "#main"   # Scope to selector
agent-browser snapshot --json       # JSON output
```

### screenshot
Take a visual screenshot. Use for documenting failures or visual verification.
```bash
agent-browser screenshot                    # Default filename
agent-browser screenshot failure.png        # Custom filename
agent-browser screenshot --full page.png    # Full page
```

### pdf
Save page as PDF.
```bash
agent-browser pdf document.pdf
```

## Interactions

### click
Click on an element.
```bash
agent-browser click @e1              # By ref
agent-browser click "#submit"        # By selector
```

### dblclick
Double-click on an element.
```bash
agent-browser dblclick @e1
```

### type
Type text into an element (appends to existing content).
```bash
agent-browser type @e1 "hello world"
```

### fill
Clear and fill an input field.
```bash
agent-browser fill @e1 "new value"
```

### press
Press a keyboard key.
```bash
agent-browser press Enter
agent-browser press Tab
agent-browser press Control+a
agent-browser press Escape
```

### hover
Hover over an element.
```bash
agent-browser hover @e1
```

### focus
Focus an element.
```bash
agent-browser focus @e1
```

## Forms

### check / uncheck
Toggle checkboxes.
```bash
agent-browser check @e1
agent-browser uncheck @e1
```

### select
Select dropdown option.
```bash
agent-browser select @e1 "option-value"
agent-browser select @e1 "Option 1" "Option 2"  # Multiple
```

### upload
Upload files.
```bash
agent-browser upload @e1 file.pdf
agent-browser upload @e1 file1.pdf file2.pdf
```

## Getting Information

### get text
Get text content of element.
```bash
agent-browser get text @e1
```

### get html
Get inner HTML.
```bash
agent-browser get html "#content"
```

### get value
Get input value.
```bash
agent-browser get value @e1
```

### get attr
Get attribute value.
```bash
agent-browser get attr @e1 href
agent-browser get attr @e1 data-id
```

### get title / url
Get page title or URL.
```bash
agent-browser get title
agent-browser get url
```

### get count
Count matching elements.
```bash
agent-browser get count ".item"
```

### get box
Get element bounding box.
```bash
agent-browser get box "#element"
```

### get styles
Get computed styles (includes box, font, color).
```bash
agent-browser get styles @e1
```

## State Checks

### is visible / enabled / checked
Check element state.
```bash
agent-browser is visible @e1
agent-browser is enabled @e1
agent-browser is checked @e1
```

## Viewport & Layout

### set viewport
Resize browser window. Essential for responsive testing.
```bash
agent-browser set viewport 375 667    # Mobile
agent-browser set viewport 768 1024   # Tablet
agent-browser set viewport 1280 800   # Desktop
```

### set device
Use device presets.
```bash
agent-browser set device "iPhone 12"
agent-browser set device "iPad"
agent-browser set device "Pixel 5"
```

## Waiting

### wait
Wait for element, text, or time.
```bash
agent-browser wait 1000              # Wait 1 second
agent-browser wait ".selector"       # Wait for element
agent-browser wait "Loading..."      # Wait for text
```

## Debugging

### console
View console messages.
```bash
agent-browser console
agent-browser console --clear
agent-browser console --json
```

### errors
View JavaScript errors.
```bash
agent-browser errors
agent-browser errors --clear
```

### eval
Execute JavaScript on the page.
```bash
agent-browser eval "document.title"
agent-browser eval "window.innerWidth"
agent-browser eval "(() => { return JSON.stringify({test: 'data'}); })()"
```

## Finding Elements

### find
Find elements by various locators.
```bash
# By role
agent-browser find role button click --name Submit

# By text
agent-browser find text "Sign In" click

# By label
agent-browser find label "Email" fill "user@example.com"

# By placeholder
agent-browser find placeholder "Search..." type "query"

# By test ID
agent-browser find testid "login-btn" click

# By position
agent-browser find first ".item" click
agent-browser find last "button" click
agent-browser find nth 2 ".card" hover
```

## Sessions

### Named sessions
Isolate browser state.
```bash
agent-browser --session test open https://example.com
agent-browser --session test snapshot
agent-browser --session prod open https://prod.example.com
```

### session list
List active sessions.
```bash
agent-browser session list
```

## Cleanup

### close
Close the browser. **Always call when done.**
```bash
agent-browser close
```

## Best Practices

1. **Always snapshot before interacting** - Get fresh element refs
2. **Use `snapshot -i` over full snapshot** - Focuses on interactive elements
3. **Wait for dynamic content** - Use `wait` before assertions
4. **Check errors after actions** - Catch JavaScript errors early
5. **Element refs are ephemeral** - Don't reuse refs across navigations
6. **Always close when done** - Use `agent-browser close`
