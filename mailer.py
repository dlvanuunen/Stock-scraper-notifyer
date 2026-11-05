import smtplib
from email.message import EmailMessage

from config import SMTP_HOST, SMTP_PORT, EMAIL_ADDRESS, PASSWORD, RECIPIENT, SUBJECT


msg = EmailMessage()
msg["From"] = EMAIL_ADDRESS
msg["To"] = RECIPIENT
msg["Subject"] = SUBJECT


def send_mail(message_body):
    # stock_info = format_stock_info(collected_info)
    msg.set_content(message_body, subtype='html')
    try:
        # Testing implicit SSL on port 465
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, PASSWORD)
            server.send_message(msg)

        print("Email sent successfully!")

    except Exception as err:
        print(f"Error: {type(err).__name__} - {err}")


def send_mail_test():
    msg.set_content("Authentication check")
    try:
        # Testing implicit SSL on port 465
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, PASSWORD)
            server.send_message(msg)

        print("Email sent successfully!")

    except Exception as err:
        print(f"Error: {type(err).__name__} - {err}")



if __name__ == "__main__":

    send_mail_test()
