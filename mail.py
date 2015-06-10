from subprocess import Popen,PIPE
from email import message_from_string
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

@app.route('/mail')
def mail():
  mail=''
  nb=0
  subject=''
  user = "test@gmail.com"
  password = "test"
  M = imaplib.IMAP4_SSL("imap.gmail.com", 993)
  M.login(user, password)
  try:
    M.select()
    typ, data = M.search(None, '(UNSEEN)')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        msg = message_from_string(str(data[0][1]))
        subject=msg['Subject']
        mail = msg['From'].split("<")[1].split(">")[0].strip()
  except Exception, e:
    print "[Exception] "+str(e)
  finally :
    nb=str(len(data[0]))
    M.close()
    M.logout()
    return '{ "from":"'+mail+'", "subject":"'+subject+'", "number":"'+nb+'"}'

