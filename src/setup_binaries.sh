#!/bin/bash

# System Binary Installer for Gundam News Corp Think-Tank
# Installs Tesseract (with JP/EN packs) and Poppler utilities.

set -e

# Visual formatting variables
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}============ AI THINK-TANK BINARY INSTALLER ============${NC}"

# Detect OS
OS_TYPE="$(uname -s)"

if [ "$OS_TYPE" = "Linux" ]; then
    echo -e "🖥️  Detected Operating System: ${GREEN}Linux${NC}"
    
    # Check if apt-get is available (Debian/Ubuntu systems)
    if [ -x "$(command -v apt-get)" ]; then
        echo -e "${BLUE}🔄 Updating package list and installing dependencies via apt...${NC}"
        sudo apt-get update -y
        sudo apt-get install -y tesseract-ocr tesseract-ocr-jpn poppler-utils
    # Check if dnf is available (Fedora/RHEL systems)
    elif [ -x "$(command -v dnf)" ]; then
        echo -e "${BLUE}🔄 Installing dependencies via dnf...${NC}"
        sudo dnf install -y tesseract tesseract-langpack-jpn poppler-utils
    else
        echo -e "${RED}❌ Error: Unsupported Linux package manager. Please manually install tesseract (with Japanese packs) and poppler-utils.${NC}"
        exit 1
    fi

elif [ "$OS_TYPE" = "Darwin" ]; then
    echo -e "🍏 Detected Operating System: ${GREEN}macOS${NC}"
    
    # Check if Homebrew is installed
    if ! [ -x "$(command -v brew)" ]; then
        echo -e "${YELLOW}⚠️  Homebrew not found! Installing Homebrew first...${NC}"
        /bin/bash -c "$(curl -fsSL https://githubusercontent.com)"
        # Apply homebrew to path for current session if it's a fresh installation
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    echo -e "${BLUE}🔄 Installing dependencies via Homebrew...${NC}"
    brew install tesseract tesseract-lang poppler

else
    echo -e "${RED}❌ Error: Unsupported Operating System: $OS_TYPE${NC}"
    exit 1
fi

echo -e "\n${BLUE}🔍 Verifying binary installations...${NC}"

# Verify Tesseract installation
if command -v tesseract >/dev/null 2>&1; then
    echo -e "  [${GREEN}OK${NC}] Tesseract Engine available: $(tesseract --version | head -n 1)"
    
    # Check if Japanese language data pack is correctly loaded
    if tesseract --list-langs | grep -q "jpn"; then
        echo -e "  [${GREEN}OK${NC}] Japanese Language Pack found."
    else
        echo -e "  [${RED}FAIL${NC}] Japanese Language Pack is missing from Tesseract path."
        exit 1
    fi
else
    echo -e "  [${RED}FAIL${NC}] Tesseract was not installed correctly."
    exit 1
fi

# Verify Poppler (pdftoppm is the main tool used by pdf2image)
if command -v pdftoppm >/dev/null 2>&1; then
    echo -e "  [${GREEN}OK${NC}] Poppler Utilities available (pdftoppm found)."
else
    echo -e "  [${RED}FAIL${NC}] Poppler Utilities (pdftoppm) missing from environment path."
    exit 1
fi

echo -e "\n${GREEN}🎉 System binaries successfully installed and verified!${NC}"
echo -e "You can now safely initialize your environment and run your Typer framework."
echo -e "${BLUE}========================================================${NC}"
