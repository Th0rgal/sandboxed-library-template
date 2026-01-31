---
name: atomic-design
description: >
  Front-end component architecture separating pure UI from data-connected components.
  Trigger terms: atomic design, component architecture, UI components, recharts,
  chart component, components/ui, component organization.
---

## Core Principle

Split components into two layers:

1. **Pure UI** (`components/ui/`) - Wraps libraries (Recharts, TanStack, etc.), receives data via props, zero data fetching
2. **Data + UI** (`components/[category]/`) - Imports UI component, handles data fetching and state

## Directory Structure

```
components/
├── ui/                    # Pure UI (library wrappers)
│   ├── Chart.tsx          # Wraps Recharts
│   ├── DataTable.tsx      # Wraps TanStack Table
│   └── Avatar.tsx
│
├── graphs/                # Data-connected graphs
│   ├── RevenueChart.tsx   # ui/Chart + revenue API
│   └── UserGrowthChart.tsx
│
├── profiles/              # Data-connected profiles
│   └── UserProfile.tsx    # ui/Avatar + user API
│
└── tables/                # Data-connected tables
    └── TransactionsTable.tsx
```

## Rules

### `components/ui/` (Pure UI)
- No `useQuery`, `useSWR`, `fetch`, or API calls
- All data via props
- Generic names: `Chart`, `DataTable`, `Avatar`

### `components/[category]/` (Data + UI)
- Imports from `components/ui/`
- Handles fetching, loading, error, empty states
- Domain-specific names: `RevenueChart`, `UserProfile`
- Category matches domain: `graphs/`, `profiles/`, `tables/`

## Anti-Patterns

```tsx
// BAD: Data fetching in UI component
// components/ui/Chart.tsx
export function Chart({ endpoint }) {
  const { data } = useQuery({ queryKey: [endpoint] }); // Wrong!
  return <LineChart data={data} />;
}

// BAD: Data component in ui/ folder
// components/ui/RevenueChart.tsx  <-- Wrong location!

// BAD: Duplicating library code in data components
// components/graphs/RevenueChart.tsx
return <ResponsiveContainer><LineChart>...</LineChart></ResponsiveContainer>
// Should use: <Chart data={chartData} />
```
