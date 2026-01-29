# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy the project configuration
COPY pyproject.toml uv.lock ./

# Sync the project's dependencies
# We use --frozen to ensure exact versions from uv.lock
RUN uv sync --frozen --no-install-project

# Copy the rest of the application
COPY . .

# Install the project itself
RUN uv sync --frozen

# Default command
CMD ["uv", "run", "start"]
