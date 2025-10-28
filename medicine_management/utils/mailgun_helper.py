# import requests
# from django.conf import settings

# def send_mailgun_email(to_email, subject, message, is_html=True):
#     data = {
#         "from": f"MediAlert <mailgun@{settings.MAILGUN_DOMAIN}>",
#         "to": [to_email],
#         "subject": subject,
#     }
#     if is_html:
#         data["html"] = message
#     else:
#         data["text"] = message

#     try:
#         response = requests.post(
#             f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
#             auth=("api", settings.MAILGUN_API_KEY),
#             data=data,
#         )
#         response.raise_for_status() 
#         return response
#     except requests.RequestException as e:
#         raise e



import requests
from django.conf import settings

def send_medicine_email(subject, message=None, recipient_email=None, html_message=None):
    """
    Send an email via Mailgun with support for both plain text and HTML content.
    """
    url = f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages"
    auth = ("api", settings.MAILGUN_API_KEY)

    data = {
        "from": settings.MAILGUN_FROM_EMAIL,
        "to": recipient_email,
        "subject": subject,
    }

    if message:
        data["text"] = message
    else:
        data["text"] = "Please view this email in HTML format."

    if html_message:
        data["html"] = html_message

    response = requests.post(url, auth=auth, data=data)
    print("Mailgun response:", response.status_code, response.text)
    return response
