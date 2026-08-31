# Multi-database support

_Nprompter_ supports fetching and aggregating content from multiple Notion databases in a single build.

When configured with multiple databases, _Nprompter_ creates individual subdirectories for each database as well as a consolidated global index page linking to all available scripts.

## Configuration

Configure multiple databases under `[build.databases]` in your `nprompter.toml`:

```toml
[build]
output = "prompter"
filter.property = "Status"
filter.value = "Ready"
sort.property = "Name"

# Database 1: Uses global defaults
[[build.databases]]
database_id = "c68ccc052d1b4eaaa3091e637f7011c5"

# Database 2: Overrides filter and sort properties
[[build.databases]]
database_id = "133439be4d2680aa840adbde85d8a923"
filter.property = "Category"
filter.value = "Recorded"
sort.property = "Episode"
```

## How It Works

1. **Global options:** Global settings specified in `[build]`, `[font]`, `[screen]`, and `[processor]` apply across all databases.
2. **Database-specific overrides:** You can provide distinct `filter.property`, `filter.value`, and `sort.property` fields inside any `[[build.databases]]` entry.
3. **Index Generation:**
   - Global root index: `prompter/index.html` lists all databases and their scripts.
   - Database sub-index: `prompter/<DATABASE_ID>/index.html` contains the scripts for that specific database.
   - Individual script: `prompter/<DATABASE_ID>/<SLUG>/index.html`.

## Building

Once configured in `nprompter.toml`, simply run:

```shell
nprompter build
```
