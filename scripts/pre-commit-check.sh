#!/bin/bash

# Pre-commit hook to check for common issues
# Place this in .git/hooks/pre-commit or use with husky

echo "🔍 Running pre-commit checks..."

# Check for unquoted YAML values that could break the build
echo "Checking YAML frontmatter..."
UNQUOTED_FILES=$(find src/content/organizations -name "*.md" -exec grep -l "age_range: [^\"']" {} \; 2>/dev/null)
if [ -n "$UNQUOTED_FILES" ]; then
    echo "❌ Found unquoted age_range values in:"
    echo "$UNQUOTED_FILES"
    exit 1
fi

UNQUOTED_FILES=$(find src/content/organizations -name "*.md" -exec grep -l "meeting_format: [^\"']" {} \; 2>/dev/null)
if [ -n "$UNQUOTED_FILES" ]; then
    echo "❌ Found unquoted meeting_format values in:"
    echo "$UNQUOTED_FILES"
    exit 1
fi

UNQUOTED_FILES=$(find src/content/organizations -name "*.md" -exec grep -l "location_area: [^\"']" {} \; 2>/dev/null)
if [ -n "$UNQUOTED_FILES" ]; then
    echo "❌ Found unquoted location_area values in:"
    echo "$UNQUOTED_FILES"
    exit 1
fi

UNQUOTED_FILES=$(find src/content/organizations -name "*.md" -exec grep -l "status: [^\"']" {} \; 2>/dev/null)
if [ -n "$UNQUOTED_FILES" ]; then
    echo "❌ Found unquoted status values in:"
    echo "$UNQUOTED_FILES"
    exit 1
fi

# Check for duplicate files
echo "Checking for duplicate organization files..."
DUPLICATES=$(find src/content/organizations -name "*.md" -exec basename {} \; | sort | uniq -d)
if [ -n "$DUPLICATES" ]; then
    echo "❌ Found duplicate organization files:"
    echo "$DUPLICATES"
    exit 1
fi

# Check if build would succeed
echo "Running quick build test..."
npm run build:11ty > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Build failed. Please run 'npm run build' to see errors."
    exit 1
fi

echo "✅ All pre-commit checks passed!"
