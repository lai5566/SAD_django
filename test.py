import requests

def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox8c230178e8bf4c6f82e7cb134df694dc.mailgun.org/messages",
        auth=("api", "pubkey-48dc11f3be8755f73f4c0a41befd2bf0"),  # 替換為您的 Mailgun API 金鑰
        data={
            "from": "Excited User <mailgun@sandbox8c230178e8bf4c6f82e7cb134df694dc.mailgun.org>",
            "to": ["lai27418@gmail.com"],  # 收件者
            "subject": "Hello",  # 郵件主題
            "text": "Testing some Mailgun awesomeness!"  # 郵件內容
        })

if __name__ == "__main__":
    response = send_simple_message()
    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Status code: {response.status_code}")
        print(f"Response: {response.text}")
