# Contributing to PyInstaller GUI

👍🎉 First off, thanks for your interest in contributing! 🎉👍

This document describes contribution guidelines that are specific to PyInstaller GUI. These are mostly guidelines, not strict rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table Of Contents

- [I don't want to read this whole thing, I just have a question!](#i-dont-want-to-read-this-whole-thing-i-just-have-a-question)
- [Reporting an Issue](#reporting-an-issue)
- [Request a Feature](#request-a-feature)
- [Pull Requests](#pull-requests)
  - [A New Feature / Change to an Existing Feature](#a-new-feature--change-to-an-existing-feature)
  - [Add or Update a Translation](#add-or-update-a-translation)
- [Style Guide](#style-guide)

## I don't want to read this whole thing, I just have a question!!!

Please don't create an issue to ask a question.

For questions and general help, create a new discussion and provide a clear description of what's going on.

## Reporting an Issue

Please don't create an issue to ask a question or get help with something specific to your application. Instead, create a new discussion.

If you run into an error or bug with PyInstaller GUI:

1. Open a new issue with the **"Bug report"** template.
2. Fill out the template.
3. Create the issue.

Please be sure to clearly explain what's happening, provide reproduction steps, and include a minimal reproducible example. Also, describe what you expected to happen.

## Request a Feature

If PyInstaller GUI doesn't do something you need or want it to do:

1. Open a new issue with the **"Feature request"** template.
2. Fill out the template.
3. Create the issue.

Please provide as much context as you can about what you're running into and be clear about why existing features and alternatives would not work for you.

## Pull Requests

### A New Feature / Change to an Existing Feature

If you want to add a feature or modify an existing one:

1. Go to create a pull request.
2. When filling out the description, read the instructions to pick the **✨ A new feature template**.
3. Fill out the new template.
4. Create the PR.

### Add or Update a Translation

If you want to add a new or update an existing translation:

1. Update the relevant translation files.
2. Go to create a pull request.
3. When filling out the description, read the instructions to pick the **📄 A new or updated translation template**.
4. Fill out the new template.
5. Create the PR.

If you are unable to submit a pull request, you can also submit the changes in a new issue.

## Style Guide

### Python

We use **Ruff** to format, lint, and auto-sort imports. The easiest way to use Ruff is through the Visual Studio Code extension, where formatting is run on save. You can also format using Ruff's CLI:

```sh
pip install ruff
ruff format .
```

### JavaScript, CSS, HTML, Markdown, JSON, YAML

We use **Prettier** for formatting. The easiest way to use Prettier is through the Visual Studio Code extension, where formatting is run on save. You can also format using Prettier's CLI:

```sh
npx prettier@2.8.8 --write .
```

Formatting is checked using a GitHub Action workflow, ensuring all PRs comply with the formatters and linting standards.
