import imaplib
import email
import os
from email.header import decode_header

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)
 
def obtain_header(msg):
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding)
    From, encoding = decode_header(msg.get("From"))[0]
    if isinstance(From, bytes):
        From = From.decode(encoding)
    return subject, From
 
def download_attachment(part,subject):
    filename = part.get_filename()
    if filename:
        folder_name = clean(subject)
        folder_name = os.path.join("attachment",folder_name)
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
            filepath = os.path.join(folder_name, filename)
            open(filepath, "wb").write(part.get_payload(decode=True))

def Outlook_Reader(username,password,types):
    m = imaplib.IMAP4_SSL("imap-mail.outlook.com")
    m.login(username,password)
    m.select(mailbox = 'Inbox', readonly = False)
    
    result, data = m.search( None, types)
    if result == 'OK':
        for num in data[0].split():
            result, data = m.fetch(num, '(RFC822)')
            resp, uid = m.fetch(num, "(UID)")
            if result == 'OK':
                email_message = email.message_from_bytes(data[0][-1]) 
                subject, From = obtain_header(email_message)
                if email_message.is_multipart():
                    for part in email_message.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            mail_data = {
                                "Subject":subject,
                                "From" :From,
                                "Body" :body,
                                "UID" : uid
                                }
                        elif "attachment" in content_disposition:
                            download_attachment(part,subject)
                else:
                    content_type = email_message.get_content_type()
                    body = email_message.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        mail_data={
                            "Subject":subject,
                            "From" :From,
                            "Body" :body,
                            "UID" : uid
                            }
                return mail_data
    m.close()
    m.logout()
    