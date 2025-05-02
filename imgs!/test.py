# from datetime import datetime
# import sqlite3
# from random import randint

# conn = sqlite3.connect('users.db')
# cur = conn.cursor()

# name_img = randint(1000000, 9999999)

# cur.execute('SELECT img FROM imgs')
# all_imgs = cur.fetchall()

# if name_img in all_imgs[0]:
#     print('true')
# else:
#     print('false')

# cur.execute('SELECT nickname FROM users WHERE nickname = ?', ['Саша'])
# users_nickname = cur.fetchone()
# print(users_nickname)
# if users_nickname == None:
#     print('true')
# else:
#     print('false')



# now = datetime.now()
# date = now.strftime("%d/%m/%Y %H:%M")
# print(date)
# # print(now.strftime("%D %H:%M:%S"))

