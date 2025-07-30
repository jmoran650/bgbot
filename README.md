# bgbot

> **Hearthstone Battlegrounds Simulator**
>
> This README shows you how to clone, set up, and run the codebase on **macOS** and **Windows 10/11**.
>
> The instructions assume Python 3.12, a *src/* layout, and that you want an **editable** install so changes are picked up live.

---

## Table of Contents

1. [Clone the repo](#1-clone-the-repo)
2. [macOS quick‑start](#2-macos-quick-start)
3. [Windows quick‑start](#3-windows-quick-start)
4. [Common developer commands](#4-common-developer-commands)
5. [Optional: GPU wheels](#5-optional-gpu-wheels)
6. [Troubleshooting](#6-troubleshooting)

---

## 1  Clone the repo

```bash
# Unix‑like shells (macOS, WSL, Git‑Bash)
git clone https://github.com/your‑org/bgbot.git
cd bgbot
```

For Windows users who prefer **Git GUI** or **GitHub Desktop**, clone as usual and then open a PowerShell window inside the `bgbot` folder.

---

## 2  macOS quick‑start

### 2.1 Prerequisites

| Tool                         | Install command                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------- |
| **Xcode Command Line Tools** | `xcode-select --install`                                                                          |
| **Homebrew**                 | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| **pyenv**                    | `brew install pyenv`                                                                              |

> If you prefer the system Python, skip *pyenv* and use `python3` instead of `python` in the commands below.

### 2.2 Add *pyenv* to zsh (run once)

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zprofile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zprofile
echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
exec "$SHELL"   # reload shell
```

### 2.3 Set up Python, venv, and project

```bash
pyenv install 3.12.2       # ⏳ first time only
pyenv local   3.12.2       # pins version inside repo
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'    # editable install + dev extras
```

### 2.4 Smoke‑test

```bash
python -m bgbot.main       # → prints tensor shapes
```

---

## 3  Windows quick‑start

### 3.1 Prerequisites

| Tool                | Where to get it                                                                                               |
| ------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Git for Windows** | [https://gitforwindows.org/](https://gitforwindows.org/)                                                      |
| **Python 3.12**     | [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/) or `pyenv-win`         |
| **Build tools**     | Install “C++ build tools” via [Visual Studio Build Tools](https://aka.ms/vsbuildtools) (needed for some deps) |

*Recommended shell:* **PowerShell** (or Windows Terminal).

### 3.2 Clone & set up

```powershell
cd C:\dev
git clone https://github.com/your-org/bgbot.git
cd bgbot

# If you installed Python via the official installer
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Or, with pyenv‑win (https://github.com/pyenv-win/pyenv-win)
# pyenv install 3.12.2
# pyenv local 3.12.2
# python -m venv .venv

pip install -e .[dev]
```

### 3.3 Run the sanity check

```powershell
python -m bgbot.main    # tensor shapes should print
```

---

## 4  Common developer commands

| Task                    | Command                        |
| ----------------------- | ------------------------------ |
| Activate venv (macOS)   | `source .venv/bin/activate`    |
| Activate venv (Windows) | `.\.venv\Scripts\Activate.ps1` |
| **Lint**                | `ruff .`                       |
| **Format**              | `black .`                      |
| **Type‑check**          | `mypy src`                     |
| **Unit tests**          | `pytest -q`                    |
| **Run main**            | `python -m bgbot.main`         |
| **Run all hooks**       | `pre-commit run --all-files`   |

---

## 5  Optional: GPU wheels (PyTorch)

Pick the tag that matches your CUDA version; then:

```bash
pip install torch==2.7.1+cu126 torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cu126
```

For Apple Silicon (M‑series) GPUs you can stick with the default CPU wheels; Metal acceleration comes automatically.

---

## 6  Troubleshooting

| Symptom                            | Fix                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------- |
| `python: command not found`        | Run `exec "$SHELL"` (macOS) or open a new PowerShell window so PATH picks up *pyenv*. |
| `ModuleNotFoundError: bgbot`       | Did you run `pip install -e .` *inside the venv*?                                     |
| `zsh: no matches found: .[dev]`    | Quote the extras: `pip install -e '.[dev]'`.                                          |
| Pre‑commit blocks commit           | Run `pre-commit uninstall` **or** fix `.pre-commit-config.yaml`.                      |
| TensorFlow stub warning in VS Code | `pip install types-tensorflow`.                                                       |

---

## License

This project is licensed under the terms of the MIT License. See **LICENSE** for details.
