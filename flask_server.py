# Данная программа сделана с помощью фреймворка Flask, который будет передавать данные из SQLite в HTML 
from flask import Flask, jsonify, request  # Правильно
import sqlite3

app = Flask(__name__)

# Данный декоратор будет 
@app.route('/api/menu')
def get_menu():
    # Подключаемся к таблицу БД про пользователей
    connF = sqlite3.connect('menufoods.db')
    curF = connF.cursor()
    
    curF.execute("SELECT * FROM menufoods")
    menu = curF.fetchall()
    
    # Преобразуем данный в JSON
    menu_list = []
    for items in menu:
        menu_list.append({
            'id' : items[0],
            'name_dish' : items[1],
            'ingredients' : items[2],
            'cost_dish' : items[3],
            'image_url' : items[4],
        })
    
    # Передам данные в 
    return jsonify(menu_list)

@app.route('/api/order', methods=['POST'])
def create_order():
    data = request.json
    user_id = data['user_id']
    items = data['items']
    address = data['address']
    
    connU = sqlite3.connect('users.db')
    curU = connU.cursor()
    
    curU.execute('''INSERT INTO orders (user_id, items, address, status)
    VALUES (?, ?, ?, ?)
    ''', (user_id, str(items), address, 'pending'))
    connU.commit()
    
    curU.close() # Закрываем сеть
    connU.close()
    
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(port=5000)