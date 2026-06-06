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

echo -e "To run the webserv tester from anywhere, add this alias to your .zshrc or .bashrc\n"

echo -e "alias testserv=$PWD/tests/main.py"

echo -e "\nAlternately, you can run the tester from\n.$PWD/tests/main.py\n"


if [ ! -e "www/42_tester_root/cgi_tester" ]; then
	echo -e "NOTE:   To pass the 42_tester section tests,
	you need to download the cgi_tester executable from intra
	and place it in the 42_tester_root directory like so:
	/www/42_tester_root/cgi_tester\n"
fi