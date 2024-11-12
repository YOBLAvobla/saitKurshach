from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functions import page_down, collect_product_info

app = Flask(__name__)


def get_products_links(item_name='ботинки new rock'):
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    driver.get(url='https://ozon.ru')
    time.sleep(2)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(2)

    find_input.send_keys(Keys.ENTER)
    time.sleep(2)

    current_url = f'{driver.current_url}&sorting=rating'
    driver.get(url=current_url)
    time.sleep(2)

    #page_down(driver=driver)  # (для сбора не по первым десяти страницам)
    time.sleep(2)

    try:
        find_links = driver.find_elements(By.CLASS_NAME, 'tile-hover-target')
        products_urls = list(set([f'{link.get_attribute("href")}' for link in find_links]))

        print('[+] Ссылки на товары собраны!')
    except:
        print('[!] Что-то сломалось при сборе ссылок на товары!')

    products_urls_dict = {}

    for k, v in enumerate(products_urls):
        products_urls_dict.update({k: v})

        with open('products_urls_dict.json', 'w', encoding='utf-8') as file:
            json.dump(products_urls_dict, file, indent=4, ensure_ascii=False)

    time.sleep(2)

    products_data = []

    for url in products_urls:
        data = collect_product_info(driver=driver, url=url)
        print(f'[+] Собрал данные товара с id: {data.get("product_id")}')
        time.sleep(1)
        products_data.append(data)

    with open('PRODUCTS_DATA.json', 'w') as file:
        json.dump(products_data, file, indent=4)

    driver.close()
    driver.quit()

    return products_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    product_name = request.form['query']
    products_list = get_products_links(item_name=product_name)

    return render_template('result.html', products=products_list)


if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, render_template, url_for

# app = Flask(__name__)


# @app.route('/')
# @app.route('/home')
# def gay_nigger():
# return render_template("index.html")


# @app.route('/about')
# def about():
# return render_template("about.html")


# @app.route('/user/<string:name>/<int:id>')
# def user(name, id):
# return "user gayname: " + name + "-" + str(id)


# if __name__ == "__main__":
# app.run(debug=True)
