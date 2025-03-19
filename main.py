import os
import requests
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

RECURLY_API_KEY = os.getenv("RECURLY_API_KEY")
RECURLY_COUPON_ENDPOINT = os.getenv("RECURLY_COUPON_ENDPOINT")
SUBSCRIBE_URL = "https://subscribe.pff.com/"  # Destination

@app.route('/get-code', methods=['GET'])
def get_promo_code():
    headers = {"Authorization": f"Bearer {RECURLY_API_KEY}"}
    response = requests.get(RECURLY_COUPON_ENDPOINT, headers=headers)

    app.logger.info(f"Recurly GET request status: {response.status_code}")
    app.logger.info(f"Recurly GET response body: {response.text}")

    if response.status_code == 200:
        promo_code = response.json().get("unique_code")
        if not promo_code:
            app.logger.warning("Unique promo code not found in response JSON. Falling back to nfldraft25.")
            promo_code = "nfldraft25"
    else:
        app.logger.error(f"Error fetching promo code, status: {response.status_code}. Falling back to nfldraft25.")
        promo_code = "nfldraft25"

    return jsonify({"coupon_code": promo_code})

@app.route('/redirect', methods=['GET'])
def redirect_user():
    if request.args.get("utm_campaign") == "winback":
        headers = {"Authorization": f"Bearer {RECURLY_API_KEY}"}
        response = requests.get(RECURLY_COUPON_ENDPOINT, headers=headers)

        app.logger.info(f"Redirect Recurly request status: {response.status_code}")
        app.logger.info(f"Redirect Recurly response body: {response.text}")

        if response.status_code == 200:
            promo_code = response.json().get("unique_code")
            if not promo_code:
                app.logger.warning("Unique promo code not found in response JSON during redirect. Using fallback.")
                promo_code = "nfldraft25"
        else:
            app.logger.error(f"Error fetching promo code during redirect, falling back to nfldraft25.")
            promo_code = "nfldraft25"

        redirect_url = f"{SUBSCRIBE_URL}?promoCode={promo_code}"
        return redirect(redirect_url, code=302)

    return redirect(SUBSCRIBE_URL, code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
