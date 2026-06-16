from flask import Flask, request, jsonify
from cipher.ecc_cipher import ECCCipher

app = Flask(__name__)

ecc_cipher = ECCCipher()


@app.route("/api/ecc/generate_keys", methods=["GET"])
def generate_keys():
    result = ecc_cipher.generate_keys()
    return jsonify({
        "message": result
    })


@app.route("/api/ecc/sign", methods=["POST"])
def sign():
    data = request.get_json()

    message = data.get("message")

    if not message:
        return jsonify({
            "error": "Message is required"
        }), 400

    signature = ecc_cipher.sign(message)

    return jsonify({
        "message": message,
        "signature": signature
    })


@app.route("/api/ecc/verify", methods=["POST"])
def verify():
    data = request.get_json()

    message = data.get("message")
    signature = data.get("signature")

    if not message or not signature:
        return jsonify({
            "error": "Message and signature are required"
        }), 400

    result = ecc_cipher.verify(message, signature)

    return jsonify({
        "message": message,
        "signature": signature,
        "is_verified": result
    })


if __name__ == "__main__":
    app.run(debug=True)