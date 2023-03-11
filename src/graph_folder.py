import imaplib, getpass, re
import src.graph_data
pattern_uid = re.compile(r'\d+ \(UID (?P<uid>\d+)\)')

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

def connect(email,password):
    imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")
    imap.login(email, password)
    return imap

def disconnect(imap):
    imap.logout()

def parse_uid(data):
    match = pattern_uid.match(data)
    return match.group('uid')

# Create Folder on outlook for Body-wise Classification
def Create_Folder_For_Body(label,username,password):
  IMAP = "imap-mail.outlook.com"
  imap = imaplib.IMAP4_SSL(IMAP)
  imap.login(username, password)
  folder = "Classification_On_Body/{}".format(clean(label))
  imap.create(folder)



#Check Folder on outlook for Body-Wise Classification
def FolderChecker_For_Body(label,username,password):
    IMAP = "imap-mail.outlook.com"
    mail = imaplib.IMAP4_SSL(IMAP)
    mail.login(username, password)
    for i in mail.list()[1]:
        l = i.decode().split(' "/" ')
        match = "Classification_On_Body"+"/"+clean(label)
        if str(l[1])==str(match):
            return True
    return False



#Move Folder on outlook for Body-Wise Classification
def Move_Items_For_Body(uid,label,username,password):
  imap = connect(username,password)
  imap.select(mailbox = 'Inbox', readonly = False)
  msg_uid = parse_uid(uid[0].decode('utf-8'))
  destination_folder ="Classification_On_Body" + "/" + clean(label)
  result = imap.uid('COPY', msg_uid, destination_folder)
  if result[0] == 'OK':
    print("DONE")
    mov, data = imap.uid('STORE', msg_uid , '+FLAGS')
  disconnect(imap)