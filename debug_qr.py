import qrcode
import qrcode.image.svg
import io
import base64

def generate_debug_qr():
    url = "https://www.vinmonopolet.no/p/12345"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    factory = qrcode.image.svg.SvgPathImage
    img = qr.make_image(image_factory=factory)
    
    buffer = io.BytesIO()
    img.save(buffer)
    svg_bytes = buffer.getvalue()
    svg_data = svg_bytes.decode("utf-8")
    
    print("--- ORIGINAL SVG START ---")
    print(svg_data[:200]) # Print start
    print("...")
    print(svg_data[-100:]) # Print end
    print("--- ORIGINAL SVG END ---")
    
    fill_color = "#320b35"
    if '<path' in svg_data:
        print("Found <path tag, replacing...")
        svg_data_mod = svg_data.replace('<path', f'<path fill="{fill_color}"')
        print("--- MODIFIED SVG START ---")
        print(svg_data_mod[:200])
    else:
        print("DID NOT FIND <path tag!")
        svg_data_mod = svg_data
        print(svg_data)

    img_str = base64.b64encode(svg_data_mod.encode("utf-8")).decode("utf-8")
    print(f"\nBase64 string len: {len(img_str)}")
    print(f"Data URI: data:image/svg+xml;base64,{img_str[:50]}...")

if __name__ == "__main__":
    generate_debug_qr()
