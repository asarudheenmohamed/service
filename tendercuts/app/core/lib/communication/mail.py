import smtplib
from django.conf import settings
from os.path import basename

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate



class Mail:
    def send(self, sender, receivers, subject, message, files=None):
        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo() # extra characters to permit edit

            smtpObj.login(
                settings.MAIL_GATEWAY['TC_USER'],
                settings.MAIL_GATEWAY['TC_PASS'])

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = COMMASPACE.join(receivers)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = subject
            msg.attach(MIMEText(message))
            for f in files or []:
                with open(f, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(f)
                    )
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                    msg.attach(part)


            smtpObj.sendmail(sender, receivers, msg.as_string())
            print "Successfully sent email"

        except smtplib.SMTPException as e:
            raise e
