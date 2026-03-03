#!/bin/bash

# Script to check Netlify access and deploy
# Usage: ./scripts/deploy-netlify.sh

echo "🔍 Checking Netlify access..."

# Check if logged in
if ! netlify whoami &> /dev/null; then
    echo "❌ Not logged in to Netlify"
    echo "Please run: netlify login"
    exit 1
fi

echo "✅ Logged in to Netlify as: $(netlify whoami | grep 'email' | cut -d'"' -f4)"

# Check if we can access the site
echo ""
echo "📋 Checking available sites..."
netlify sites list

echo ""
echo "🚀 Deploying to production..."
netlify deploy --prod --dir=_site --site=b25e8199-75e5-45aa-bcab-ce5b441a661d
