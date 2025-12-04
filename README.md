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
        export GOOGLE_APPLICATION_CREDENTIALS="local_key.json"
        ```

    *   **Windows (PowerShell):**
        ```powershell
        $env:GOOGLE_APPLICATION_CREDENTIALS="local_key.json"
        ```

    Replace `/path/to/your/local_key.json` with the actual path to your key file.

2.  **Run the Flask app:**

    You can run the application in two modes: **Local** (path-based routing) or **Production** (domain-based routing).

    ### Local Mode (Recommended for Development)

    Set `ENV=LOCAL` to enable path-based routing:
    - Homepage: `http://localhost:8080/`
    - Registration: `http://localhost:8080/reg`

    *   **Linux/macOS:**
        ```bash
        export ENV=LOCAL
        uv run flask run --host=0.0.0.0 --port=8080
        ```
    *   **Windows (PowerShell):**
        ```powershell
        $env:ENV="LOCAL"
        uv run flask run --host=0.0.0.0 --port=8080
        ```

    ### Production Mode

    If `ENV` is not set to `LOCAL`, the app uses domain-based routing:
    - `winedentity.org` -> Homepage
    - `reg.winedentity.org` -> Registration Form
    - Other domains -> 404 Not Found

    To run in this mode locally (requires modifying `hosts` file):
    ```bash
    uv run flask run --host=0.0.0.0 --port=8080
    ```

## Testing

To run the verification suite:

```bash
uv run python tests.py
```
