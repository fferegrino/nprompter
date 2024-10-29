# Configuration file

_Nprompter_ searches for a configuration file in the repository where it is currently running (or you can specify a location with the `--config`), if it does not find it uses some default values which are:

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

```

You can use the [`create_config`](/nprompter/usage) command to obtain an editable version of the configuration.