#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    PyInstaller GUI - Clean Test Files  ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo -e "${YELLOW}Cleaning test output directories...${NC}"
echo ""

# Remove test output directories and files
echo -e "${BLUE}Removing:${NC}"
echo -e "  - tests/coverage_html/"

if [ -d "tests/coverage_html" ]; then
    rm -rf tests/coverage_html
    echo -e "    ${GREEN}✓ Removed${NC}"
else
    echo -e "    ${YELLOW}⚠ Not found${NC}"
fi

echo -e "  - tests/report/"

if [ -d "tests/report" ]; then
    rm -rf tests/report
    echo -e "    ${GREEN}✓ Removed${NC}"
else
    echo -e "    ${YELLOW}⚠ Not found${NC}"
fi

echo -e "  - .pytest_cache/"

if [ -d ".pytest_cache" ]; then
    rm -rf .pytest_cache
    echo -e "    ${GREEN}✓ Removed${NC}"
else
    echo -e "    ${YELLOW}⚠ Not found${NC}"
fi

echo -e "  - tests/.coverage"

if [ -f "tests/.coverage" ]; then
    rm -f tests/.coverage
    echo -e "    ${GREEN}✓ Removed${NC}"
else
    echo -e "    ${YELLOW}⚠ Not found${NC}"
fi

echo -e "  - tests/.coverage.*"

if ls tests/.coverage.* 1>/dev/null 2>&1; then
    rm -f tests/.coverage.*
    echo -e "    ${GREEN}✓ Removed${NC}"
else
    echo -e "    ${YELLOW}⚠ Not found${NC}"
fi

echo -e "  - .pytest_cache/ (root)"

if [ -d ".pytest_cache" ]; then
    rm -rf .pytest_cache
    echo -e "    ${GREEN}✓ Removed${NC}"
else
    echo -e "    ${YELLOW}⚠ Not found${NC}"
fi

echo -e "  - htmlcov/ (root)"

if [ -d "htmlcov" ]; then
    rm -rf htmlcov
    echo -e "    ${GREEN}✓ Removed${NC}"
else
    echo -e "    ${YELLOW}⚠ Not found${NC}"
fi

echo -e "  - .coverage (root)"

if [ -f ".coverage" ]; then
    rm -f .coverage
    echo -e "    ${GREEN}✓ Removed${NC}"
else
    echo -e "    ${YELLOW}⚠ Not found${NC}"
fi

echo ""
echo -e "${GREEN}✓ Clean completed!${NC}"
echo ""
echo -e "${YELLOW}Note: To re-run tests with coverage, use: ./scripts/test.sh${NC}"
echo -e "${BLUE}========================================${NC}"