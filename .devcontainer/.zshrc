# Enable Powerlevel10k instant prompt.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export ZSH="$HOME/.oh-my-zsh"
export PATH="$HOME/.local/bin:$PATH"

ZSH_THEME="powerlevel10k/powerlevel10k"

plugins=(git zsh-syntax-highlighting zsh-autosuggestions)

source $ZSH/oh-my-zsh.sh

# Aliases
alias zshconfig="vi ~/.zshrc"
alias dcup="docker-compose up -d --wait"
alias dcdown="docker-compose down"
alias dcbash="docker-compose exec -it web bash"
alias dps="docker ps -a"

# uv
export PATH="$HOME/.cargo/bin:$PATH"
eval "$(uv generate-shell-completion zsh)"

# p10k
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
