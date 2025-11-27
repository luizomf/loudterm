# Load .env
set dotenv-load

# Variables
project_name := "loudterm"
python_version := "3.13.9"
root_dir := "src" / project_name

# Default: show all recipes
default:
  @just -l

# Clear screen + tmux scrollback
clear:
  @tmux clear-history
  @printf '\e[H\e[2J\e[3J'
  @clear

# Run pytest in watch mode using watchdog
test: clear
  -@watchmedo \
    shell-command --patterns="**/*.py" \
    --ignore-directories \
    --wait --recursive . \
    -c 'clear;pytest -q --color=yes --tb=short'

# Run loudterm via pyproject entrypoint
run: clear
  @echo "🚀 Running loudterm..."
  @uv run loudterm

# Full environment setup using uv (run once)
setup: clear
  uv python install {{python_version}}
  uv python pin {{python_version}}
  uv sync
