#!/bin/bash

echo -e "Creating test_configs directory...\n"
rm -r test_configs
cp -r config_templates test_configs
echo -e "Customizing config files with your directory path...\n"
sed -i "s|DIRECTORY/|$PWD/|g" test_configs/*.conf
sed -i "s|DIRECTORY/|$PWD/|g" test_configs/parsing/*.conf
sed -i "s|DIRECTORY/|$PWD/|g" test_configs/networking_init/*.conf
