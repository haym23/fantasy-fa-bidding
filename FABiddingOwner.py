import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import base64
import datetime
from Tkinter import *

# Make pop up when bid is successfully placed
# Change email address to bowman
# Add stuff with timestamp

fields = 'Owner Name', 'Player Name', 'Salary', '# of Years'
TEXT_FILE = 'faBid.txt'
USERNAME = 'officialfantasyemail@gmail.com'
PASSWORD = 'Fantasy2017'

def send_mail(send_from, send_to, fileName, u, p):
    emailfrom = send_from
    emailto = send_to
    fileToSend = fileName
    username = u
    password = p

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Free agent bid"
    msg.preamble = "Hello comissioner bowman, I have a bid for you"
    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()

    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()

    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()

    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)

    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
        
def condense(bidFields):
    code = ''
    for field in bidFields:
        code = code + str(field)
    code += '|'
    return code

def encode(clear, key):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc))

def decode(enc, key):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def textFile(text):
    f = open(TEXT_FILE, 'w')
    f.write(text)
    f.close()

def fetch(entries):
    orig = ''
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        orig += condense(text)
    orig += '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    textFile(decode(encode(orig, 'key'), 'key'))
    #send_mail(USERNAME, 'haym23@yahoo.com', TEXT_FILE, USERNAME, PASSWORD)
    print "Successfully sent email to file"
    

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

if __name__ == '__main__':
   root = Tk()
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
   b1 = Button(root, text='Submit',
          command=(lambda e=ents: fetch(e)))
   b1.pack(side=LEFT, padx=5, pady=5)
   b2 = Button(root, text='Quit', command=root.quit)
   b2.pack(side=LEFT, padx=5, pady=5)
   root.mainloop()

