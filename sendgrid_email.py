import os
import argparse
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Cc
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv

def send_email(sendgrid_api_key: str, mail_from:str, email_to: tuple, email_cc: tuple, subject: str,
               email_body: str, content_type: str = 'text/html') -> int:
    """
    send email using sendgrid and python
    sendgrid api key --> for auth
    mail_from --> sender email id
    email_to  --> email receiver
    email_cc --> email receivers as cc'd
    subject --> email subject
    email_body --> email body
    content_type --> email content type (text/html)
    
    returns status code
    """
    
    from_email = Email(mail_from)  # Change to your verified sender
    print(f"Mail is being send from {mail_from}")

    # setting up to mail ids
    to_email = []
    for to in email_to:
        to_email.append(To(to))

    # setting up cc mail ids
    cc_mails = []
    for to in email_cc:
        cc_mails.append(Cc(to))

    content = Content(content_type, email_body)    
    mail = Mail(from_email, to_email, subject, content)
    mail.add_cc(cc_mails)
    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    
    try:
        sg = sendgrid.SendGridAPIClient(sendgrid_api_key)
        response = sg.client.mail.send.post(request_body=mail_json)
    except Exception as err:
        print(f"Error: {err}")
        print(f"{'*** ' * 10}")
        print(f"Recipients are: to={';'.join(email_to)}, cc={';'.join(email_cc)}")

        raise err
    
    print(f"Response code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response body: {response.body}")
    
    return response.status_code
        
    
def main():
    """Run the code"""
    load_dotenv()
    parser = argparse.ArgumentParser("Send emails using python and sendgrid")
    parser.add_argument("--recepient", required=True, type=str, help="recepients of email")
    parser.add_argument("--cced", required=False, type=str, help="cc of email")
    parser.add_argument("--subject", required=True, type=str, help="subject of email")
    parser.add_argument("--email_body",required=True, type=str, help="body of email" )


    api_key = os.environ['SENDGRID_API_KEY']

    args = parser.parse_args()

    recepients = args.recepient
    cceds = args.cced
    subject = args.subject
    email_body = args.email_body


    recepient = recepients.split(",")
    cced = cceds.split(",") if cceds else []
    # subject = os.environ['subject']
    # email_body = os.environ['email_body']

    send_email(sendgrid_api_key=api_key,
               email_body=email_body, subject=subject,
               email_cc=(cced), email_to=(recepient),
               mail_from='krishnadhas@devwithkrishna.in')
    

if __name__ == "__main__":
    main()
