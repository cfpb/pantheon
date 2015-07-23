#!/bin/sh

##
# Clones the Unitybox repo which contains various helper functions,
# roles and common modules that we use in setting up this repo
##

# Clone the unitybox repo if it doesn't exist
if [ ! -d "../unitybox" ]; then
    echo "\033[1m Installing unitybox...\033[0m"
    git clone https://github.com/Ooblioob/unitybox.git ../unitybox
fi

cd ../unitybox

# Update to the latest version
echo "\033[1m Updating unitybox...\033[0m"
git fetch origin master
git reset --hard HEAD
git checkout master

echo "\033[1m Update completed!\033[0m"
