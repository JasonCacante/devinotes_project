#!/bin/bash
set -e

# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Instalar dependencias del proyecto
uv sync

# Instalar oh-my-zsh sin interacción
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Instalar Powerlevel10k
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"

# Instalar plugins de zsh
git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting.git \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting"

git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions.git \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions"

# Copiar .zshrc limpio (sin secrets)
cp .devcontainer/.zshrc ~/.zshrc

# Configurar zsh como shell por defecto
sudo chsh -s "$(which zsh)" "$USER"

echo "Setup completado"
