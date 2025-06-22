# Recommendation Service Template

## Setup

### Python

This template uses Python 3.9, but you can use other versions if you prefer.
However, we don't guarantee that everything will work with other versions.

### Make

[Make](https://www.gnu.org/software/make/) is a very popular utility
designed for transforming files using a defined sequence of commands.
However, it can also be used to execute arbitrary command sequences.
These commands and rules are specified in the `Makefile`.

We will actively use `make` in this project, so we recommend getting familiar with it.

On macOS and \*nix systems, `make` is usually pre-installed or can be easily installed.
Some ways to install `make` on Windows are described [here](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows).

### Poetry

[Poetry](https://python-poetry.org/) is a handy tool for dependency management in Python.
We'll use it to set up the environment.

So before getting started, you should follow [the installation steps](https://python-poetry.org/docs/#installation).

## Virtual Environment

We'll work within a virtual environment created specifically for this project.
If you're unfamiliar with the concept of virtual environments in Python,
make sure to read [this tutorial](https://docs.python.org/3.8/tutorial/venv.html).
We recommend using a separate virtual environment for each of your projects.

### Environment Initialization

Run the command:

```
make setup
```

This will create a new virtual environment in the `.venv` folder.
It will install the packages listed in `pyproject.toml`.

Note: If you've already run `make setup` once, running it again will do nothing,
since its only dependency – the `.venv` directory – already exists.
If you need to rebuild the environment from scratch for any reason,
first run `make clean` to delete the old environment.

### Installing/Removing Packages

To install new packages, use `poetry add`; to remove them, use `poetry remove`.
We do not recommend manually editing the dependency section in `pyproject.toml`.

## Linters, Tests, and Autoformatting

### Autoformatting

Run:

```
make format
```

This will auto-format your code using [isort](https://github.com/PyCQA/isort)
(for sorting imports) and [black](https://github.com/psf/black),
one of the most popular formatters for Python.

### Static Code Checks

Run:

```
make lint
```

This will run linters – tools for static code analysis.
They help catch errors before the code is run and enforce the [PEP8](https://peps.python.org/pep-0008) style guide.
This includes the same tools `isort` and `black`, but in this case, they only check formatting without modifying code.

### Tests

Run:

```
make test
```

This will run tests using the [pytest](https://pytest.org/) tool.

## Running the Application

### Method 1: Python + Uvicorn

```
python main.py
```

This runs the app locally in a single process.
Default host and port: `127.0.0.1` and `8080`.
These can be changed using the `HOST` and `PORT` environment variables.

The process is managed by the lightweight [ASGI](https://asgi.readthedocs.io/en/latest/) server [uvicorn](https://www.uvicorn.org/).

Note: You must use the Python interpreter from the project's virtual environment.

### Method 2: Uvicorn

```
uvicorn main:app
```

This is very similar to the previous method but starts the app directly.
Host and port can be passed via command-line arguments.

Note: You must use the `uvicorn` from the project's environment.

### Method 3: Gunicorn

```
gunicorn main:app -c gunicorn.config.py
```

Similar to the previous method, but uses the more feature-rich server [gunicorn](https://gunicorn.org/)
(`uvicorn` is used internally). Parameters are specified via a config file,
and host/port can be set via environment variables or command-line arguments.

This launches the service with multiple parallel processes – by default, one per CPU core.

Note: You must use `gunicorn` from the project's environment.

### Method 4: Docker

Same as above, but inside a Docker container.
If you're not familiar with [Docker](https://www.docker.com/), it's worth learning.

Inside the container, you can use any of the above methods.
In production, it's recommended to use `gunicorn`.

To build and run the Docker image, use:

```
make run
```

## CI/CD

When you perform an action specified in the config, a CI (Continuous Integration) process is triggered.
What exactly happens and how it’s triggered is defined in special `.yaml`/`.yml` config files in the `.github/workflows` folder.

Currently, there’s only one config: `test.yml`, which creates a virtual environment,
runs linters and tests. If something goes wrong, the process fails, and a red cross appears in GitHub.
You should check the logs, fix the issue, and push the changes again.

This process is triggered when creating or updating a pull request, or when pushing to `master`.
