FROM python:3.14.0-slim AS install

# Install poetry to read a pyproject.toml
RUN python3 -m pip install "poetry==2.2.1"
RUN python3 -m poetry self add poetry-plugin-export

# Add pyproject.toml to read from
ADD pyproject.toml poetry.lock ./

# Install the poetry dependencies via pip
RUN python3 -m poetry export --with kcomp -o requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Reset all the build image files
FROM python:3.14.0-slim

# Transfer configured Python installation
COPY --from=install /usr/local /usr/local

# Uninstall poetry and its plugin
RUN python3 -m pip uninstall poetry poetry-plugin-export -y