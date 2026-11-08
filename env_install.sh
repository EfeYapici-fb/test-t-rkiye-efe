#!/bin/bash
# env_install.sh - sets up a Python development environment (Python, pip, Jupyter)
# Works on macOS (Homebrew) and Linux (apt). Usage: ./env_install.sh

# ---------- Strict mode (bonus) ----------
# -e: stop at first failing command, -u: unset variable = error,
# -o pipefail: a pipeline fails if any command in it fails
set -euo pipefail

# ---------- Functions ----------

# Feature 1: pretty printing (blank line before and after, printf for portability)
pretty_print() {
    printf "\n%s\n\n" "$1"
}

# Feature 2: detect the operating system using $OSTYPE
detect_os() {
    case "$OSTYPE" in
        darwin*)  echo "macos" ;;
        linux*)   echo "linux" ;;
        *)        echo "unknown" ;;
    esac
}

# Install a package with the right package manager for this OS
install_package() {
    local pkg="$1"
    if [[ "$OS" == "macos" ]]; then
        brew install "$pkg"
    elif [[ "$OS" == "linux" ]]; then
        sudo apt-get update -y
        sudo apt-get install -y "$pkg"
    fi
}

# ---------- Main logic ----------

OS="$(detect_os)"
pretty_print "Detected operating system: $OS"

if [[ "$OS" == "unknown" ]]; then
    pretty_print "Unsupported operating system: $OSTYPE"
    exit 1
fi

# macOS needs Homebrew as its package manager
if [[ "$OS" == "macos" ]] && ! command -v brew >/dev/null 2>&1; then
    pretty_print "Homebrew is not installed. Install it from https://brew.sh and run this script again."
    exit 1
fi

# Feature 3: Python install check
if command -v python3 >/dev/null 2>&1; then
    pretty_print "Python is already installed: $(python3 --version)"
else
    pretty_print "python3 not found, installing it..."
    if [[ "$OS" == "macos" ]]; then
        install_package python3
    else
        install_package python3
        install_package python3-pip
    fi
    pretty_print "Python installed: $(python3 --version)"
fi

# Feature 4: pip version verification
if python3 -m pip --version >/dev/null 2>&1; then
    pretty_print "pip is available: $(python3 -m pip --version)"
else
    pretty_print "pip not found, installing it..."
    if [[ "$OS" == "linux" ]]; then
        install_package python3-pip
    else
        python3 -m ensurepip --upgrade
    fi
    pretty_print "pip installed: $(python3 -m pip --version)"
fi

# Feature 5: Jupyter Notebook installation (command depends on the OS)
pretty_print "Installing Jupyter Notebook..."
if [[ "$OS" == "macos" ]]; then
    # Homebrew Python is "externally managed", so use brew for Jupyter
    brew install jupyterlab || python3 -m pip install --user notebook
else
    # On Debian/Ubuntu, the apt package avoids the "externally-managed-environment" error
    sudo apt-get install -y jupyter-notebook || python3 -m pip install --user notebook
fi

if command -v jupyter >/dev/null 2>&1; then
    pretty_print "Jupyter installed: $(jupyter --version | head -n 1)"
else
    pretty_print "Jupyter installed but not in PATH. Try: python3 -m notebook"
fi

# Feature 6: macOS-only Homebrew health check
if [[ "$OS" == "macos" ]]; then
    pretty_print "Running Homebrew health check..."
    brew doctor || pretty_print "brew doctor reported warnings (see above)."
fi

pretty_print "All done! Launch Jupyter with: jupyter notebook"
