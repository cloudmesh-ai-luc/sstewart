If you have the following lines in your template:
MARIADB_PASSWORD=replace_with_a_local_password
MARIADB_ROOT_PASSWORD=replace_with_a_different_root_password

You must interrupt the program with an error message as you have not set the password.

The password must be set in the .env file. Make sure the env file is in ~/.config/911/env

Ask LLM to give you a 911 setup method that reads the config file from ~/.config/911/env

Figure out what you are going to place in repositories and can ask LLM what it should be called, if part of a service, it should be under the services folder

