#!/bin/bash

# Update and Install System Dependencies
echo "Updating system packages..."
sudo apt-get update -y || brew update
echo "Installing system dependencies..."
sudo apt-get install -y git nmap || brew install git nmap

# Install Python packages
echo "Installing Python dependencies..."
pip install rich python-nmap

# Install Amass using Snap (Alternative methods may be required for non-Linux systems)
echo "Installing Amass..."
sudo snap install amass || echo "Snap not available, please install Amass manually."

# Ensure Go is installed for building from source
if ! command -v go &> /dev/null
then
    echo "Go could not be found, installing..."
    sudo apt-get install -y golang || brew install go
fi

# Setup GOPATH
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
mkdir -p "$GOPATH/bin"

echo "Cloning and installing tools..."

# Install Subfinder by cloning and building from source
git clone https://github.com/projectdiscovery/subfinder.git $GOPATH/src/github.com/projectdiscovery/subfinder
(cd $GOPATH/src/github.com/projectdiscovery/subfinder/v2/cmd/subfinder && go build .)
mv $GOPATH/src/github.com/projectdiscovery/subfinder/v2/cmd/subfinder/subfinder $GOPATH/bin/

# Install Httpx by cloning and building from source
git clone https://github.com/projectdiscovery/httpx.git $GOPATH/src/github.com/projectdiscovery/httpx
(cd $GOPATH/src/github.com/projectdiscovery/httpx/cmd/httpx && go build .)
mv $GOPATH/src/github.com/projectdiscovery/httpx/cmd/httpx/httpx $GOPATH/bin/

# Download and install Gau
echo "Downloading and installing Gau..."
curl -L "URL_TO_GAU_BINARY" -o gau.tar.gz
tar -xzf gau.tar.gz
mv gau $GOPATH/bin/
rm gau.tar.gz

# Download and install Waybackurls
echo "Downloading and installing Waybackurls..."
curl -L "URL_TO_WAYBACKURLS_BINARY" -o waybackurls.tar.gz
tar -xzf waybackurls.tar.gz
mv waybackurls $GOPATH/bin/
rm waybackurls.tar.gz

echo "All dependencies installed successfully!"
