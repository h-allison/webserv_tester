#!/bin/bash

POST_DIR="DIRECTORY/www/demo/upload/"

# Ensure directory exists
mkdir -p "$POST_DIR"

# Generate unique filename
FILENAME="$POST_DIR$(date +%s%N)_$$.txt"

# Read the payload safely if CONTENT_LENGTH is set
if [ -n "$CONTENT_LENGTH" ] && [ "$CONTENT_LENGTH" -gt 0 ]; then
    dd bs=1 count="$CONTENT_LENGTH" 2>/dev/null > "$FILENAME"
fi

# --- HTTP COMPLIANT RESPONSE ---
# 1. Status Code
echo "HTTP/1.0 200 Created"

# 2. Headers
echo "Content-Type: text/plain"
# Good practice to prevent browser caching on API/CGI endpoints
echo "Cache-Control: no-cache" 

# 3. Empty line to separate headers from body
echo ""

# 4. Response Body
echo "Success: File uploaded successfully."
echo "Written to: $FILENAME"
