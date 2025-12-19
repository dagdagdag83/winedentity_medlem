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

# QR Code Generation
import qrcode
import qrcode.image.svg
import io
import base64

def generate_vinmonopolet_qr(product_id):
    """Generates a base64 encoded SVG QR code for a Vinmonopolet product."""
    if not product_id:
        return ""
        
    url = f"https://www.vinmonopolet.no/p/{product_id}"
    
    # Configure QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Generate SVG image
    # Using SvgPathImage as requested for clean path-based SVG
    factory = qrcode.image.svg.SvgPathImage
    img = qr.make_image(image_factory=factory)
    
    buffer = io.BytesIO()
    img.save(buffer)
    svg_data = buffer.getvalue().decode("utf-8")
    
    # Inject brand color
    # The SVG output by qrcode has fill="#000000". We replace it.
    fill_color = "#320b35" 
    if 'fill="#000000"' in svg_data:
        svg_data = svg_data.replace('fill="#000000"', f'fill="{fill_color}"')
    else:
        # Fallback if the format changes, try to inject style which might override
        svg_data = svg_data.replace('<path', f'<path fill="{fill_color}"')
    
    # Encode as base64 for data URI usage in <img> tag
    img_str = base64.b64encode(svg_data.encode("utf-8")).decode("utf-8")
    
    return f"data:image/svg+xml;base64,{img_str}"
