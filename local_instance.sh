#!/bin/bash

# Check for environmental file before running docker-compose
env_file_path=~/env.txt
service_dir=$(dirname $(readlink -f "$0"))
echo "Service directory $service_dir"

# TODO For some reason, this path is able to be checked properly.
# firebase_key_path="$service_dir/openapi_server/keys/firebase_auth_key.json"

# # Check if the file exists
# if [ ! -f "$file_path" ]; then
#     echo "Warning: File $firebase_key_path does not exist. Create a 'keys' folder under /openapi_server and move your key into that folder."
#     exit 1
# fi

# # Check if the file exists
# if [ ! -f "$env_file_path" ]; then
#     echo "Warning: File $env_file_path does not exist."
#     echo "Create environmental variable file prior to running container"
#     exit 1
# fi

# Navigate to the correct directory
cd "service_dir"

clear 

# Kill all containers, build, and deploy.
docker-compose down --remove-orphans
docker-compose build
docker-compose up