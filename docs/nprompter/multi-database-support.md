# Multi-database support

Nprompter now supports fetching content from multiple Notion databases. You can configure this in the `[build.databases]` section of your configuration file:

```toml
[[build.databases]]
id = "c68ccc052d1b4eaaa3091e637f7011c5"

[[build.databases]]
id = "133439be4d2680aa840adbde85d8a923"
```

This will fetch content from both databases and create a single index file with the content from all databases. All the other options you can set in the `[build]` section will apply to all databases but you can also specify database-specific options for filtering and sorting under each database section.
