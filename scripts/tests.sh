#!/bin/bash

# Test runner script for PyInstaller GUI

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    PyInstaller GUI - Test Runner       ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${YELLOW}Project directory: ${PROJECT_DIR}${NC}"
echo ""

cd "$PROJECT_DIR"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate
fi

# Install pytest if not installed
if ! python -c "import pytest" 2>/dev/null; then
    echo -e "${YELLOW}pytest not found. Installing...${NC}"
    pip install pytest
fi

# Install pytest-cov if not installed
if ! python -c "import pytest_cov" 2>/dev/null; then
    echo -e "${YELLOW}pytest-cov not found. Installing...${NC}"
    pip install pytest-cov
fi

echo ""
echo -e "${BLUE}Running tests...${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Run tests with coverage
python -m pytest tests/ -v --tb=short --cov=pyinstaller_gui --cov-report=term-missing --cov-report=html 2>&1

TEST_EXIT_CODE=$?

echo ""
echo -e "${BLUE}========================================${NC}"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${RED}✗ Some tests failed!${NC}"
fi

echo ""
echo -e "${YELLOW}Coverage report saved to: htmlcov/index.html${NC}"
echo -e "${BLUE}========================================${NC}"

exit $TEST_EXIT_CODE