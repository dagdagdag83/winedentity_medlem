# Flask App with Google Cloud Firestore

This is a simple Flask application that uses Google Cloud Firestore as a database. 

## Local Development Setup

### Prerequisites

*   Python 3.13
*   `uv` package manager

### Installation

1.  **Install `uv`:**

    If you don't have `uv` installed, you can install it with:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    For more installation options, see the [official `uv` documentation](https://docs.astral.sh/uv/getting-started/installation/).

2.  **Create a virtual environment:**

    It's recommended to use a virtual environment for development. Create one with `uv`:

    ```bash
    uv venv
    ```

    This will create a `.venv` directory in the project root.

3.  **Activate the virtual environment:**

    *   **Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows (PowerShell):**
        ```powershell
        .venv\Scripts\Activate.ps1
        ```

4.  **Install dependencies:**

    With the virtual environment activated, install the project in editable mode:

    ```bash
    uv pip install -e .
    ```
    This command reads the dependencies from `pyproject.toml` and installs them.

## Running the Application

The application can be run in two modes:

### 1. Local Development (with Mock Database)

For local development, you can use a mock in-memory database by setting the `ENV` environment variable. This avoids the need for Google Cloud credentials.

*   **Run the Flask app:**
    With the virtual environment activated, run the following command:

    ```bash
    ENV=local flask --app winedentity run
    ```

    The application will be available at `http://127.0.0.1:5000`.

### 2. Production Mode (with Google Cloud Firestore)

To run the application against the real Google Cloud Firestore database, you need to provide credentials.

*   **Set Google Cloud Credentials:**
    Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account key file.

    *   **Linux/macOS:**
        ```bash
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/local_key.json"
        ```

    *   **Windows (PowerShell):**
        ```powershell
        $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\local_key.json"
        ```

*   **Run the Flask app:**
    With the virtual environment activated and credentials set, run the application:

    ```bash
    flask --app winedentity run
    ```
