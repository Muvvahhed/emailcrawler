import imaplib
import email
import yaml
import pandas as pd
with open('credentials.yml') as f:
    content = f.read()

my_credentials = yaml.load(content, Loader=yaml.FullLoader)
user, password = my_credentials["user"], my_credentials["password"]

imap_url = "imap.gmail.com"

my_mail = imaplib.IMAP4_SSL(imap_url)

my_mail.login(user, password)

my_mail.select('Inbox')

key = "FROM"
value = "mustyk2.mk@gmail.com"

_, data = my_mail.search(None, key, value)
mail_id_list = data[0].split()
print(mail_id_list)

msgs = []

for num in mail_id_list:
    typ, data = my_mail.fetch(num, '(RFC822)')
    msgs.append(data)

emails = []
for msgs in msgs[::-1]:
    for response_part in msgs:
        if type(response_part) is tuple:
            my_msg = email.message_from_bytes((response_part[1]))
            print("---------------------------------------------")
            print("subj:", my_msg["subject"])
            print("from:", my_msg["from"])
            print("body:")
            my_email = {
                "subj:": my_msg["subject"],
                "from:": my_msg["from"]
            }
            for part in my_msg.walk():
                if part.get_content_type() == "text/plain":
                    my_email["body"] = part.get_payload()
                    print(part.get_payload())
            emails.append(my_email)
print(emails)

df = pd.DataFrame(emails)
df.to_csv("emails.csv")
