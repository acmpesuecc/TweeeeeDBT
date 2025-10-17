## Getting the code locally

Clone your fork and create an isolated virtual environment.

```bash
# replace <your-fork-url> with your fork URL or the repository URL
git clone <your-fork-url>
cd TweeeeeDBT

# create and activate a Python virtual environment (Linux / macOS)
python3 -m venv .venv
source .venv/bin/activate

# install project dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Branching & workflow

1. Fork the repository (if you don't have write access).
2. Create a descriptive branch from `main` for your work:

```bash
# update main
git checkout main
git pull origin main

# create a feature branch
git checkout -b feat/short-description
```

## Submitting a pull request

1. Push your branch to your fork:

```bash
git add .
git commit -m "Short, meaningful summary of changes"
git push -u origin feat/short-description
```

2. Open a Pull Request against `acmpesuecc:main` (the main repository). In your PR description, include:

- What you changed and why
- Any setup required to test the change
- Screenshots or logs if relevant

3. Address review comments and push follow-up commits to the same branch. The PR will be re-reviewed.

## Code style and tips

- Keep functions small and focused.
- Add or update inline comments and docstrings where behavior isn't obvious.
- Prefer clear variable names over clever ones.
- If you touch database schemas or migrations, document the change and update `DB/schema.sql` if applicable.

## PR checklist

Before requesting review, run through this checklist:

- [ ] My code follows the repository style.
- [ ] I ran tests locally and they pass.
- [ ] I updated documentation when appropriate.
- [ ] My PR has a clear title and description.

## Thank you

Thanks again for helping improve TweeeeeDBT. If you'd like help getting started, open an issue with the label `good first issue` or message the maintainers, we're happy to guide new contributors.