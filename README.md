## Physical Asset Information Application Interface
### OpenAPI generated server
### Moon Five Technologies Inc 

## Setup
1. Retrieve the firebase admin sdk private key, add this file to the `/openapi_server/keys` folder under the name `firebase_auth_key.json`.
2. Set environmental variables POSTGRESQL_PASSWORD, TMP_API_SECRET_KEY that can be accessed within the docker-compose container. This can be done by creating a file `~/env.txt`, which houses this information with every new line looking like `VARIABLE_NAME=VALUE`.  
3. Ensure that no one else can view this file by running `chmod 700 ~/env.txt`.
4. Install docker and docker-compose.

## Run a local instance
1. Run `chmod +x local_instance.sh` to give the shell script execution privileges.
2. Then execute the shell script by typing `./local_instance.sh`
3. Navigate to `http://localhost/api/v1/ui/` to view your swagger instance.
3. You can use `Control + C` to stop the local instance.
