#!/usr/bin/env bash
# Compiles every exam's reference solutions and runs their randomized tests against java.util.
set -euo pipefail
cd "$(dirname "$0")/.."
for dir in source/*/; do
  name=$(basename "$dir")
  out=$(mktemp -d)
  javac -nowarn -d "$out" "$dir"java/*.java 2>&1 | grep -v '^Note:' || true
  echo "== $name"
  for f in "$dir"java/*.java; do
    java -cp "$out" "$(basename "$f" .java)"
  done
  rm -rf "$out"
done
