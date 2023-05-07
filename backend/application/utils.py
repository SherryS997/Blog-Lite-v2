from PIL import Image
import io
import seaborn as sns
import matplotlib.pyplot as plt
import os, smtplib
import pandas as pd
from application.data_access import get_posts_author_desc, get_comments_post
from application.config import UPLOAD_FOLDER
from weasyprint import HTML
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.application import MIMEApplication
from email import encoders


def create_plot(data, plot_type, username):
    import matplotlib

    matplotlib.use('GTK3Cairo')

    sns.set_style("whitegrid")
    sns.set(rc={"figure.figsize":(18, 10)})
    
    # Create the bar plot
    ax = sns.barplot(x=plot_type, y="Titles", data=data, color="skyblue")

    # Add the view numbers to the bars
    for i, v in enumerate(data[plot_type]):
        ax.text(v + 0.5, i, str(v), color='black', fontweight='bold', rotation=270)

    # Add labels and a title
    ax.set_xlabel(plot_type)
    ax.set_ylabel("Title")
    ax.set_title("Post " + plot_type, fontsize=20)

    folder_name = UPLOAD_FOLDER+ "Analytics/" + username
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    plt.savefig(folder_name + "/" + plot_type +".png")
    plt.clf()

def convert_to_webp(image_file):
    with Image.open(image_file) as img:
        width, height = img.size
        max_size = 800
        if width > max_size or height > max_size:
            ratio = max_size / max(width, height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), resample=Image.LANCZOS)
        output = io.BytesIO()
        img.save(output, format='webp', quality=80)
        return output.getvalue()

def create_analytics(username):
    posts = get_posts_author_desc(username)
    titles = [post.title for post in posts]
    views = [post.views for post in posts]
    likes = [post.likes for post in posts]
    comments = [len(get_comments_post(post.roll)) for post in posts]
    view_data = pd.DataFrame({
        'Titles': titles,
        'Views': views
    })

    like_data = pd.DataFrame({
        'Titles': titles,
        'Likes': likes
    })

    comment_data = pd.DataFrame({
        'Titles': titles,
        'Comments': comments
    })

    create_plot(view_data, "Views", username)
    create_plot(like_data, "Likes", username)
    create_plot(comment_data, "Comments", username)

def create_pdf_report(username):
    html = HTML(url="http://localhost:2345/97NBUmvRLiA4mz6Or6ZWF24lQj8Pt1slyRHnZitcsdMPOy8bHp3w6PcdIm2diYU/"+ username)
    file_name = "report.pdf"
    html.write_pdf(target=file_name)


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def send_email(address, subject, message, attachment=None, images=None, filename=None, subtype=None):
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "service@bloglite.com"
    SENDER_PASSWORD = ""

    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = address
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))

    if attachment:
        part = MIMEApplication(attachment.read(), _subtype=subtype)
        part.add_header("Content-Disposition", "attachment", filename= filename)
        msg.attach(part)
    
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

def create_pdf(username):
    html = HTML(url="http://localhost:2345/97NBUmvRLiA4mz6Or6aadsflQj8Pt1slyRHnZitcsdMPOy8bHp3w6PcdIm2diYU/"+ username)
    file_name = username + "'s posts.pdf"
    html.write_pdf(target=file_name)