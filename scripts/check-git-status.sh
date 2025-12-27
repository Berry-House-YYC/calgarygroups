#!/bin/bash

# Check if we're behind remote
echo "🔄 Checking for remote updates..."

# Fetch latest changes without merging
git fetch origin >/dev/null 2>&1

# Count commits behind
BEHIND=$(git rev-list HEAD..origin/main --count 2>/dev/null || echo "0")

if [ "$BEHIND" != "0" ]; then
    echo ""
    echo "⚠️  WARNING: You're $BEHIND commit(s) behind origin/main"
    echo "   Run 'git pull --no-rebase' to update before making changes"
    echo ""
    echo "💡 Quick commands:"
    echo "   npm run sync  - Pull and start dev server"
    echo "   npm run push  - Pull and push changes"
    echo ""
else
    echo "✅ You're up to date with origin/main"
fi
