import random
import string

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def get_random_string(length):
    # TODO check if this code is already used
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


def generate_temporary_password(length=8):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str

def send_email(email, obj, msg, link):
    message = Mail(
        from_email='***************',
        to_emails=email,
        subject=obj,
        html_content='<div>{}<a href="{}">Reset Password</a></div>'.format(msg, link))
    try:
        sg = SendGridAPIClient(
            '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')
        response = sg.send(message)
        print(response.status_code, flush=True)
        print(response.body, flush=True)
        print(response.headers, flush=True)
    except Exception as e:
        print(e.message, flush=True)
