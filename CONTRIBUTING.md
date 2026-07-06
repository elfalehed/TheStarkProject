# Contributing to TheStarkProject

First off, thanks for considering a contribution! This project only works as a community effort — whether that's code, documentation, hardware designs, bug reports, or ideas.

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Ways to Contribute](#-ways-to-contribute)
- [Getting Set Up](#-getting-set-up)
- [Project Structure](#-project-structure)
- [Branching & Commit Conventions](#-branching--commit-conventions)
- [Pull Request Process](#-pull-request-process)
- [Coding Standards](#-coding-standards)
- [Module-Specific Guidelines](#-module-specific-guidelines)
- [Security & Responsible Use Policy](#-security--responsible-use-policy)
- [Reporting Bugs](#-reporting-bugs)
- [Proposing New Modules](#-proposing-new-modules)

---

## 🤝 Code of Conduct

Be respectful, be constructive, be patient with beginners. Harassment, discrimination, or hostile behavior of any kind will not be tolerated. If you experience or witness unacceptable behavior, please open an issue tagged `conduct` or contact a maintainer directly.

---

## 🛠 Ways to Contribute

You don't need to write code to contribute:

- **Code** — new features, bug fixes, performance improvements
- **Documentation** — module READMEs, setup guides, architecture docs
- **Hardware designs** — CAD files, wiring diagrams, BOMs for physical builds
- **Testing** — writing tests, testing on different hardware/OS combos
- **Ideas & discussion** — opening issues to propose new modules or improvements
- **Triage** — helping label and reproduce reported bugs

---

## 💻 Getting Set Up

```bash
# Fork the repo, then clone your fork
git clone https://github.com/<your-username>/TheStarkProject.git
cd TheStarkProject

# Install dependencies (monorepo-wide)
pnpm install

# Run a specific module in dev mode
pnpm --filter heads-up dev

# Run all module tests
pnpm test
```

Each module under `modules/<module-name>/` has its own `README.md` with module-specific setup steps (e.g., ROS2 environment for `arm-ctrl`, simulator setup for `swarm-ops`). Read that before diving in.

---

## 🧱 Project Structure

Quick refresher — see the main `README.md` for the full breakdown:

```
TheStarkProject/
├── modules/        # Independent tools (friday-core, heads-up, arm-ctrl, etc.)
├── shared/          # Shared libraries (event-bus, types, ui-kit)
├── infra/           # Docker/Helm/broker configs
├── examples/        # Full-stack and quickstart demos
└── docs/            # Architecture & setup documentation
```

If your change is scoped to one module, keep it inside that module's folder. Cross-cutting changes (e.g., a new event-bus message type) belong in `shared/`.

---

## 🌿 Branching & Commit Conventions

**Branch naming:**
```
feature/<module>-<short-description>   e.g. feature/arm-ctrl-ik-solver
fix/<module>-<short-description>       e.g. fix/heads-up-widget-crash
docs/<short-description>               e.g. docs/contributing-update
```

**Commit messages** follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat(arm-ctrl): add inverse kinematics solver for 6-DOF arm
fix(heads-up): resolve WebSocket reconnect loop
docs(sentry): clarify defensive-use-only scope
chore(deps): bump ros2-bridge to 2.1.0
```

This keeps changelogs and release notes auto-generatable.

---

## 🔀 Pull Request Process

1. **Open an issue first** for anything non-trivial (new features, architectural changes) so we can discuss the approach before you invest time.
2. **Fork & branch** off `main` using the naming convention above.
3. **Write tests** for new functionality where applicable.
4. **Run the full check suite** before opening a PR:
   ```bash
   pnpm lint
   pnpm test
   pnpm build
   ```
5. **Open the PR** against `main`, filling out the PR template:
   - What does this change do?
   - Which module(s) does it affect?
   - How was it tested?
   - Any hardware dependencies (if applicable)?
6. **Respond to review feedback** — at least one maintainer approval is required before merge.
7. Squash-merge is preferred to keep history clean.

---

## 📐 Coding Standards

- **TypeScript** for all web/Node modules (`heads-up`, `friday-core`, `arc-sim`, `bench-bot`, `vox`, `sentry`). Strict mode on.
- **Python** for ROS2 nodes and simulation glue code, following PEP 8, type-hinted where practical.
- **Linting/formatting** is enforced via ESLint + Prettier (JS/TS) and `ruff`/`black` (Python) — run `pnpm lint --fix` before committing.
- **Tests**: Vitest/Jest for JS/TS, `pytest` for Python. Aim for meaningful coverage on core logic, not 100% for its own sake.
- **No hardcoded secrets** — use `.env` files (never committed) and document required variables in each module's README.

---

## 🧩 Module-Specific Guidelines

| Module | Notes |
|---|---|
| `friday-core` | New LLM tool integrations should be added via the plugin system, not hardcoded into the router. |
| `heads-up` | Follow the shared `ui-kit` design tokens for consistency across widgets. |
| `arm-ctrl` | All motion commands must pass through the safety/interlock layer — no bypassing e-stop logic. |
| `exo-telem` | Firmware changes need a corresponding hardware test log in the PR description. |
| `swarm-ops` | New mission types should include a simulation config, not just live-hardware code. |
| `arc-sim` | This is a simulation/visualization module only — no real high-voltage power electronics content. |
| `bench-bot` | IoT triggers should degrade gracefully if a device is offline. |
| `vox` | Wake-word models and audio samples must be original or properly licensed — no scraped voice data. |
| `sentry` | See the security policy below — defensive scope only. |

---

## 🛡 Security & Responsible Use Policy

`SENTRY` and any security-adjacent tooling in this project exist strictly for **defensive, educational purposes** — monitoring and scanning systems and networks **you own or have explicit permission to test**.

Contributions that add offensive capabilities (exploit development, unauthorized access tooling, malware, credential harvesting, etc.) will be **rejected and closed** without further discussion. This applies regardless of stated intent or framing (e.g., "for education," "for research").

If you discover a genuine security vulnerability in this project's own code, please report it privately by opening a draft security advisory on GitHub rather than a public issue.

---

## 🐛 Reporting Bugs

When filing an issue, please include:

- Module affected
- Steps to reproduce
- Expected vs. actual behavior
- Environment (OS, Node/Python version, hardware if relevant)
- Logs or screenshots if available

Use the bug report issue template — it captures all of this automatically.

---

## 💡 Proposing New Modules

Got an idea for a new tool (say, a materials-stress simulator or a lab-inventory tracker)? Open an issue with the `proposal` label and include:

- The problem it solves
- Rough scope (is it a full module or a feature of an existing one?)
- Any dependencies (hardware, external APIs, libraries)
- How it fits into the existing event-bus architecture

Maintainers will review and discuss feasibility before it's added to the roadmap.

---

Thanks again for contributing — every PR, issue, and idea moves this project forward. 🚀