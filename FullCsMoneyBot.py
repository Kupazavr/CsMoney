import requests
import json
from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import steam
from steam import guard
import time
from steampy.client import SteamClient
import telebot


def parser(botnumber, proxy):
    print('started')
    whitelistlist = []
    whitelist = open('D:\CsMoney\whitelist.txt', 'r', encoding='utf-8-sig')
    for i in whitelist.readlines():
        whitelistlist.append(i)
    whitelist.close()
    while True:
        try:
            botinventory = json.loads(requests.get('https://cs.money/load_bots_inventory?', proxies=proxy).text)
            if botinventory.status_code == '403' or botinventory.status_code == '429':
                print(botinventory.status_code + ' ' + botnumber)

            botn = open(botnumber, 'w', encoding='utf-8')
            for g in whitelistlist:
                for Dicts in botinventory:
                    try:
                        t = Dicts.get('e')
                        if t == 'FN':
                            botinventory = ' (Factory New)'
                        elif t == 'MW':
                            botinventory = ' (minimal Wear)'
                        elif t == 'WW':
                            botinventory = ' (Well-Worn)'
                        elif t == 'FT':
                            botinventory = ' (Field-Tested)'
                        elif t == 'BS':
                            botinventory = ' (Battle-Scarred)'
                        for i in Dicts.get('id'):
                            if g[:-1] == (Dicts.get('m') + botinventory):
                                botn.write((Dicts.get('m') + botinventory) + ',' + i + '\n')
                    except AttributeError:
                        continue
            botn.close()
        except:
            continue


# ВЕБ

def web():
    # Потом вмотрирую телегу
    # token = '417167184:AAGKeX24-8gvzI9ZGOUUsZ9lcZ46Oq_6Fwo'
    # bot = telebot.TeleBot(token)

    driver = webdriver.Chrome()
    driver.get('https://cs.money/ru')
    driver.maximize_window()

    def autorize():
        i1 = 0
        while i1 == 0:
            try:
                driver.find_element(By.XPATH, '//*[@id="authenticate_button"]').click()
                i1 += 1
            except Exception:
                continue
        i2 = 0
        while i2 == 0:
            try:
                driver.find_element(By.XPATH, '//*[@id="steamAccountName"]').send_keys('koprozavr')
                driver.find_element(By.XPATH, '//*[@id="steamPassword"]').send_keys('Ghjcnjnfr12345')
                driver.find_element(By.XPATH, '//*[@id="imageLogin"]').click()
                i2 += 1
            except Exception:
                continue

    autorize()

    def auth():
        firstauth = steam.webauth.MobileWebAuth('koprozavr', 'Ghjcnjnfr12345')
        secauth = steam.guard.SteamAuthenticator(
            {"shared_secret": "cPy2hkAUgdWUJW/+1mKT0OZtqOY=", "identity_secret": "n96/dM+qWs6P8JrfOTtUhP0/qKg="},
            medium=firstauth)
        finishauth = secauth.get_code(time.time())
        q1 = 0
        while q1 == 0:
            try:
                driver.find_element(By.XPATH, '//*[@id="twofactorcode_entry"]').send_keys(finishauth)
                q1 += 1
            except Exception:
                continue
        q2 = 0
        while q2 == 0:
            try:
                driver.find_element(By.XPATH,
                                    '//*[@id="login_twofactorauth_buttonset_entercode"]/div[1]/div[2]').click()
                q2 += 1
            except Exception:
                continue

    auth()
    # Блок смены валюты
    r1 = 0
    while r1 == 0:
        try:
            test1 = driver.find_element(By.XPATH, '//*[@id="current_currency"]')
            test2 = driver.find_element(By.XPATH, '//*[@id="currency-drop"]/ul/li[1]/a')
            action = ActionChains(driver)
            action.move_to_element(test1).perform()
            action.move_to_element(test2).click().perform()
            r1 += 1
        except:
            continue

    # Блок Баланса

    # ПОИСК ПРЕДМЕТА НА САЙТЕ

    # Тут должен быть for цикл для поиска предметов
    while True:
        try:
            # Главное

            items = []
            for i in range(1, 11):
                item = open((r'D:\CsMoney\Bots\\')[:-1] + str(i) + '.txt', 'r', encoding="utf-8-sig")
                for i in item:
                    items.append((i[:-1]).split(','))
                item.close()

            if items.__len__() > 0:
                driver.find_element(By.XPATH, '//*[@id="refresh_bot_inventory"]').click()
                h1 = 0
                while h1 == 0:
                    style = driver.find_element(By.XPATH, '//*[@id="circle_bot_inventory"]').get_attribute('style')
                    if style == 'display: none;':
                        h1 += 1
                    else:
                        continue
            else:
                continue
            print('starting finding' + str(time.time()))
            # Блок поиска предмета
            for i in items:
                # Поиск предмета по имени
                if (i[0])[10:15] == 'Music' or (i[0])[0:5] == 'Music':
                    driver.find_element(By.XPATH, '//*[@id="bot-search-input"]').clear()
                    driver.find_element(By.XPATH, '//*[@id="bot-search-input"]').send_keys(i[0] + i[1])

                    print('ищу предмет' + ' ' + i[0] + i[1] + str(time.time()))
                    p1 = 0
                    while p1 == 0:
                        try:
                            h = driver.find_element(By.XPATH,
                                                    "/html/body/div[@class='main']/div[@class='content']/div[@class='trade-container wrapper']/div[@class='row']/div[@class='column-3']/div[@id='block-desktop-bot']/div[@id='block-items-bot']/div[@class='block__content']/div[@id='inventory_bot']/div[15]")
                            continue
                        except:
                            p1 += 1

                else:
                    driver.find_element(By.XPATH, '//*[@id="bot-search-input"]').clear()
                    driver.find_element(By.XPATH, '//*[@id="bot-search-input"]').send_keys(i[0])

                    print('Нашел предмет ' + ' ' + i[0] + str(time.time()))
                    p1 = 0
                    while p1 == 0:
                        try:
                            h = driver.find_element(By.XPATH,
                                                    "/html/body/div[@class='main']/div[@class='content']/div[@class='trade-container wrapper']/div[@class='row']/div[@class='column-3']/div[@id='block-desktop-bot']/div[@id='block-items-bot']/div[@class='block__content']/div[@id='inventory_bot']/div[15]")
                            continue
                        except:
                            p1 += 1
                # Поиск нужного мне предмета
                try:
                    # Нахождение нужного мне предмета по айди
                    if (i[0])[10:15] == 'Music' or (i[0])[0:5] == 'Music':
                        driver.find_element(By.XPATH,
                                            "/html/body/div[@class='main']/div[@class='content']/div[@class='trade-container wrapper']/div[@class='row']/div[@class='column-3']/div[@id='block-desktop-bot']/div[@id='block-items-bot']/div[@class='block__content']/div[@id='inventory_bot']/div[@id='" +
                                            i[2] + "']").click()
                    else:
                        driver.find_element(By.XPATH,
                                            "/html/body/div[@class='main']/div[@class='content']/div[@class='trade-container wrapper']/div[@class='row']/div[@class='column-3']/div[@id='block-desktop-bot']/div[@id='block-items-bot']/div[@class='block__content']/div[@id='inventory_bot']/div[@id='" +
                                            i[1] + "']").click()

                    driver.find_element(By.XPATH, '//*[@id="trade-btn"]').click()
                    g = 0
                    t1 = time.time()
                    # Окошко трейда
                    while g == 0:
                        print('Вывожу предмет' + ' ' + i[0] + str(time.time()))
                        try:
                            a = driver.find_element(By.XPATH, '//*[@id="trade-popup"]/div[4]/div/div[4]').get_attribute(
                                'class')
                            # Если появилась надпись трейда то идем дальше
                            if a == 'waiting__bottom visuallyhidden':
                                driver.refresh()
                                # Проверка на загрузку шмоток
                                h2 = 0
                                while h2 == 0:
                                    style = driver.find_element(By.XPATH,
                                                                '//*[@id="circle_bot_inventory"]').get_attribute(
                                        'style')
                                    if style == 'display: none;':
                                        h2 += 1
                                    else:
                                        continue
                                g += 1
                            elif time.time() - t1 > 15:
                                driver.refresh()
                                # Проверка на загрузку шмоток
                                h3 = 0
                                while h3 == 0:
                                    style = driver.find_element(By.XPATH,
                                                                '//*[@id="circle_bot_inventory"]').get_attribute(
                                        'style')
                                    if style == 'display: none;':
                                        h3 += 1
                                    else:
                                        continue
                                g += 1
                            else:
                                continue
                        except OSError:
                            continue
                except:
                    continue
                    # Пока не знаю что
        # WARNING!! разобратся с OSerror,(Проблема селениума,открывает слишком много сокетов,вполне возможно из-за AJAX)
        except OSError:
            continue
        items.clear()


# Трейд
def tradeautorize():
    time.sleep(40)
    steam_client = SteamClient('F7C162A70D570C47A7BE89CDE6C7ADA8')
    print('ok1')
    steam_client.login('koprozavr', 'Ghjcnjnfr12345', 'D:\CsMoney\Steamguard.txt')
    print('logged')
    while True:
        try:
            received_offers = steam_client.get_trade_offers(True)
            response = received_offers['response']
            trade_offers_received = response.get('trade_offers_received')
            for i in trade_offers_received:
                tradeoffer_id = i.get('tradeofferid')
                message = i.get('message')
                if message == 'Automatically generated from CS.MONEY' or 'This is an automatic trade generated by OPSkins. Security token' in message:
                    print(message)
                    steam_client.accept_trade_offer(tradeoffer_id)
                else:
                    continue
        except:
            continue


def opskinslistings():
    while True:
        time.sleep(200)
        classidpricetradelist = []
        payload = []
        whitelistpricelist = []
        # Получаем список с именами и ценами
        whitelistprice = open('D:\CsMoney\whitelistPrice.txt', 'r', encoding='utf-8-sig')

        for i in whitelistprice:
            whitelistpricelist.append((i[:-1]).split(','))
        whitelistprice.close()
        classidpricetrade = open('D:\CsMoney\ClassIDPriceTrade.txt', 'w', encoding='utf-8')
        steamrequest = json.loads(
            requests.get('http://steamcommunity.com/inventory/76561198246813440/730/2?l=english&count=75').text)
        try:
            for i in steamrequest['descriptions']:
                for g in whitelistpricelist:
                    if (g[0])[10:15] == 'Music' or (g[0])[0:5] == 'Music':
                        if str(i['market_name']) == str(g[0] + g[1]):
                            classidpricetrade.write(i['classid'] + ',' + g[3] + '\n')
                        else:
                            continue
                    else:
                        if str(i['market_name']) == str(g[0]):
                            classidpricetrade.write(i['classid'] + ',' + g[1] + '\n')
                        else:
                            continue
            classidpricetrade.close()
            classidpricetrade = open('D:\CsMoney\ClassIDPriceTrade.txt', 'r', encoding='utf-8-sig')
            # Создали лист с классайди и ценами
            for i in classidpricetrade:
                classidpricetradelist.append((i[:-1]).split(','))
            classidpricetrade.close()
            # Перебор ассет айди,и если найдено в листе нужный классайди то добавляем в пейлоад новый елемент
            for i in steamrequest['assets']:
                for g in classidpricetradelist:
                    if i['classid'] == g[0]:
                        payload.append({"appid": 730, "contextid": 2, "assetid": int(i['assetid']),
                                        "price": (int(float(g[1]) * 100)), "addons": []})
                    else:
                        continue
            whitelistpricelist.clear()
            classidpricetradelist.clear()
            print(payload)
            a = requests.post('https://api.opskins.com/ISales/ListItems/v1/',
                              data={'items': json.dumps(payload), "key": "12c5525e2d3bfcd0b7241fdee228aa"})
            print(a.text)
        except:
            continue


if __name__ == '__main__':
    th1 = Process(target=parser, args=(r'D:\CsMoney\Bts\1.txt', {'https': '188.166.173.172:3128'}))
    th1.start()
    time.sleep(0.1)
    th2 = Process(target=parser, args=(r'D:\CsMoney\Bots\2.txt', {'https': '188.166.145.12:3128'}))
    th2.start()
    time.sleep(0.1)
    th3 = Process(target=parser, args=(r'D:\CsMoney\Bots\3.txt', {'https': '178.62.102.94:3128'}))
    th3.start()
    time.sleep(0.1)
    th4 = Process(target=parser, args=(r'D:\CsMoney\Bots\4.txt', {'https': '139.59.187.166:3128'}))
    th4.start()
    time.sleep(0.1)
    th5 = Process(target=parser, args=(r'D:\CsMoney\Bots\5.txt', {'https': '138.68.132.66:3128'}))
    th5.start()
    time.sleep(0.1)
    th6 = Process(target=parser, args=(r'D:\CsMoney\Bots\6.txt', {'https': '46.101.23.161:3128'}))
    th6.start()
    time.sleep(0.1)
    th7 = Process(target=parser, args=(r'D:\CsMoney\Bots\7.txt', {'https': '178.62.64.155:3128'}))
    th7.start()
    time.sleep(0.1)
    th8 = Process(target=parser, args=(r'D:\CsMoney\Bots\8.txt', {'https': '46.101.11.118:3128'}))
    th8.start()
    time.sleep(0.1)
    th9 = Process(target=parser, args=(r'D:\CsMoney\Bots\9.txt', {'https': '138.68.142.54:3128'}))
    th9.start()
    time.sleep(0.1)
    th10 = Process(target=parser, args=(r'D:\CsMoney\Bots\10.txt', {'https': '139.59.177.227:3128'}))
    th10.start()
    thWeb = Process(target=web)
    thWeb.start()
    thTrade = Process(target=tradeautorize)
    thTrade.start()
    thOps = Process(target=opskinslistings)
    thOps.start()
