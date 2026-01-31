# Responsive Testing Breakpoints

## Standard Breakpoints

| Device     | Width  | Height | Notes                          |
|------------|--------|--------|--------------------------------|
| Mobile     | 375    | 667    | iPhone SE / small phones       |
| Tablet     | 768    | 1024   | iPad / standard tablets        |
| Desktop    | 1280   | 800    | Standard laptop screen         |

## How to Resize

Use `browser_resize` with width and height:

```
Mobile:  browser_resize(width=375, height=667)
Tablet:  browser_resize(width=768, height=1024)
Desktop: browser_resize(width=1280, height=800)
```

## What to Check at Each Breakpoint

### Mobile (375x667)

- [ ] Navigation collapses to hamburger menu
- [ ] Hamburger menu opens/closes correctly
- [ ] Text is readable (not too small)
- [ ] Touch targets are at least 44x44 pixels
- [ ] No horizontal scrollbar
- [ ] Forms are usable (inputs full width)
- [ ] Images scale appropriately
- [ ] Modals fit within viewport

### Tablet (768x1024)

- [ ] Layout adapts (may be 2-column)
- [ ] Navigation may still be hamburger or expanded
- [ ] Tables readable or scrollable
- [ ] Cards may stack or grid
- [ ] No awkward whitespace

### Desktop (1280x800)

- [ ] Full navigation visible
- [ ] Multi-column layouts work
- [ ] Tables fully visible
- [ ] Proper use of horizontal space
- [ ] No content stretching too wide

## Common Responsive Issues

### Layout Breaking
- Elements overlapping
- Content cut off
- Horizontal scroll appearing

### Navigation Problems
- Menu items inaccessible on mobile
- Hamburger menu not working
- Dropdowns cut off by viewport

### Typography Issues
- Text too small to read on mobile
- Line lengths too long on desktop
- Headings breaking awkwardly

### Touch Target Issues
- Buttons too small on mobile
- Links too close together
- Form inputs hard to tap

### Image Issues
- Images not scaling
- Images too large for mobile (slow load)
- Broken aspect ratios

## Testing Procedure

```
For each breakpoint:
1. Resize browser to breakpoint dimensions
2. Navigate to homepage
3. Take snapshot - verify layout
4. Check navigation functionality
5. Navigate to key pages (forms, data views)
6. Interact with main features
7. Check console for errors
8. Document any issues found
```

## Quick Responsive Test Checklist

```
[ ] Mobile: Can access all navigation?
[ ] Mobile: Can complete main user flow?
[ ] Mobile: Any horizontal scroll?
[ ] Tablet: Layout makes sense?
[ ] Tablet: Touch interactions work?
[ ] Desktop: Uses space efficiently?
[ ] Desktop: No oversized elements?
[ ] All: Console errors at any size?
```
