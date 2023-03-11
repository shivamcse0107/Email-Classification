import imaplib

def Create_Folder(username,password):
  IMAP = "imap-mail.outlook.com"
  imap = imaplib.IMAP4_SSL(IMAP)
  imap.login(username, password)
  folder1 = "Classification_On_Subject"
  folder2 = "Classification_On_Body"
  folder3 = "Classification_On_SubjectBody"
  imap.create(folder1)
  imap.create(folder2)
  imap.create(folder3)

if __name__ =="__main__":
    username="shivam17818@outlook.com"
    password ="Shivam@17818"
    Create_Folder(username,password)