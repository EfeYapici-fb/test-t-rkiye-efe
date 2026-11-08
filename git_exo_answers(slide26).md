# Git mini exo: commands and answers

## Part 1: Setup & config
```bash
git --version
git config --global user.name "Efe Yapici"
git config --global user.email "your_email@example.com"
git config --global --list      # to verify
```

## Part 2: First repository
```bash
mkdir my-first-repo
cd my-first-repo
git init
touch readme.txt
```

## Part 3: First commit
1. Current state: `git status`
2. Stage the file: `git add readme.txt`
3. Commit: `git commit -m "Add readme file"`
4. History: `git log`

## Part 4: Make changes
```bash
echo "This is my first repository" >> readme.txt
git status
git add readme.txt
git commit -m "Update readme file"
git log --oneline
```
- `git status` now shows `readme.txt` as **modified**, "Changes not staged for commit" (the change is in the working directory but not staged yet).
- Number of commits now: **2**.

## Part 5: Exploration
- `git diff`: shows the **unstaged** changes line by line (what changed since the last add/commit). Nothing is shown if everything is staged or committed.
- `git log --oneline`: shows the commit history in a compact form: one line per commit (short hash + message).

## Part 6: Branches
```bash
git branch                       # 1. list branches
git branch feature-script        # 2. create
git switch feature-script        # 3. switch (or: git checkout feature-script)
git switch -c dev                # 4. create and switch (or: git checkout -b dev)
git switch feature-script        # 5. back to feature-script
git branch                       # 6. verify (the * marks the current branch)
```

## Part 7: Bash script on a branch
```bash
git switch feature-script
touch install.sh
```
Content of `install.sh` (Linux/WSL; on macOS use `brew update` and `brew install tree`):
```bash
#!/bin/bash
echo "Starting installation..."
sudo apt-get update
sudo apt-get install -y tree
echo "Installation complete!"
```
```bash
chmod +x install.sh
git add install.sh
git commit -m "Add install script"
git log --oneline
```

## Part 8: Merge
```bash
git switch main                  # 1
ls                               # 2
git merge feature-script         # 3
ls                               # 4
git log --oneline                # 5
git branch -d feature-script     # 6
```
- 2. `install.sh` is **not** present on `main`: it was committed only on the `feature-script` branch, and `main` has not received it yet.
- 4. After the merge, `install.sh` **appears** on `main`.
- 5. The history now contains the "Add install script" commit (fast-forward merge: no extra merge commit, history stays linear).

## Part 9: Push to GitHub
1. On github.com: New repository, name `my-first-repo`, do **not** add a README (keep it empty).
```bash
git remote add origin https://github.com/EfeYapici-fb/my-first-repo.git   # 3
git branch -M main                                                         # make sure the branch is called main
git push -u origin main                                                    # 4
```
5. After refreshing: the repository now shows `readme.txt` and `install.sh` and the commits.

## Part 10: Delete and clone
```bash
cd ..                                            # 1. leave the project folder
rm -rf my-first-repo                             # 2. delete the local folder
git clone https://github.com/EfeYapici-fb/my-first-repo.git   # 3
cd my-first-repo                                 # 4
ls                                               # files are back
```

## Part 11: Full workflow
```bash
cd ..
rm -rf my-first-repo                  # 1. delete local folder
# 2. GitHub: my-first-repo > Settings > Delete this repository
mkdir bash-installer                  # 3
cd bash-installer
git init                              # 4
echo "# bash-installer: script that installs Python, pip and Jupyter" > README.md   # 5
git add README.md
git commit -m "Add README"            # 6
git switch -c feature-install         # 7
cp /path/to/env_install.sh .          # 8. copy the previous script into this repo
git add env_install.sh
git commit -m "Add install script"    # 9
git switch main                       # 10
git merge feature-install             # 11
git branch -d feature-install         # 12
# 13. GitHub: new repository "bash-installer" (empty)
git remote add origin https://github.com/EfeYapici-fb/bash-installer.git
git branch -M main
git push -u origin main               # 14
```

## Reflection questions
1. **Why is version control useful?** It records the history of every change, lets you go back to an earlier version, makes teamwork possible (several people on the same code) and protects against losing work.
2. **Staging vs committing?** Staging (`git add`) selects which changes will go into the next commit (the staging area). Committing (`git commit`) permanently saves those staged changes in the history.
3. **When to commit?** When a small, logical unit of work is finished and the code works (one feature, one fix), not too rarely and not for half-broken code.
4. **`git init` vs `git clone`?** `git init` creates a new empty repository in the current folder. `git clone` copies an existing remote repository (with its full history) to your computer.
5. **Why good commit messages?** They explain what changed and why, so that you and your teammates can understand the history, find bugs and review the work quickly.
6. **Purpose of branches?** To work on a feature or fix in isolation, without breaking the stable code on `main`, and to merge it back when it is ready.
7. **When create a new branch instead of working on main?** For a new feature, a bug fix, an experiment, or any change that might take time or break something, especially when several people work together.
