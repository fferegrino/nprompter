# nprompter

> A browser-based web teleprompter powered by Notion as a backend for editing and storing scripts.

[![Documentation](https://img.shields.io/badge/docs-fferegrino.github.io%2Fnprompter-blue)](https://fferegrino.github.io/nprompter/)
[![PyPI](https://img.shields.io/pypi/v/nprompter.svg)](https://pypi.org/project/nprompter/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Read the full documentation: [https://fferegrino.github.io/nprompter/](https://fferegrino.github.io/nprompter/)**

![](https://media.giphy.com/media/jioUQ1Jus86xwa2EBw/giphy.gif)

---

## Key Features

- 📝 **Write in Notion:** Draft and update scripts in your existing Notion workspace.
- 📺 **Browser Teleprompter:** High-contrast, smooth auto-scrolling with horizontal mirroring for teleprompter glass.
- 🎛️ **Full Keyboard & Remote Control:** Adjust speed, font size, padding, line height, or jump to top with keyboard or wireless presenter remotes (clickers).
- 🏷️ **Director Cues & Formatting:** Hide private stage notes via custom colors or brackets (`[...]`), and ignore footnotes after dividers (`---`).
- 📚 **Multi-Database Support:** Aggregate scripts across multiple Notion databases with customized filtering and sorting.
- 📱 **Installable PWA:** Offline-ready Progressive Web App with local settings persistence.

---

## Installation

Install `nprompter` using `pip` or `uv`:

```bash
pip install nprompter
```

---

## Quickstart

### 1. Set your Notion API Key

```bash
export NOTION_API_KEY="secret_..."
```

*(See the [Notion Integration Guide](https://fferegrino.github.io/nprompter/configuring-notion/create-integration/) to learn how to create your token and share your database).*

### 2. Generate Your Teleprompter

Build the static teleprompter files for a Notion database:

```bash
nprompter build [DATABASE_ID]
```

### 3. Launch the Teleprompter

Start a local web server and open the teleprompter directly in your browser:

```bash
nprompter serve
```

---

## Quick Reference & Commands

- `nprompter build [DATABASE_ID] [OPTIONS]`: Fetch pages and render the HTML teleprompter website.
- `nprompter serve [PORT] [DIRECTORY]`: Serve the generated files locally (default port: `8889`).
- `nprompter create-config`: Generate a customizable `nprompter.toml` configuration file.

### Essential In-Prompter Shortcuts

| Key | Action |
| :--- | :--- |
| <kbd>Space</kbd> / <kbd>F5</kbd> | Start / Pause auto-scrolling |
| <kbd>→</kbd> / <kbd>←</kbd> | Adjust scroll speed |
| <kbd>Q</kbd> / <kbd>W</kbd> | Decrease / Increase font size |
| <kbd>M</kbd> | Mirror screen (horizontal flip for glass reflection) |
| <kbd>F</kbd> | Fullscreen mode |
| <kbd>H</kbd> | Show keyboard shortcuts help modal |

See the [Keyboard Controls & Remote Guide](https://fferegrino.github.io/nprompter/nprompter/controls/) for all available shortcuts.
