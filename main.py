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
        headers = {"Accept": "application/json"}
        response = requests.get(
            RECURLY_COUPON_ENDPOINT,
            auth=HTTPBasicAuth(RECURLY_API_KEY, ''),
            headers=headers
        )

        if response.status_code == 200:
            promo_code = response.json().get("unique_code", {}).get("code", "nfldraft25")
        else:
            app.logger.error(f"Failed to fetch promo code: Status {response.status_code}")
            promo_code = "nfldraft25"

        return jsonify({"coupon_code": promo_code})

    except Exception as e:
        app.logger.error(f"Exception in get-code: {str(e)}")
        return jsonify({"coupon_code": "nfldraft25"})

@app.route('/redirect', methods=['GET'])
def redirect_user():
    try:
        if request.args.get("utm_campaign") == "winback":
            headers = {"Accept": "application/json"}
            response = requests.get(
                RECURLY_COUPON_ENDPOINT,
                auth=HTTPBasicAuth(RECURLY_API_KEY, ''),
                headers=headers
            )

            if response.status_code == 200:
                promo_code = response.json().get("unique_code", {}).get("code", "nfldraft25")
            else:
                app.logger.error(f"Failed promo code fetch (redirect): Status {response.status_code}")
                promo_code = "nfldraft25"

            redirect_url = f"{SUBSCRIBE_URL}?promoCode={promo_code}"
            return redirect(redirect_url, code=302)

        return redirect(SUBSCRIBE_URL, code=302)

    except Exception as e:
        app.logger.error(f"Error fetching promo code during redirect: {str(e)}, falling back to nfldraft25")
        return redirect(f"{SUBSCRIBE_URL}?promoCode=nfldraft25", code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
