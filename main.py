import os
import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

RECURLY_API_KEY = os.getenv("RECURLY_API_KEY")
RECURLY_COUPON_ENDPOINT = os.getenv("RECURLY_COUPON_ENDPOINT")
SUBSCRIBE_URL = "https://subscribe.pff.com/"  # Destination

@app.route('/get-code', methods=['GET'])
def get_promo_code():
    try:
        response = requests.get(
            RECURLY_COUPON_ENDPOINT,
            auth=HTTPBasicAuth(RECURLY_API_KEY, '')
        )
        response.raise_for_status()
        promo_code = response.json().get("unique_code", {}).get("code", "nfldraft25")
    except Exception as e:
        print(f"Error fetching promo code in /get-code: {e}")
        promo_code = "nfldraft25"

    return jsonify({"coupon_code": promo_code})

@app.route('/redirect', methods=['GET'])
def redirect_user():
    if request.args.get("utm_campaign") == "winback":
        try:
            response = requests.get(
                RECURLY_COUPON_ENDPOINT,
                auth=HTTPBasicAuth(RECURLY_API_KEY, '')
            )
            response.raise_for_status()
            promo_code = response.json().get("unique_code", {}).get("code", "nfldraft25")
        except Exception as e:
            print(f"Error fetching promo code during redirect: {e}, falling back to nfldraft25")
            promo_code = "nfldraft25"

        redirect_url = f"{SUBSCRIBE_URL}?promoCode={promo_code}"
        return redirect(redirect_url, code=302)

    # If utm_campaign is not winback, just redirect to subscribe.pff.com
    return redirect(SUBSCRIBE_URL, code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
