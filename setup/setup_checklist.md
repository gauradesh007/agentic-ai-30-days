# Setup Checklist — Agentic AI 30-Day Journey

This guide documents the complete development setup used for the Agentic AI 30-Day Journey.

The goal of this file is to help someone start from a fresh Linux Mint / Ubuntu-based machine and recreate the same working environment for:

- Python development
- VS Code development
- Git and GitHub workflow
- SSH authentication
- Ollama local LLM execution
- project-level virtual environments
- clean repository structure

---

# 1. System Assumptions

This setup was created and tested on:

- Linux Mint / Ubuntu-based Linux
- Python 3.12+
- Git
- VS Code
- GitHub
- Ollama
- Local LLM: llama3.2:1b

The same steps should work on most Ubuntu-based Linux distributions.

---

# 2. Update Linux System

Start by updating package lists:

```bash
sudo apt update
sudo apt upgrade -y
```

Install common developer utilities:

```bash
sudo apt install -y curl wget gpg git openssh-client python3 python3-pip python3-venv
```

Verify installation:

```bash
python3 --version
pip3 --version
git --version
ssh -V
```

---

# 3. Install VS Code

Install required packages:

```bash
sudo apt install -y wget gpg apt-transport-https
```

Add Microsoft signing key:

```bash
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
rm -f packages.microsoft.gpg
```

Add VS Code repository:

```bash
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
```

Install VS Code:

```bash
sudo apt update
sudo apt install -y code
```

Verify:

```bash
code --version
```

---

# 4. Recommended VS Code Extensions

Install these extensions:

- Python by Microsoft
- Pylance by Microsoft
- Black Formatter by Microsoft
- Material Icon Theme
- GitHub Theme

---

# 5. VS Code Formatting Setup

Use Black Formatter for Python.

1. Press `Ctrl + Shift + P`
2. Search `Format Document With`
3. Choose `Configure Default Formatter`
4. Select `Black Formatter`

Enable format on save:

1. Open Settings
2. Search `format on save`
3. Enable `Editor: Format On Save`

Recommended theme:

```text
GitHub Light Default
```

Recommended icon theme:

```text
Material Icon Theme
```

---

# 6. Configure Git

Set Git user name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
git config --global init.defaultBranch main
```

Verify:

```bash
git config --global --list
```

---

# 7. Create SSH Key for GitHub

Generate SSH key:

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

Start SSH agent:

```bash
eval "$(ssh-agent -s)"
```

Add key:

```bash
ssh-add ~/.ssh/id_ed25519
```

Show public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the full output.

---

# 8. Add SSH Key to GitHub

In GitHub:

1. Open GitHub Settings
2. Go to SSH and GPG keys
3. Click New SSH key
4. Add title, for example `Linux Mint Laptop`
5. Paste the public key
6. Save

Test SSH authentication:

```bash
ssh -T git@github.com
```

Successful output:

```text
Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.
```

---

# 9. Create Main Project Folder

```bash
mkdir -p ~/projects
cd ~/projects
```

Clone the repo:

```bash
git clone git@github.com:<your-username>/agentic-ai-30-days.git
cd agentic-ai-30-days
```

If starting fresh locally:

```bash
mkdir agentic-ai-30-days
cd agentic-ai-30-days
git init
```

---

# 10. Recommended Repository Structure

```text
agentic-ai-30-days/
│
├── setup/
│   └── setup_checklist.md
│
├── notes/
│   ├── day01.md
│   ├── day02.md
│   ├── day03.md
│   ├── day04.md
│   ├── day05.md
│   └── day06.md
│
├── resources/
├── projects/
│
├── day01-first-agent/
├── day02-multi-tool-agent/
├── day03-stateful-agent/
├── day04-react-agent/
├── day05-memory-agent/
├── day06-planning-agent/
│
├── README.md
└── .gitignore
```

Folder purposes:

| Folder | Purpose |
|---|---|
| setup | environment setup and onboarding |
| notes | daily conceptual notes |
| resources | future diagrams, screenshots, references |
| projects | future real-world capstone projects |
| dayXX folders | daily learning projects |

---

# 11. Python Virtual Environment Per Project

Each day project uses its own virtual environment.

Example:

```bash
cd ~/projects/agentic-ai-30-days/day06-planning-agent
python3 -m venv venv
source venv/bin/activate
pip install requests
```

Verify active Python:

```bash
which python
```

Expected:

```text
/home/<user>/projects/agentic-ai-30-days/day06-planning-agent/venv/bin/python
```

Deactivate:

```bash
deactivate
```

Why use one venv per project?

- dependency isolation
- fewer package conflicts
- cleaner project setup
- reproducible execution
- safer experimentation

---

# 12. .gitignore Setup

Create `.gitignore` in repo root:

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc

# Virtual environments
venv/
.venv/

# Environment variables
.env

# VS Code
.vscode/

# OS files
.DS_Store
Thumbs.db
EOF
```

Never commit:
- `venv/`
- `.env`
- API keys
- secrets
- local machine-specific files

---

# 13. Install Ollama

Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify:

```bash
ollama --version
```

Check available models:

```bash
ollama list
```

Check API health:

```bash
curl http://localhost:11434/api/tags
```

If you see this while running `ollama serve`:

```text
bind: address already in use
```

Ollama is already running on port `11434`.

---

# 14. Pull Local Model

```bash
ollama pull llama3.2:1b
```

Test:

```bash
ollama run llama3.2:1b
```

Type:

```text
hello
```

Exit:

```text
/bye
```

---

# 15. Running Python Agent Projects

Example:

```bash
cd ~/projects/agentic-ai-30-days/day06-planning-agent
source venv/bin/activate
python agent.py
```

If using XFCE terminal, verify:

```bash
pwd
which python
```

Correct Python should be inside the current project `venv`.

---

# 16. Git Workflow

From repo root:

```bash
cd ~/projects/agentic-ai-30-days
git status
git add .
git status
git commit -m "Day X: describe what changed"
git push
git status
```

Expected final status:

```text
nothing to commit, working tree clean
```

If push is rejected:

```bash
git pull --rebase origin main
git push
```

Do not force push casually.

---

# 17. GitHub Pages Portfolio Setup

Create a GitHub Pages repository named:

```text
<your-username>.github.io
```

Clone locally:

```bash
cd ~/projects
git clone git@github.com:<your-username>/<your-username>.github.io.git
cd <your-username>.github.io
```

Create `index.html`:

```bash
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Your Name | Agentic AI Portfolio</title>
</head>
<body>
  <h1>Your Name</h1>
  <p>I am building agentic AI systems in public.</p>

  <h2>30-Day Agentic AI Journey</h2>
  <p>This website will showcase learning logs, projects, demos, and deployed AI agents.</p>

  <h2>Links</h2>
  <ul>
    <li><a href="https://github.com/<your-username>/agentic-ai-30-days">Agentic AI 30-Day Repo</a></li>
  </ul>
</body>
</html>
EOF
```

Commit and push:

```bash
git add .
git commit -m "Create initial portfolio homepage"
git push
```

Website:

```text
https://<your-username>.github.io
```

---

# 18. GitHub Profile README Setup

Create a special GitHub repository named exactly:

```text
<your-username>
```

Add a `README.md`.

GitHub automatically shows this on your profile page.

Recommended sections:
- short intro
- current focus
- areas of expertise
- certifications
- tech stack
- current project
- portfolio link
- LinkedIn link

---

# 19. Recommended GitHub Repository About Settings

For the main learning repo, add:

## Description

```text
Hands-on 30-day journey building Agentic AI systems, multi-tool AI agents, workflow orchestration, and local LLM applications using Python and Ollama.
```

## Website

```text
https://<your-username>.github.io
```

## Topics

```text
agentic-ai
ai-agents
python
ollama
llm
workflow-automation
local-llm
ai-engineering
```

---

# 20. Daily Project Setup Template

For each new day:

```bash
cd ~/projects/agentic-ai-30-days

mkdir dayXX-project-name
cd dayXX-project-name

python3 -m venv venv
source venv/bin/activate

pip install requests

touch agent.py README.md

code .
```

Run:

```bash
python agent.py
```

---

# 21. Recommended Daily Closeout

At the end of each day:

1. Clean/comment `agent.py`
2. Update day project `README.md`
3. Create/update `notes/dayXX.md`
4. Update root project `README.md`
5. Test program from terminal
6. Commit and push

Commands:

```bash
cd ~/projects/agentic-ai-30-days
git status
git add .
git status
git commit -m "Day X: short summary"
git push
git status
```

---

# 22. Troubleshooting Checklist

## Python file runs but prints nothing

Check if file is empty or unsaved:

```bash
ls -l agent.py
head -20 agent.py
```

Save in VS Code:

```text
Ctrl + S
```

---

## Module not found

Activate venv:

```bash
source venv/bin/activate
```

Install dependency:

```bash
pip install requests
```

---

## Wrong Python is running

```bash
which python
```

Expected:

```text
.../current-project/venv/bin/python
```

---

## Ollama timeout

Check Ollama:

```bash
curl http://localhost:11434/api/tags
```

Warm model:

```bash
ollama run llama3.2:1b
```

Exit:

```text
/bye
```

Increase timeout if needed:

```python
timeout=600
```

---

# 23. Engineering Principles Learned During Setup

Important principles:

- verify before assuming
- check current directory
- activate correct virtual environment
- never commit secrets
- use per-project venvs
- document everything
- commit small meaningful changes
- use `git status` frequently
- prefer clarity over cleverness

---

# 24. Final Setup Verification

A correct setup should allow:

```bash
cd ~/projects/agentic-ai-30-days/day06-planning-agent
source venv/bin/activate
which python
python agent.py
```

Expected:
- project venv Python is used
- agent runs successfully
- Ollama responds locally
- final controller answer prints

---

# Final Note

This setup is designed for learning real AI workflow engineering.

The goal is not just to run scripts.

The goal is to build a professional engineering environment for:

- reliable AI agents
- workflow orchestration
- local LLM development
- GitHub-based proof-of-work
- future capstone projects
