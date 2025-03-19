import os
import requests
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

RECURY_API_KEY = os.getenv("RECURY_API_KEY")
RECURY_COUPON_ENDPOINT = os.getenv("RECURY_COUPON_ENDPOINT")
SUBSCRIBE_URL = "https://subscribe.pff.com/"  # Destination

@app.route('/get-code', methods=['GET'])
def get_promo_code():
    headers = {"Authorization": f"Bearer {RECURY_API_KEY}"}
    response = requests.get(RECURY_COUPON_ENDPOINT, headers=headers)
    if response.status_code == 200:
        promo_code = response.json().get("unique_code", {}).get("code", "nfldraft25")
    else:
        promo_code = "nfldraft25"
    return jsonify({"coupon_code": promo_code})

@app.route('/redirect', methods=['GET'])
def redirect_user():
    # Optional: Check for utm_campaign=winback
    if request.args.get("utm_campaign") == "winback":
        headers = {"Authorization": f"Bearer {RECURY_API_KEY}"}
        response = requests.get(RECURY_COUPON_ENDPOINT, headers=headers)
        if response.status_code == 200:
            promo_code = response.json().get("unique_code", {}).get("code", "nfldraft25")
        else:
            promo_code = "nfldraft25"
        # Redirect with promoCode in query
        redirect_url = f"{SUBSCRIBE_URL}?promoCode={promo_code}"
        return redirect(redirect_url, code=302)
    # If utm_campaign is not winback, just redirect to subscribe.pff.com
    return redirect(SUBSCRIBE_URL, code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
