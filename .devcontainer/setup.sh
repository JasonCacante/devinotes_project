#!/bin/bash
set -e

# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Instalar dependencias del proyecto
uv sync

# Instalar dotfiles (zsh, plugins, p10k)
if [ -d "$HOME/dotfiles" ]; then
  bash "$HOME/dotfiles/install.sh"
else
  echo "AVISO: ~/dotfiles no encontrado - clona tu repo de dotfiles primero"
fi

# Claude Code config se monta directamente desde el host (~/.claude bind mount)
if [ -d ~/.claude ]; then
  echo "Directorio .claude montado desde el host"
else
  echo "AVISO: ~/.claude no encontrado - asegurate de que existe en el host WSL"
fi

echo "Setup completado"
