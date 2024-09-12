#!/bin/bash

# Run the Python script to generate the static site
python3 src/main.py

# Ensure the public directory exists
if [ -d "public" ]; then
    # Change to the public directory and start the HTTP server
    cd public
    python3 -m http.server 8888
else
    echo "Error: public directory not found!"
fi
