from application.workers import celery
from celery.schedules import crontab
from flask import render_template
from flask import current_app as app
from jinja2 import Template
from application.data_access import get_all_users, get_posts_author_desc, get_comments_post, get_user_username
from application.models import db, Post
from application.utils import create_analytics, create_pdf_report, zipdir, send_email, create_pdf, convert_to_webp
from application.config import UPLOAD_FOLDER
import csv, os, shutil, zipfile, smtplib
import datetime as dt
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.application import MIMEApplication
from email import encoders


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=13, minute=0), 
        reminder_email.s(), 
        name='add every day'
    )

    sender.add_periodic_task(
        crontab(hour=13, minute=0, day_of_month='1'), 
        send_report.s(), 
        name='add every month'
    )

@celery.task()
def importBlogs(f, author):
    directory = f[:-4]

    with zipfile.ZipFile(f, "r") as zip_ref:
        os.makedirs(directory)
        zip_ref.extractall(directory)
        os.remove(f)

    files = os.listdir(directory)
    txt_files = [f for f in files if os.path.splitext(f)[1] == ".txt"]
    image_files = [f for f in files if os.path.splitext(f)[1] in [".jpg", ".png", ".gif"]]

    for txt in txt_files:
        for img in image_files:
            if txt[:-4] in img:
                break
        
        last_post = Post.query.order_by(Post.roll.desc()).first()
        day = str(dt.datetime.now().day) if len(str(dt.datetime.now().day)) > 1 else "0" + str(dt.datetime.now().day)
        month = str(dt.datetime.now().month) if len(str(dt.datetime.now().month)) > 1 else "0" + str(dt.datetime.now().month)
        date = str(dt.datetime.now().year)+"-"+month+"-"+day
        filename = str(last_post.roll + 1)
        title = txt[:-4]

        with open(directory + "/" + txt, "r") as content:
            content = content.read()

        filepath = os.path.join(UPLOAD_FOLDER+"Posts/", filename +".webp")
        with open(filepath, 'wb') as f:
            f.write(convert_to_webp(directory + "/" + img))

        post = Post(author=author, img=filename, text=content, date=date, title=title, views=0, likes=0)

        db.session.add(post)
        db.session.commit()

    shutil.rmtree(directory)



@celery.task()
def reminder_email():
    template_str = """
    <p>
        Dear {{ user }},
    </p>
    <br />
    <p>
        I hope this email finds you well. I wanted to reach out to remind you that it's been a while since you last posted on our blog site. We appreciate your contributions and believe your voice adds value to our platform.
    </p>
    <p>
        We understand that life can get busy, but we encourage you to take a moment to share your thoughts and ideas with our community. Your unique perspective is important to us and to our readers.
    </p>
    <p>
        Thank you for being a part of our blogging community, and we look forward to seeing your next post.
    </p>
    <br />
    <p>
        Best regards,
    </p>
    <p>
        {{ your_name }}
        """
    users = get_all_users()
    template = Template(template_str)

    for user in users:
        user_dict = user.to_dict()
        if not user_dict["posted"] and user_dict["username"] != "[deleted]":
            address = user_dict["email"]
            subject = user_dict["username"] + ", a friendly reminder to contribute to Blog-Lite"
            rendered_template = template.render(user=user_dict["username"], your_name="Blog-Lite")

            send_email(address, subject, rendered_template)
            
            user.posted = 0
            db.session.commit()

        folder_path = "static/img/Analytics/" + user_dict["username"]

        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
            except OSError as e:
                pass


    return 200

@celery.task()
def export_csv(username):
    user_dict = get_user_username(username).to_dict()
    posts = get_posts_author_desc(username)

    with open("analytics.csv", "w", newline='') as f:
        f = csv.writer(f, delimiter=',')
        f.writerow(["Roll", "Author", "Title", "Text", "Date", "Image ID", "Views", "Comments", "Likes"])
        for post in posts:
            comments = len(get_comments_post(post.roll))
            f.writerow([post.roll, post.author, post.title, post.text, post.date, post.img, post.views, comments, post.likes])

    template_str = """
        <p>
            Dear {{ user }},
        </p>
        <br />
        <p>
            Thank you for using our website to post your blogs. We hope you are enjoying the experience so far.
        </p>
        <p>
            As requested, we have attached your blog posts analytics CSV file to this email. Please find it attached.
        </p>
        <p>
            If you have any questions or concerns about your analytics data, please don’t hesitate to reach out to us.
        </p>
        <br />
        <p>
            Best regards,
        </p>
        <p>
            Blog-Lite
        </p>
        """
    template = Template(template_str)

    address = user_dict["email"]
    subject = "Your Blog Posts Analytics CSV"
    message = template.render(user=user_dict["username"])

    file = open("analytics.csv", "rb")

    send_email(address, subject, message, attachment=file, filename="analytics.csv", subtype="csv")

    os.remove("analytics.csv")


@celery.task()
def send_report():
    users = get_all_users()

    for user in users:
        user = user.to_dict()
        if user["username"] != "[deleted]":
            SMTP_SERVER_HOST = "localhost"
            SMTP_SERVER_PORT = 1025
            SENDER_ADDRESS = "service@bloglite.com"
            SENDER_PASSWORD = ""
            msg = MIMEMultipart()
            msg["From"] = SENDER_ADDRESS
            msg["To"] = user["email"]
            msg["Subject"] = "Monthly Report"
            state = len(get_posts_author_desc(user["username"])) > 0
            if state:
                if user["pdf"] == 0:
                    template = render_template("analytics.html", user=user["username"], state=state)
                    
                    msg.attach(MIMEText(template, "html"))

                    if state:
                        images = ["Views.png", "Likes.png", "Comments.png"]

                        create_analytics(user["username"])

                        for image in images:
                            with open("static/img/Analytics/" + user["username"] + "/" + image, "rb") as fp:
                                img = MIMEImage(fp.read(), _subtype='png')
                            img.add_header('Content-ID', '<{}>'.format(image))
                            msg.attach(img)

                    
                    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
                    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
                    s.send_message(msg)
                    s.quit()
                else:
                    template_str = """
                    <p>
                        Dear {{ user }},
                    </p>
                    <br />
                    <p>
                        We hope this email finds you well. We wanted to share with you the analytics report for your blog posts. 
                    </p>
                    <br />
                    <p>
                        Please find attached a PDF report that includes the following information:
                    </p>
                    <p>
                        - Number of views
                    </p>
                    <p>
                        - Number of likes
                    </p>
                    <p>
                        - Number of comments
                    </p>
                    <br />
                    <p>
                        We hope you find this information useful and informative. If you have any questions or concerns, please don't hesitate to reach out to us.
                    </p>
                    <br />
                    <p>
                        Best regards,
                    </p>
                    <p>
                        Blog-lite
                    """
                    template = Template(template_str)

                    create_pdf_report(user["username"])

                    with open("report.pdf", "rb") as f: 
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(f.read())

                    encoders.encode_base64(part)

                    rendered_template = template.render(user=user["username"])
                    msg.attach(MIMEText(rendered_template, "html"))

                    part.add_header("Content-Disposition", "attachment; filename= report.pdf")
                    msg.attach(part)

                    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
                    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
                    s.send_message(msg)
                    s.quit()

                    os.remove("report.pdf")

                    folder_path = "static/img/Analytics/" + user["username"]

                    if os.path.exists(folder_path):
                        try:
                            shutil.rmtree(folder_path)
                        except OSError as e:
                            pass


@celery.task()
def export(username):
    posts = get_posts_author_desc(username)
    create_pdf(username)

    template = """
    <p>
        Dear {{ user }},
    </p>
    <br />
    <p>
        We hope this email finds you well. We are writing to let you know that your blog export is now ready for download.
    </p>
    <p>
        Please find attached your blog export in a pdf file format. If you have any issues downloading your blog export, please don't hesitate to contact us.
    </p>
    <p>
        Thank you for using our platform!
    </p>
    <br />
    <p>
        Best regards,
    </p>
    <p>
        Blog-lite
    """
    template = Template(template)
    message = template.render(user=username)
    user = get_user_username(username).to_dict()
    file_name = username + "'s posts.pdf"

    file = open(file_name, "rb")

    send_email(user["email"], "Your blog export is ready!", message, attachment = file, filename = file_name, subtype="pdf")

    os.remove(file_name)
