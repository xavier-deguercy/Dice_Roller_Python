﻿﻿# Guidance for AI coding agents — Dice Roller Python

This file gives focused, actionable context to help an AI agent be productive in this repository.

Overview
- **Purpose:** small D&D dice-rolling app. UI(s) call a separated core (business rules) in `src/core`.
- **Key components:**
  - Core logic: [src/core/dice_roller.py](src/core/dice_roller.py)
  - GUI (Tkinter): [src/v2_gui/app_tk.py](src/v2_gui/app_tk.py)
  - Console UI (placeholder): [src/v1_console/cli.py](src/v1_console/cli.py)
  - Tests: `tests/` (pytest)

Architecture & patterns to preserve
- The project uses a `src` package layout. Imports in code use `from src.core...` so prefer running modules (e.g. `python -m ...`) or ensure `PYTHONPATH` includes project root.
- UI <-> core separation: UI code never contains rules; it *calls* `DiceRoller` to get results. Keep UI logic (presentation, input validation) in UI modules and rules in `src/core/dice_roller.py`.
- Core return shapes: many methods return structured dicts for UIs to render (e.g. `roll_d20` returns keys like `mode`, `rolls`, `selected`). Maintain these shapes when extending APIs.

Helpful file examples
- See `src/core/dice_roller.py` for method names and error semantics (raises `ValueError` on unsupported dice or invalid args).
- See `src/v2_gui/app_tk.py` for how the UI consumes core APIs and how advantage/disadvantage and inspiration are composed.

Developer workflows (commands)
- Activate virtualenv on Windows (PowerShell):
  - `& .venv\\Scripts\\Activate.ps1`
- Run the Tkinter app (recommended way to keep imports working):
  - `python -m src.v2_gui.app_tk`
- Run tests (pytest):
  - `pytest -q`

Project-specific conventions
- Variable and UI labels are French (e.g., `DES_AUTORISES`, `inspiration_var`). Prefer concise French UI strings when touching the UI.
- Keep core logic language-agnostic (exception messages may be French), but preserve existing public function names and signatures.
- When adding new core functions, follow the existing pattern: validate args -> raise `ValueError` for bad input -> return simple primitives or small dicts for UI consumption.

Integration notes
- The GUI imports the core as `from src.core.dice_roller import DiceRoller` — avoid relative imports that break when running as a module.
- `d100` is treated/simulated conceptually (see comments). Be conservative with changes to d100 logic.

Testing guidance
- Tests use pytest and live in `tests/`. Follow existing test naming like `test_usXXX_*.py`.
- Prefer small unit tests for core methods (e.g., `roll_die`, `roll_d20`, `roll_many`) asserting deterministic aspects (e.g., raised exceptions, returned dict keys/types). Mock randomness only where determinism is required.

When in doubt
- Run the GUI manually (`python -m src.v2_gui.app_tk`) to observe expected strings and flows.
- Search for usages of a core method before changing its return shape — UIs currently expect dict keys like `rolls`, `selected`, `mode`.

Examples
- Quick REPL test:
  - `python -c "from src.core.dice_roller import DiceRoller; print(DiceRoller().roll_die(6))"`

Deliverables
- If you modify core APIs, update `src/v2_gui/app_tk.py` and tests accordingly.

If any part of this guidance is unclear or you'd like the instructions expanded (examples, more files referenced, or stricter lint/test rules), tell me which sections to refine.
