# Configuration file

_Nprompter_ looks for a configuration file named `nprompter.toml` in your current working directory (or you can specify a custom path using `--config [PATH]` / `-c [PATH]`). If not provided, it falls back to sensible defaults.

You can generate a starter `nprompter.toml` file with all default values by running:

```shell
nprompter create-config
```

---

## Default Configuration

```toml
[font]
size = 50
size_increment = 2
line_height = 1.2
line_height_increment = 0.1
max_size = 200
family = "'Roboto', sans-serif"

[processor]
skip_on_break = false
hide_non_default_colors = false
skip_square_brackets = false
replace_nbsp = true
render_code = "placeholder"

[screen]
padding.horizontal = 100
padding.vertical = 50
padding.increment = 10
padding.max_value = 250
hmargin.horizontal = 50
hmargin.vertical = 50
pmargin.horizontal = 50
pmargin.vertical = 50
scroll.speed = 10
scroll.speed_increment = 3
scroll.max_speed = 50
color = "white"
background = "black"

[build]
output = "prompter"
web_assets_folder = "web/assets"
filter.property = "Status"
filter.value = "Ready"
sort.property = "Name"
extra_html = ""

[manifest]
app_name = "Nprompter"
short_name = "Nprompter"
description = "A Notion-powered teleprompter"
```

---

## Configuration Reference

### `[font]`

Configures typography for the teleprompter display.

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `size` | Integer | `50` | Initial font size in pixels. |
| `size_increment` | Integer | `2` | Number of pixels font size changes per keyboard step (`Q`/`W`). |
| `max_size` | Integer | `200` | Maximum allowable font size in pixels. |
| `line_height` | Float | `1.2` | Initial line-height (in `em`). |
| `line_height_increment` | Float | `0.1` | Step size for line-height adjustments (`Z`/`X`). |
| `family` | String | `"'Roboto', sans-serif"` | CSS font family applied to scripts. |

### `[processor]`

Controls how Notion page blocks and formatting are parsed and converted to HTML.

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `skip_on_break` | Boolean | `false` | When `true`, stops processing blocks at the first Notion divider (`---`), discarding anything below it. |
| `hide_non_default_colors` | Boolean | `false` | When `true`, adds a `.notion-hide` class to blocks styled with custom Notion text/background colors (useful for director notes/cues). |
| `skip_square_brackets` | Boolean | `false` | When `true`, ignores text enclosed in brackets like `[stage cue]`. |
| `replace_nbsp` | Boolean | `true` | When `true`, converts non-breaking spaces (`\xa0`) into standard whitespace. |
| `render_code` | String | `"placeholder"` | How code blocks in Notion are rendered: `"placeholder"` (shows a `⚠ Code block ⚠` note), `"render"` (renders raw code inside `<pre>`), or `"skip"` (omits code blocks completely). |

### `[screen]`

Configures layout, margins, colors, and default scroll behavior.

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `color` | String | `"white"` | Text color for scripts. |
| `background` | String | `"black"` | Background color for the teleprompter screen. |
| `padding.horizontal` | Integer | `100` | Initial horizontal padding in pixels. |
| `padding.vertical` | Integer | `50` | Vertical padding in pixels. |
| `padding.increment` | Integer | `10` | Pixels added/removed when adjusting padding (`A`/`S`). |
| `padding.max_value` | Integer | `250` | Maximum horizontal padding in pixels. |
| `hmargin.horizontal` / `.vertical` | Integer | `50` | Margins around headings. |
| `pmargin.horizontal` / `.vertical` | Integer | `50` | Margins around paragraphs. |
| `scroll.speed` | Integer | `10` | Initial scroll timer delay (lower value = faster scrolling). |
| `scroll.speed_increment` | Integer | `3` | Speed change per keyboard step (`←`/`→` or remote). |
| `scroll.max_speed` | Integer | `50` | Upper limit for scroll timer delay. |

### `[build]`

Specifies defaults for content generation and indexing.

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `output` | String | `"prompter"` | Target directory where the website will be generated. |
| `web_assets_folder` | String | `"web/assets"` | Path to custom static assets to copy into the build folder. |
| `filter.property` | String | `"Status"` | Default Notion database property to filter against. |
| `filter.value` | String | `"Ready"` | Default value matching pages must have. |
| `sort.property` | String | `"Name"` | Default property used to sort scripts on index pages. |
| `extra_html` | String | `""` | Optional raw HTML injected into every page (e.g. analytics or custom headers/footers). |
| `database_id` | String | `None` | (Optional) Single default database ID to fetch if not supplied on the CLI. |
| `databases` | Array | `[]` | (Optional) List of multiple databases to process. See [Multi-database support](./multi-database-support.md). |

### `[manifest]`

Configures the web app manifest (`manifest.json`) when installed as a Progressive Web App (PWA).

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `app_name` | String | `"Nprompter"` | Full application name. |
| `short_name` | String | `"Nprompter"` | Short name displayed on mobile/desktop home screens. |
| `description` | String | `"A Notion-powered teleprompter"` | Description in the web manifest. |
