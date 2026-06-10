#!/bin/bash

echo -e "\nCreating test_configs directory..."
if [ -d "test_configs" ]; then
	rm -r test_configs
fi
cp -r templates/config_templates test_configs

echo -e "Customizing config files with your directory path...\n"
sed -i "s|DIRECTORY/|$PWD/|g" test_configs/*.conf
sed -i "s|DIRECTORY/|$PWD/|g" test_configs/parsing/*.conf
sed -i "s|DIRECTORY/|$PWD/|g" test_configs/networking_init/*.conf

#####################################################################

echo -e "\nCreating scripts which require custom paths..."
if [ -f "www/demo/scripts/post_body.sh" ]; then
	rm "www/demo/scripts/post_body.sh"
fi
cp -r templates/script_templates/post_body.sh www/demo_with_cgi/scripts/post_body.sh

echo -e "Customizing scripts with your directory path...\n"
sed -i "s|DIRECTORY/|$PWD/|g" www/demo/scripts/post_body.sh

#####################################################################

echo -e "Done.\n"

echo -e "To run the webserv tester from anywhere, add this alias to your .zshrc or .bashrc\n"

echo -e "alias testserv=$PWD/tests/main.py"

echo -e "\nAlternately, you can run the tester from\n.$PWD/tests/main.py\n"
