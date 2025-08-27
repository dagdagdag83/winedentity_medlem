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

    With the virtual environment activated, install the required packages using `uv`:

    ```bash
    uv pip install -r requirements.txt
    ```

## Running the Application

1.  **Set Google Cloud Credentials:**

    This application requires Google Cloud credentials to connect to Firestore. You need to set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account key file.

    *   **Linux/macOS:**
        ```bash
        export GOOGLE_APPLICATION_CREDENTIALS="/local_key.json"
        ```

    *   **Windows (PowerShell):**
        ```powershell
        $env:GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/local_key.json"
        ```

    Replace `/path/to/your/local_key.json` with the actual path to your key file.

2.  **Run the Flask app:**

    With the virtual environment activated and the environment variable set, you can run the application:

    ```bash
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000`.
