#!/usr/bin/env bash
# Render build script

set -o errexit

# Upgrade pip and install build tools first
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt
