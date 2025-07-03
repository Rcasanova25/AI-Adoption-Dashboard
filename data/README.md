# Data Architecture

This directory contains the modular data loading system for the Economics of AI Dashboard.

## Structure

```
data/
├── loaders/          # Data source interfaces and implementations
├── extractors/       # PDF and document extraction utilities
├── models/           # Pydantic data models and schemas
├── transformers/     # Data transformation and calculation logic
├── cache/            # Caching layer for processed data
└── config/           # Data source configuration
```

## Design Principles

1. **Separation of Concerns**: Each component has a single responsibility
2. **Dependency Injection**: Loaders can be swapped for testing/development
3. **Type Safety**: All data validated through Pydantic models
4. **Performance**: Multi-layer caching for expensive operations
5. **Testability**: Each component independently testable

## Data Sources

All data loaded from authoritative PDF documents in the "AI adoption resources" directory:
- Stanford HAI AI Index Report 2025
- McKinsey Global Survey on AI
- OECD AI Policy Observatory reports
- Federal Reserve economic impact studies
- Goldman Sachs AI economic analysis