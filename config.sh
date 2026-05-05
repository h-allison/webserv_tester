#!/bin/bash

echo -e "\nCreating test_configs directory..."
if [ -d "test_configs" ]; then
	rm -r test_configs
fi
cp -r config_templates test_configs

echo -e "Customizing config files with your directory path...\n"
sed -i "s|DIRECTORY/|$PWD/|g" test_configs/*.conf
sed -i "s|DIRECTORY/|$PWD/|g" test_configs/parsing/*.conf
sed -i "s|DIRECTORY/|$PWD/|g" test_configs/networking_init/*.conf

echo -e "Done.\n"

echo -e "To run the webserv tester from anywhere, add this alias to your .zshrc\n"

echo -e "alias testerv="$PWD+"/src/main.py"

echo -e "\nAlternately, you can run the tester from\n.$PWD/src/main.py\n"

