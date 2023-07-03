from flask import Flask, request, render_template
import generate_sitemap
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import threading

app = Flask(__name__)


def send_sitemap(url, email):
 # Generate sitemap
        sitemap = generate_sitemap.build_sitemap(url)

        # Save sitemap
        with open('sitemap.xml', 'wb') as f:
            f.write(sitemap)

        # Send email
        msg = MIMEMultipart()
        msg['From'] = 'myemail@gmail.com'
        msg['To'] = email
        msg['Subject'] = 'Your Sitemap for '+url

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open('sitemap.xml', 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="sitemap.xml"')
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        text = msg.as_string()
        server.sendmail('your_email@gmail.com', email, text)
        server.quit()

        os.remove('sitemap.xml')  # Delete the sitemap file

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        email = request.form['email']

        # Start background thread
        thread = threading.Thread(target=send_sitemap, args=(url, email))
        thread.start()

        return 'Sitemap generation started. It will be sent to your email when complete.'

    return render_template('index.html')  # a form for URL and email input

if __name__ == '__main__':
    app.run(debug=True)
