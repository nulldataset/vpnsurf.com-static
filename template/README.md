# Example site template

This folder holds the **main site code template** for the static site: a Tailwind 4 CSS and HTML theme that serves as the base for the live site.

## Purpose

- **You add here:** Your Tailwind 4 (or other) CSS and HTML site template — e.g. layout, components, styles, and placeholder structure for the homepage, article pages, and navigation.
- **LLM / build use:** An LLM or build process uses this template as the **main site code**. It:
  - Organizes and adds **articles** from `source/articles/` into the theme (e.g. article list pages, article detail pages).
  - Organizes and adds **images** from `source/pictures/` (and optionally `source/videos/`) into the theme.
  - Produces the **complete site** (typically output into `public/`) so that the site is a coherent Tailwind-themed site populated with content from the source folders.

Content in `source/articles/`, `source/pictures/`, and `source/videos/` is copied to `public/` by `./build.sh`. The template in this folder is the skeleton: the LLM (or you) combines this theme with that content to build the final pages in `public/` (e.g. by generating HTML that uses the template layout and references the copied assets).

## For LLM / agents

- **Template location:** `template/` (this folder). Expect Tailwind 4 CSS and HTML files here as the example site template.
- **Content sources:** `source/articles/`, `source/pictures/`, `source/videos/`. The build copies these to `public/articles/`, `public/pictures/`, `public/videos/`.
- **Your task:** Use the template in `template/` as the main site code. Organize and add articles and images from the source folders into this theme (e.g. generate or adapt HTML/CSS so that the complete site lives in `public/` with a consistent layout, navigation, and content drawn from source). Ensure the built site in `public/` is ready for deploy (Surfer uploads `public/` to the live domain).

## Summary

| Input | Role |
|-------|------|
| **template/** | Main site code template (Tailwind 4 + HTML). Base theme and structure. |
| **source/articles/, source/pictures/, source/videos/** | Content to organize and add into the template. Copied to `public/` by `./build.sh`. |
| **public/** | Deploy target. The complete built site (template + content) should end up here. |
