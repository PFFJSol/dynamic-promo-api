import os
import requests
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

RECURLY_API_KEY = os.getenv("RECURLY_API_KEY")
RECURLY_COUPON_ENDPOINT = os.getenv("RECURLY_COUPON_ENDPOINT")
SUBSCRIBE_URL = "https://subscribe.pff.com/"  # Destination


def fetch_promo_code():
    headers = {
        "Accept": "application/xml",
    }
    response = requests.get(RECURLY_COUPON_ENDPOINT, auth=(RECURLY_API_KEY, ''), headers=headers)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.content)
            first_coupon_code = root.find('.//coupon_code').text
            return first_coupon_code or "nfldraft25"
        except Exception as e:
            app.logger.error(f"Error parsing XML response: {e}")
            return "nfldraft25"
    else:
        app.logger.error(f"Failed promo code fetch: Status {response.status_code}")
        return "nfldraft25"


@app.route('/get-code', methods=['GET'])
def get_promo_code():
    promo_code = fetch_promo_code()
    return jsonify({"coupon_code": promo_code})


@app.route('/redirect', methods=['GET'])
def redirect_user():
    if request.args.get("utm_campaign") == "winback":
        promo_code = fetch_promo_code()
        redirect_url = f"{SUBSCRIBE_URL}?promoCode={promo_code}"
        return redirect(redirect_url, code=302)
    else:
        return redirect(SUBSCRIBE_URL, code=302)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
