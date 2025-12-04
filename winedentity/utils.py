import os
import logging
import requests

def verify_recaptcha(token, secret_key):
    """Verifies the reCAPTCHA token with Google."""
    if not secret_key:
        logging.warning("RECAPTCHA_SECRET_KEY is not set. Skipping verification.")
        return True, 0.9  # Assume success for local development if not set

    try:
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': secret_key,
                'response': token
            }
        )
        result = response.json()
        logging.debug(f"reCAPTCHA verification result: {result}")

        if result.get('success') and result.get('score', 0.0) >= 0.5:
            return True, result.get('score')
        else:
            return False, result.get('score')
    except Exception as e:
        logging.error(f"Error verifying reCAPTCHA: {e}")
        return False, 0.0
