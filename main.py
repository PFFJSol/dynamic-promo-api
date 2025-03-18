import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Retrieve API Key securely from Cloud Run environment variables
RECURLY_API_KEY = os.getenv("RECURLY_API_KEY")
RECURLY_COUPON_ENDPOINT = os.getenv("RECURLY_COUPON_ENDPOINT")

@app.route('/get-code', methods=['GET'])
def get_promo_code():
    headers = {"Authorization": f"Bearer {RECURLY_API_KEY}"}
    response = requests.get(RECURLY_COUPON_ENDPOINT, headers=headers)

    if response.status_code == 200:
        promo_code = response.json().get("unique_code", {}).get("code", "nfldraft25")
    else:
        promo_code = "nfldraft25"  # Default fallback promo code

    return jsonify({"coupon_code": promo_code})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))