#!/bin/bash

# Script to check Netlify deployment status
# Usage: ./scripts/check-netlify.sh

NETLIFY_SITE_ID="7e5b0e0f-3c6f-4b5a-9e8e-7b0e0f3c6f4b5"
SITE_URL="https://calgarygroups.com"

echo "🔍 Checking Netlify deployment status..."
echo "Site: $SITE_URL"
echo ""

# Check if site is accessible
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$SITE_URL")

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Site is accessible (HTTP $HTTP_STATUS)"
elif [ "$HTTP_STATUS" = "301" ] || [ "$HTTP_STATUS" = "302" ]; then
    echo "✅ Site is redirecting (HTTP $HTTP_STATUS)"
else
    echo "❌ Site appears to be down (HTTP $HTTP_STATUS)"
    exit 1
fi

# Check latest deployment info if Netlify CLI is available
if command -v netlify &> /dev/null; then
    echo ""
    echo "📊 Latest deployment info:"
    netlify status --site "$NETLIFY_SITE_ID" 2>/dev/null || echo "Could not fetch deployment status"
else
    echo ""
    echo "💡 Install Netlify CLI for detailed deployment info:"
    echo "   npm install -g netlify-cli"
    echo "   netlify status --site $NETLIFY_SITE_ID"
fi

echo ""
echo "🌐 Check Netlify dashboard for more details:"
echo "   https://app.netlify.com/sites/calgarygroups/deploys"
