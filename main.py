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
    auth = HTTPBasicAuth(RECURLY_API_KEY, '')
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(RECURLY_COUPON_ENDPOINT, auth=auth, headers=headers)
        if response.status_code == 200:
            promo_code = response.json().get("unique_code", {}).get("code", "nfldraft25")
        else:
            print(f"ERROR in main: Failed promo code fetch (get-code): Status {response.status_code}")
            promo_code = "nfldraft25"
    except Exception as e:
        print(f"ERROR in main: Exception fetching promo code (get-code): {e}")
        promo_code = "nfldraft25"
    return jsonify({"coupon_code": promo_code})

@app.route('/redirect', methods=['GET'])
def redirect_user():
    if request.args.get("utm_campaign") == "winback":
        auth = HTTPBasicAuth(RECURLY_API_KEY, '')
        headers = {"Accept": "application/json"}
        try:
            response = requests.get(RECURLY_COUPON_ENDPOINT, auth=auth, headers=headers)
            if response.status_code == 200:
                promo_code = response.json().get("unique_code", {}).get("code", "nfldraft25")
            else:
                print(f"ERROR in main: Failed promo code fetch (redirect): Status {response.status_code}")
                promo_code = "nfldraft25"
        except Exception as e:
            print(f"ERROR in main: Error fetching promo code during redirect: {e}, falling back to nfldraft25")
            promo_code = "nfldraft25"

        redirect_url = f"{SUBSCRIBE_URL}?promoCode={promo_code}"
        return redirect(redirect_url, code=302)

    return redirect(SUBSCRIBE_URL, code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
