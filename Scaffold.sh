#!/usr/bin/env bash
set -e

ROOT="TheStarkProject"

echo "Scaffolding $ROOT ..."

# --- Top-level files & folders ---
mkdir -p "$ROOT"/{.github/workflows,.github/ISSUE_TEMPLATE,docs/setup-guides,shared/event-bus,shared/types,shared/ui-kit,infra/helm,infra/mosquitto,examples/full-stack-demo,examples/single-module-quickstarts}

# README.md, CONTRIBUTING.md, and LICENSE already exist in the repo root — not touched
touch "$ROOT"/package.json
touch "$ROOT"/turbo.json
touch "$ROOT"/pnpm-workspace.yaml
touch "$ROOT"/.github/workflows/ci.yml
touch "$ROOT"/.github/workflows/release.yml
touch "$ROOT"/docs/architecture.md
touch "$ROOT"/docs/event-bus-spec.md
touch "$ROOT"/infra/docker-compose.yml

# --- Modules ---
declare -A modules=(
  ["friday-core"]="src/llm src/memory src/plugins tests"
  ["heads-up"]="src/components src/widgets src/overlays src/hooks public"
  ["arm-ctrl"]="ros2_ws/src ros2_ws/launch ik safety"
  ["exo-telem"]="src/sensors src/fusion firmware"
  ["swarm-ops"]="sim src/planner src/coordinator missions"
  ["arc-sim"]="src/model src/visualizer"
  ["bench-bot"]="src/octoprint src/iot-triggers src/macros"
  ["vox"]="src/wake-word src/stt src/tts"
  ["sentry"]="src/scanners src/dashboard"
)

for module in "${!modules[@]}"; do
  base="$ROOT/modules/$module"
  mkdir -p "$base"
  touch "$base/README.md"

  # package.json for all except arm-ctrl (ROS2/Python-based)
  if [ "$module" != "arm-ctrl" ]; then
    touch "$base/package.json"
  fi

  for sub in ${modules[$module]}; do
    mkdir -p "$base/$sub"
  done
done

echo "✅ Done. Structure created under ./$ROOT"
echo ""
echo "Tree preview:"
if command -v tree &> /dev/null; then
  tree "$ROOT" -L 3
else
  find "$ROOT" -maxdepth 3 | sed -e 's|[^/]*/|  |g'
fi