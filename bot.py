import telebot
from bs4 import BeautifulSoup
import sqlite3 as sql
import requests, time, os, sys
import libs.secret as sc
import libs.sqldriver as fl
import libs.listaProductos as lp
import libs.cleanLib as cL
from retrying import retry
import pyshorteners

bot = telebot.TeleBot(sc.token_telegram)
    
def restart():
    sendRestartMsg("Restarting...")
    os.execv(sys.executable, ['python3'] + sys.argv)

def sendRestartMsg(bot_message):
    bot.send_message(sc.cID, bot_message, parse_mode='Markdown')

def tg_sendtext(bot_message):
    bot.send_message(sc.cID, bot_message, parse_mode='Markdown')

def telegram_bot_sendtext(bot_message):
    print(bot_message)
    with sql.connect('items.db') as conn:
        c = conn.cursor()
        sqlite_select_query = """SELECT * from msgs ORDER BY datetime DESC LIMIT 2"""
        mensajes_list = []
        for row in c.execute(sqlite_select_query):
            mensajes_list.append(row[0])
        c.close()
        
    if mensajes_list[0] == mensajes_list[1]:
        print("No hay cambios")
    elif mensajes_list[0] != mensajes_list[1]:
        bot.send_message(sc.cID, bot_message, parse_mode='Markdown')
        print("Hay cambios")
    
    
def sendException(bot_message):
    print(bot_message)
    bot.send_message(sc.cID, "```" + bot_message + "```", parse_mode='Markdown')
    time.sleep(1)


@retry(stop_max_attempt_number=3)
def publicAPI(id_product):
    try:
        url = f"https://publicapi.solotodo.com/products/available_entities/?ids={id_product}&stores=1085&stores=30&stores=3&stores=279&stores=1119&stores=128&stores=920&stores=2570&stores=4418&stores=1712&stores=4385&stores=4&stores=722&stores=788&stores=285&stores=2603&stores=3758&stores=201&stores=398&stores=397&stores=755&stores=3626&stores=4056&stores=31&stores=61&stores=193&stores=7&stores=4055&stores=1052&stores=4187&stores=255&stores=3164&stores=656&stores=3131&stores=16&stores=426&stores=261&stores=4451&stores=1911&stores=88&stores=3791&stores=3593&stores=1580&stores=283&stores=1382&stores=172&stores=2801&stores=559&stores=9&stores=3560&stores=326&stores=4286&stores=822&stores=4682&stores=1349&stores=2735&stores=4484&stores=1976&stores=2240&stores=1217&stores=4517&stores=1448&stores=2274&stores=1811&stores=3692&stores=393&stores=232&stores=87&stores=27&stores=281&stores=4287&stores=263&stores=56&stores=1283&stores=2702&stores=1845&stores=256&stores=2967&stores=954&stores=3428&stores=197&stores=4814&stores=292&stores=5&stores=524&stores=199&stores=43&stores=3956&stores=4154&stores=76&stores=228&stores=294&stores=23&stores=290&stores=392&stores=887&stores=260&stores=195&stores=225&stores=2867&stores=115&stores=4583&stores=3395&stores=265&stores=287&stores=3362&stores=37&stores=118&stores=39&stores=2339&stores=921&stores=116&stores=1250&stores=257&stores=266&stores=3263&stores=986&stores=3890&stores=3659&stores=11&stores=2834&stores=278&stores=34&stores=12&stores=198&stores=3098&stores=1547&stores=1251&stores=1118&stores=267&stores=4022&stores=953&stores=28&stores=3824&stores=186&stores=2471&stores=18&stores=2009&stores=223&stores=2306&stores=2768&stores=4088&stores=194&stores=1316&stores=1019&stores=956&stores=2042&stores=293&stores=1877&stores=2966&stores=623&stores=67&stores=47&stores=86&stores=183&stores=22&stores=3197&stores=3495&stores=4550&stores=4352&stores=1514&stores=3165&stores=955&stores=2999&stores=1086&stores=2670&stores=2438&stores=4121&stores=2669&stores=4616&stores=167&stores=3032&stores=4715&stores=173&stores=264&stores=4220&stores=35&stores=231&stores=2636&stores=6&stores=280&stores=2174&stores=4089&stores=2141&stores=789&stores=359&stores=2835&stores=44&stores=1647&stores=821&stores=63&stores=495&stores=14&stores=239&stores=45&stores=1613&stores=85&stores=4386&stores=1151&stores=3230&stores=91&stores=3099&exclude_refurbished=undefined"
        data = requests.get(url).json()
        idp = data['results'][0]['entities'][0]['id']
        nombre_producto = data['results'][0]['entities'][0]['name']
        external_url = data['results'][0]['entities'][0]['external_url']
        slug = data['results'][0]['product'][0]['slug']
        offer_price = data['results'][0]['entities'][0]['active_registry']['offer_price']
        offer_price = format(int(float(offer_price)), ',')
        solotodo_url = "https://www.solotodo.cl/products/" + str(idp) + "-" + str(slug)
        return  f"El producto `{nombre_producto}` bajó de precio:\n\n👉`{offer_price}`👈  \n\n [LINK PRODUCTO ❗]({external_url}) [❗ SOLOTODO]({solotodo_url})"
    except Exception as e:
        sendException("Exception: publicAPI"+str(e))
        
@retry(stop_max_attempt_number=3)
def publicAPI2(id_product):
    try:
        url = f"https://publicapi.solotodo.com/products/available_entities/?ids={id_product}&stores=1085&stores=30&stores=3&stores=279&stores=1119&stores=128&stores=920&stores=2570&stores=4418&stores=1712&stores=4385&stores=4&stores=722&stores=788&stores=285&stores=2603&stores=3758&stores=201&stores=398&stores=397&stores=755&stores=3626&stores=4056&stores=31&stores=61&stores=193&stores=7&stores=4055&stores=1052&stores=4187&stores=255&stores=3164&stores=656&stores=3131&stores=16&stores=426&stores=261&stores=4451&stores=1911&stores=88&stores=3791&stores=3593&stores=1580&stores=283&stores=1382&stores=172&stores=2801&stores=559&stores=9&stores=3560&stores=326&stores=4286&stores=822&stores=4682&stores=1349&stores=2735&stores=4484&stores=1976&stores=2240&stores=1217&stores=4517&stores=1448&stores=2274&stores=1811&stores=3692&stores=393&stores=232&stores=87&stores=27&stores=281&stores=4287&stores=263&stores=56&stores=1283&stores=2702&stores=1845&stores=256&stores=2967&stores=954&stores=3428&stores=197&stores=4814&stores=292&stores=5&stores=524&stores=199&stores=43&stores=3956&stores=4154&stores=76&stores=228&stores=294&stores=23&stores=290&stores=392&stores=887&stores=260&stores=195&stores=225&stores=2867&stores=115&stores=4583&stores=3395&stores=265&stores=287&stores=3362&stores=37&stores=118&stores=39&stores=2339&stores=921&stores=116&stores=1250&stores=257&stores=266&stores=3263&stores=986&stores=3890&stores=3659&stores=11&stores=2834&stores=278&stores=34&stores=12&stores=198&stores=3098&stores=1547&stores=1251&stores=1118&stores=267&stores=4022&stores=953&stores=28&stores=3824&stores=186&stores=2471&stores=18&stores=2009&stores=223&stores=2306&stores=2768&stores=4088&stores=194&stores=1316&stores=1019&stores=956&stores=2042&stores=293&stores=1877&stores=2966&stores=623&stores=67&stores=47&stores=86&stores=183&stores=22&stores=3197&stores=3495&stores=4550&stores=4352&stores=1514&stores=3165&stores=955&stores=2999&stores=1086&stores=2670&stores=2438&stores=4121&stores=2669&stores=4616&stores=167&stores=3032&stores=4715&stores=173&stores=264&stores=4220&stores=35&stores=231&stores=2636&stores=6&stores=280&stores=2174&stores=4089&stores=2141&stores=789&stores=359&stores=2835&stores=44&stores=1647&stores=821&stores=63&stores=495&stores=14&stores=239&stores=45&stores=1613&stores=85&stores=4386&stores=1151&stores=3230&stores=91&stores=3099&exclude_refurbished=undefined"
        data = requests.get(url).json()
        nombre_producto = data['results'][0]['entities'][0]['name']
        external_url = data['results'][0]['entities'][0]['external_url']
        offer_price = data['results'][0]['entities'][0]['active_registry']['offer_price']
        offer_price = format(int(float(offer_price)), ',')
        type_tiny = pyshorteners.Shortener()
        short_url = type_tiny.tinyurl.short(external_url)
        return f"`Añadido a la base de datos: {nombre_producto} - ({offer_price})` - {str(short_url)}"
    except Exception as e:
        sendException("publicAPI2"+str(e))

def pDesc(price):
    try:
        oldItems = fl.itemS_all('items.db','items')
        nItems = len(oldItems)
        if nItems != 0:
            for item in oldItems:
                    if int(item[1]) != int(price):
                        if int(item[1]) > int(price):                 
                            valor_original = int(item[1])
                            valor_nuevo = int(price)
                            descuento = valor_original - valor_nuevo
                            porcentaje_descuento = (descuento * 100) / valor_original
                            porcentaje_descuento = round(porcentaje_descuento, 2)
                            return (int(porcentaje_descuento*0.01))
    except Exception as e:
        sendException("pDesc"+str(e))

def textDescuento(price):
    try:
        descuento = pDesc(price)
        if descuento >= 0 and descuento <= 10:
            return  f"💩\n"
        elif descuento > 10 and descuento <= 30:
            return  f"😊\n"
        elif descuento > 30 and descuento <= 50:
            return  f"😲\n"
        elif descuento > 50 and descuento <= 60:
            return  f"🤑\n"
        elif descuento > 60  and descuento <= 80:
            return  f"🅱\n"
        elif descuento > 80 and descuento <= 90:
            return  f"🅰\n"
        elif descuento >= 90 and descuento <= 100:
            return  f"🔥\n"
        else:
            return f"🤔\n"
    except Exception as e:
        sendException("textDescuento"+str(e))

def comparaDB(name,price):
    try:
        oldItems = fl.itemS_all('items.db','items')
        nItems = len(oldItems)
        count = 1
        if nItems != 0:
            for item in oldItems:
                if item[0] == name:
                    if int(item[1]) != int(price):
                        if int(item[1]) > int(price):
                            id_product = item[0]
                            id_product = id_product.split('-')
                            id_product = id_product[0]
                            fl.itemIns('items.db','msgs', item[0], price)
                            name_match_query = f"SELECT datetime, mensaje from msgs WHERE datetime = '{id_product}' AND mensaje = '{price}'"
                            conn = sql.connect('items.db')
                            cursor = conn.cursor()
                            cursor.execute(name_match_query)
                            result = cursor.fetchall()
                            if result:
                                print("[SKIP] " + str(item[0]))
                            else:
                                print("No existe")
                                print("[TELEGRAM] Añadido a la base de datos: " + str(item[0]))
                                telegram_bot_sendtext(str(textDescuento(price)) + str(publicAPI(id_product)))
                                
                                
                            fl.itemUpdt('items.db','items', item[0], price)
                        else: 
                            fl.itemUpdt('items.db','items', item[0], price)
                else:
                    if count < nItems:
                        count = count + 1
                    else:
                        id_product = item[0]
                        id_product = id_product.split('-')
                        id_product = id_product[0]
                        fl.itemIns('items.db','items', name, price)
                        info = publicAPI2(id_product)
                        print ('Nuevo item: ', name)
                        tg_sendtext(info)
                        count = 1
        else:
            id_product = item[0]
            id_product = id_product.split('-')
            id_product = id_product[0]
            fl.itemIns('items.db','items', name, price)
            info = publicAPI2(id_product)
            tg_sendtext(info)
            print ('Nuevo item: ', name)
            count = 1
    except Exception as e:
        sendException("comparaDB  " + str(e))
        

@retry(stop_max_attempt_number=3)
def getItems(link):
    try:
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        seturl = requests.get(link, headers=headers)
        doc = BeautifulSoup(seturl.content, 'html.parser')
        items = doc.find_all('div', {'class': 'price'})
        for link in items:
            item = cL.textItem_cleaner(str(link))
            price = cL.textPrice_clean(str(link))
            comparaDB(item, price)
    except ConnectionError as e:
        sendException("Connection Error")
        sendException(str(e))
        
def main():
    for x in lp.consultas:
        getItems(lp.consultas[x])

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    logo="""
            __          _             _____       _                 
           / _|        | |           /  ___|     (_)                
      ___ | |_ ___ _ __| |_ __ _ ___ \ `--. _ __  _ _ __   ___ _ __ 
     / _ \|  _/ _ \ '__| __/ _` / __| `--. \ '_ \| | '_ \ / _ \ '__|
    | (_) | ||  __/ |  | || (_| \__ \/\__/ / | | | | |_) |  __/ |   
     \___/|_| \___|_|   \__\__,_|___/\____/|_| |_|_| .__/ \___|_|   
                                               | |              
                                               |_|                                                                      
    """ 
    print(logo)
    time.sleep(1)
    if not os.path.isfile('items.db'):fl.makeDB()
    count = 0
    while count < 300:
        try:
            main()
            time.sleep(3)
            count = count + 1
        except Exception as e:
            print(e)
            sendException(str(e))
            pass
        except KeyboardInterrupt:
            break
    
    restart()
    bot.infinity_polling(timeout=20, long_polling_timeout = 5)
