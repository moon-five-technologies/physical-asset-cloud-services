## Physical Asset Information Application Interface
An OpenAPI generated server 

## Setup
1. Get a firebase admin sdk private key, this can be retrieved either via this link (https://console.firebase.google.com/u/0/project/fir-mft-charge/settings/serviceaccounts/adminsdk) and clicking `Generate New Private Key` or from an admin who has access to the firebase console. 
2. Move this file to the `/openapi_server/keys` folder under the name `firebase_auth_key.json`.  This folder is included in the .gitignore, so you won't have to worry about adding keys accidentally to github.
3. Set environmental variables POSTGRESQL_PASSWORD, TMP_API_SECRET_KEY that can be accessed within the docker-compose container. This can be done by creating a file `~/env.txt`, which houses this information with every new line looking like `VARIABLE_NAME=VALUE`.  
4. Ensure that no one else can view this file by running `chmod 700 ~/env.txt`.
5. Install docker and docker-compose.

## Run a local instance
1. Run `chmod +x local_instance.sh` to give the shell script execution privileges.
2. Then execute the shell script by typing `./local_instance.sh`. This shell script checks that the required files are in the proper place before tearing down any containers that are already running, building your current container, and then deploying via `docker-compose up`.
3. Navigate to `http://localhost/api/v1/ui/` to view your swagger instance.
3. You can use `Control + C` to stop the local instance.
