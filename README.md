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
    uv pip install -e .
    ```

## Running the Application

1.  **Set Environment Variables:**

    This application requires several environment variables to be set. You can create a `.env` file in the project root and add the following:

    ```bash
    # For local development with a mock database
    ENV="local"
    
    # For connecting to Google Cloud Firestore
    # GOOGLE_APPLICATION_CREDENTIALS="local_key.json"

    # Flask session secret key
    FLASK_SESSION_SECRET_KEY="a_secure_random_string"

    # reCAPTCHA keys
    RECAPTCHA_SITE_KEY="your_recaptcha_site_key"
    RECAPTCHA_SECRET_KEY="your_recaptcha_secret_key"
    ```
    
    **Note:** For local development, setting `ENV="local"` will use a mock database. If you want to use Google Cloud Firestore, you'll need to provide the `GOOGLE_APPLICATION_CREDENTIALS`.

2.  **Run the Flask app:**

    With the virtual environment activated and the environment variables set, you can run the application:

    ```powershell
    $env:FLASK_APP="winedentity"
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000`.
