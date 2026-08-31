---
title: Notion Formatting & Script Writing
description: Guide to supported Notion blocks, annotations, LaTeX equations, and custom director cue directives in Nprompter.
---

# Notion Formatting & Script Writing

_Nprompter_ translates Notion blocks into clean, high-contrast HTML elements designed for readability on camera.

---

## Supported Notion Blocks

| Notion Block | Output Element | Notes |
| :--- | :--- | :--- |
| **Paragraph** | `<p>` | Standard body text. Line breaks (`Shift+Enter`) become `<br />`. |
| **Heading 1, 2, 3** | `<h1>`, `<h2>`, `<h3>` | Formatted with distinctive margins and typography. |
| **Bulleted List** | `<ul><li>...</li></ul>` | Groups consecutive items automatically. |
| **Numbered List** | `<ol><li>...</li></ol>` | Groups consecutive numbered points. |
| **Quote & Callout** | `<blockquote>` | Rendered with blockquote styling. |
| **Divider** | `<hr />` | Horizontal rule across the screen (can also act as end-of-script marker). |
| **Equation** | `<p>$expression$</p>` | Rendered in LaTeX equation format. |
| **Code** | `<pre>` or placeholder | Configurable via `processor.render_code` setting. |

---

## Inline Styles & Text Annotations

All standard Notion rich text annotations are supported:

- **Bold** (`**text**` $\rightarrow$ `<b>text</b>`)
- *Italic* (`*text*` $\rightarrow$ `<i>text</i>`)
- <u>Underline</u> (`<u>text</u>`)
- ~~Strikethrough~~ (`<s>text</s>`)
- `Inline Code` (`<code>text</code>`)
- **Notion Colors:** Mapped to CSS classes matching Notion's palette (e.g. `.notion-red`, `.notion-blue_background`).

---

## Script Cues & Special Directives

You can tailor how _Nprompter_ parses your scripts using options in `[processor]` of your `nprompter.toml`:

### 1. Director Notes via Square Brackets
Set `skip_square_brackets = true` in `nprompter.toml`.

Any text enclosed in square brackets (e.g., `[B-roll: Show screenshot]` or `[Smile and look at camera]`) will be omitted from the teleprompter page, allowing you to keep production cues in Notion without cluttering your speech text.

### 2. Private Notes via Notion Colors
Set `hide_non_default_colors = true` in `nprompter.toml`.

Any paragraph or heading styled with a custom Notion color or background color will receive the `.notion-hide` CSS class (`display: none;`), hiding it on the prompter.

### 3. Stop Processing at Dividers
Set `skip_on_break = true` in `nprompter.toml`.

When a Notion divider (`---`) is encountered, _Nprompter_ stops processing the page and ignores all content below it. This is useful if you store references, research notes, or checklists at the bottom of your Notion pages.

### 4. Code Block Handling
Set `render_code` to:
- `"placeholder"` (default): Renders `⚠ Code block ⚠` to remind you on camera without filling the screen with complex code.
- `"render"`: Renders the full code snippet inside `<pre>`.
- `"skip"`: Completely omits code blocks from output.
