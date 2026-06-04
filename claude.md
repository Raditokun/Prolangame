# Developer Environment Instructions

You are acting as an AI coding assistant inside a specific project workspace. To maintain proper project organization and prevent conflicts with other modules, you must adhere to the following strict directory scoping rules:

## 🚨 Scope Restriction Rule

- **Your entire working scope is strictly restricted to the `claude/` directory.**
- You are **ONLY** allowed to create, modify, or delete files inside the `claude/` folder (e.g., `claude/main.py`).
- Do **NOT** create or modify any files in the root directory (`PROLANGAME/`) or any other folders outside of `claude/`.

## Expected Behavior

1. **File Operations:** If you are generating full code scripts or suggesting file structures, always prefix the paths with `claude/`.
2. **Context:** You may read or reference the global structure if necessary, but all actual code output must be isolated inside your designated folder.

Please acknowledge these boundaries before providing any code.
