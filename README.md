# sensorflux
Service relay for sensors to influxdb

## How to start

To set everything up, from this directory:

1. Create a new virtual environment with `pyenv virtualenv <python_version> <environment_name>`
2. Activate the virtual environment with `source <environment_name>/bin/activate` 
3. Install the requirements with `pip install -r requirements_dev.txt`
4. Install the package with `pip install -e .`
5. Install the git pre-commit hook with `pre-commit install`
6. Launch the backend by following the instructions from [./docker/sensorflux-backend/README.md](./docker/sensorflux-backend/README.md)

## Development

- The primary development stream is on the main branch
- Development takes place on `feature` or `fix` branches
- Naming convention for branches is `feature/name_of_branch` and `fix/underscore_between_words`
- You can manually test all the files with pre-commit using the command `pre-commit run --all-files` (remove the flag to only test staged files)