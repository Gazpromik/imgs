from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import requests
import sqlite3
import json
import os
from datetime import timedelta, datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
import time
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(weeks=1)

upload_folder = 'C:\\Рабочий стол\\Новая web разработка\\Projects\\imgs!\\static'
app.config['UPLOAD_FOLDER'] = upload_folder


class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f'{prompt}'
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        
        if 'uuid' not in data:
            raise KeyError(f"В ответе нет 'uuid': {data}")

        return data['uuid']
        

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)


@app.route('/')
def main():
    return render_template('index.html')
@app.route('/register', methods=["POST"])
def register():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    data = request.form.to_dict()
    nickname = request.form.get("nickname")
    email = request.form.get("email")
    password = request.form.get("password")
    email_code = ''
    accept_password = request.form.get("accept_password")
    

    cur.execute('SELECT nickname FROM users WHERE nickname = ?', [nickname])
    users_nickname = cur.fetchone()
    cur.execute('SELECT email FROM users WHERE email = ?', [email])
    users_email = cur.fetchone()
    if nickname == '' or email == '' or password == '' or accept_password == '':
        return jsonify({"status": "no_info"})
    elif password != accept_password:
        return jsonify({"status": "passwords_not_match"})
    elif users_nickname != None:
        return jsonify({"status": "nickname_is_exists"})
    elif users_email != None:
        return jsonify({"status": "email_is_exists"})
    elif users_nickname == None and users_email == None and password == accept_password:
        num1 = str(randint(0, 9))
        num2 = str(randint(0, 9))
        num3 = str(randint(0, 9))
        num4 = str(randint(0, 9))
        num5 = str(randint(0, 9))
        num6 = str(randint(0, 9))
        email_code = num1+num2+num3+num4+num5+num6
        session['temporary_data'] = [data, nickname, email, password, email_code]
        # Данные для подключения
        smtp_server = "smtp.yandex.ru"
        smtp_port = 465  
        sender_email = "Chiparick1234@yandex.ru"  # Ваш email на Яндексе
        sender_password = "oxbceygctbveddim"      # Ваш пароль или пароль от приложения
        recipient_email = email  # Email получателя

        html_content = render_template("email_html.html", email_code=email_code) #делаем html письмо и добавляем туда код
        # Создание MIME-сообщения
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = "Подтверждение почты"

        # Тело письма
        message.attach(MIMEText(html_content, "html"))

        # Подключение к серверу и отправка письма
        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, message.as_string())
                print("Сообщение успешно отправлено!")
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
        return jsonify({"status": "success"})



@app.route('/confirm_email', methods=["POST"])
def confirm_email():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    user_code = str(request.form.get("user_code"))

    data = session['temporary_data'][0]
    nickname = session['temporary_data'][1]
    email = session['temporary_data'][2]
    password = session['temporary_data'][3]

    email_code = session['temporary_data'][4]

    if user_code == '':
        return jsonify({"status": "wait_to_confirm"})
    elif user_code != email_code:
        return jsonify({"status": "invalid_code"})
    elif user_code == email_code:
        cur.execute('INSERT INTO users (nickname, email, password, like_imgs) VALUES (?,?,?,?)', [nickname, email, password, ''])
        conn.commit()
        session['user'] = nickname
        session['temporary_data'].clear()
        return jsonify({'status': 'success', 'Data': data, 'nickname': nickname, 'email': email})
@app.route('/login', methods=["POST"])
def login():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # if 'user' in session:
    #     cur.execute("SELECT * FROM users WHERE nickname = ?", [session['user']])
    #     result = cur.fetchall()
    #     return jsonify({'status': 'success', 'Data': result, 'nickname': result[0][1], 'password': result[0][3], 'email': result[0][2]})
    
    
    
    
    
    data_input = request.form.to_dict()
    nickname = request.form.get("nickname_log")
    password = request.form.get("password_log")
    cur.execute('SELECT * FROM users WHERE nickname = ?', [nickname])
    data = cur.fetchall()

    if nickname == '' or password == '':
        return jsonify({'status': 'no_input'})
    elif not data:
        return jsonify({'status': 'no_info'})
    elif data[0][1] == nickname and data[0][3] == password:
        session['user'] = nickname
        return jsonify({'status': 'success', 'Data': data_input, 'nickname': nickname, 'password': password, 'email': data[0][2]})
    else:
        return jsonify({'status': 'access_denied'})
@app.route('/get_img', methods=["POST"])
def get_img():
    
    if "get_file" not in request.files:
        return jsonify({"error": "Файл не передан"}), 400

    file = request.files["get_file"]
    if file.filename == "":
        return jsonify({"error": "Файл не выбран"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    discribe_picture = request.form.get("discribe_picture", "")

    img_url = f"/static/{file.filename}"  

    try:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO imgs (img, discribe, likes, comments, users_like) VALUES (?, ?, 0, 0, ?)', (img_url, discribe_picture, ''))
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"error": f"Ошибка БД: {str(e)}"}), 500

    return jsonify({"message": "Файл загружен", "img_url": img_url})

@app.route('/update', methods=["POST"])
def update():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM imgs')
    return cur.fetchall()
@app.route('/like', methods=["GET"])
def like():
    if 'user' not in session:
        return 'noUser'
    img = request.args.get("src")

    increace = int(request.args.get("increace"))

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM imgs WHERE img = ?', [img])
    data_img = cur.fetchone()
    print(data_img)
    id_img = str(data_img[0])

    cur.execute('SELECT like_imgs, id FROM users WHERE nickname = ?', [session['user']])
    user_likes = cur.fetchone()

    print(type(user_likes[0]), user_likes[0])
    print(type(id_img), id_img)

    if increace == 1:
        new_user_likes = user_likes[0] + "," + id_img
    elif increace == -1:
        new_user_likes = user_likes[0].replace(","+id_img,"")
        

    likes = data_img[3] + increace

    print(new_user_likes)
    print(user_likes[1])
    cur.execute('UPDATE imgs SET likes = ? WHERE img = ?', (likes, img))
    conn.commit()
    cur.execute('UPDATE users SET like_imgs = ? WHERE id = ?', (new_user_likes, user_likes[1]))
    conn.commit()

    

    cur.execute('SELECT * FROM imgs WHERE img = ?', [img])
    new_data_img = cur.fetchone()

    conn.close()
    return jsonify({"img": new_data_img})

@app.route('/exit_from_acc', methods=["GET"])
def exit_from_acc():
    session.clear()
    return jsonify({"session": 'clear'})
@app.route('/current_picture', methods=["GET"])
def current_picture():
    if 'user' not in session:
        return jsonify({"status": 'noUser'})
    img = request.args.get("url")
    
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM imgs WHERE img = ?', [img])
    results = cur.fetchall()
    id_img = str(results[0][0])
    cur.execute('SELECT like_imgs FROM users WHERE nickname = ?', [session['user']])
    user = cur.fetchone()
    user_likes = user[0].split(",")
    if id_img in user_likes:
        like = 'true'
    else:
        like = 'false'
    cur.execute('SELECT * FROM comments WHERE img = ?', [img])
    img_comments = cur.fetchall()

    conn.close()
  
    return jsonify({"img": results, "status": 'ok', "like": like, "comment": img_comments})
@app.route('/comments', methods=["POST"])
def comments():
    comment = request.form.get("koment")
    user = session['user']
    img = request.form.get("src")
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M")
    print(img, ' ', comment, ' ', user, ' ', date)

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO comments (img, text, nickname, data) VALUES (?,?,?,?)', [img , comment, user, date])
    conn.commit()
    
    img_comment_content = [comment, user, date]

    conn.close()

    return jsonify({"comment": img_comment_content})
    
@app.route('/generate_img', methods=["POST"])
def generate_img():
    discribe = str(request.form.get("discribe"))

    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', 'DA0C0AAEF4CBC3BFEB2DD9A2AFA78C43', '0B6DBAC1A6436454429E37ABF5CCE76C')
    pipeline_id = api.get_pipeline()
    uuid = api.generate(discribe, pipeline_id)
    files = api.check_generation(uuid)

    img64 = files[0]

    img = base64.b64decode(files[0])

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    session['generate_id'] = ''

    cur.execute('INSERT INTO test_generate (img, text) VALUES (?,?)', [img, discribe])
    conn.commit()

    cur.execute('SELECT id FROM test_generate WHERE img = ?', [img])
    img_id = cur.fetchone()

    session['generate_id'] = img_id[0]

    return jsonify({"img": img64})

@app.route('/publish_img', methods=["POST"])
def publish_img():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM test_generate WHERE id = ?', [session['generate_id']])
    generated_img = cur.fetchone()

    

    cur.execute('SELECT img FROM imgs')
    all_imgs = cur.fetchall()


    while True:
        num_img = randint(1000000, 9999999)
        if num_img in all_imgs:
            pass
        else:
            name_img = f"static/{num_img}.png"
            break
    
    

    with open(name_img,"wb") as f:
        f.write(generated_img[1])

    cur.execute('INSERT INTO imgs (img, discribe, likes, comments, users_like) VALUES (?, ?, 0, 0, ?)', (name_img, generated_img[2], ''))
    conn.commit()

    return jsonify({"status": 'success'})
app.run()