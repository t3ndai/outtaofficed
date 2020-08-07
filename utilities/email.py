import httpx
from settings import MAILGUN_API_KEY


def send_mail(sender, to, msg, topic):
    return httpx.post(
        "https://api.mailgun.net/v3/outtaoffice.work/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": sender, "to": to, "text": msg, "subject": topic,},
    )

