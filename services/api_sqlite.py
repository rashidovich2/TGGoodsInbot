# - *- coding: utf- 8 - *-
import math
import random
import asyncio
import aiosqlite
import sqlite3
import json
import zoneinfo
import pytz
import datetime
import decimal
from tgbot.utils.const_functions import get_unix, convert_day, get_date, ded


D=decimal.Decimal

def adapt_decimal(d):
    return str(d)

def convert_decimal(s):
    return D(s)

# Register the adapter
sqlite3.register_adapter(D, adapt_decimal)

# Register the converter
sqlite3.register_converter("decimal", convert_decimal)

MSK = zoneinfo.ZoneInfo("Europe/Moscow")

from tgbot.data.config import PATH_DATABASE
from tgbot.utils.const_functions import get_unix, get_date, clear_html

#Добавление отправки асихронное
async def add_sending_postx(sending_id, user_id, post_id, msgid, current_state):
    await print(user_id)
    async with aiosqlite.connect(PATH_DATABASE) as con:
        con.row_factory = aiosqlite.Row
        await con.execute("INSERT INTO storage_posts_sending "
                          "(sending_id, user_id, post_id, msgid, current_state) "
                          "VALUES (?, ?, ?, ?, ?)",
                          [sending_id, user_id, post_id, msgid, current_state])
        await con.commit()
        return sending_id

# Редактирование пользователя
def update_sendings(sending_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_posts_sending SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(f"{sql}WHERE sending_id = ?", parameters)
        con.commit()


# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

####################################################################################################
##################################### ФОРМАТИРОВАНИЕ ЗАПРОСА #######################################
# Форматирование запроса без аргументов
def update_format(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


# Форматирование запроса с аргументами
def update_format_args(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())

# Форматирование запроса с аргументами
def update_format_or_args(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " OR ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())

########################################### ЗАПРОСЫ НА ПРОДАВЦА ########################
########################################################################################
def create_seller_request(user_id, requesttxt):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_requests "
                    "(requester, datetime, state, requesttxt) "
                    "VALUES (?, ?, ?, ?)",
                    [user_id, get_unix(), 'created', requesttxt])
        con.commit()

# Получение всех запросов продавцов
def get_all_randtgaccounts():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT * FROM storage_tgaccounts"
        return con.execute(sql).fetchall()

#Проыерка на дубли username
def check_dbfor_invited_username(username):
    print('Проверка на существование записи username api_sqlite.py  67')
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT count(*) FROM storage_tgparse "
        #sql, parameters = update_format_args(sql, kwargs)
        #return con.execute(sql, parameters).fetchone()
        #sql, parameters = update_format(sql, kwargs)
        #parameters.append(user_id)
        dbrow = []
        #count = 0
        dbrow = con.execute(
            f"{sql}WHERE state='invited' AND username = ?", [username]
        ).fetchone()[0]
        #print(len(dbrow))
        print(dbrow)
        #count = len(dbrow)
        #print(str(dbrow['username']))
        #dbrow=dbrow.strip("(")
        #dbrow=dbrow.strip(")")
        #dbrow=dbrow.strip(",")
        #con.commit()
        print(f'Проверяем {username} в БД')
        return dbrow >= 1

# Удаление корзины
def remove_ordersx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_orders"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

# Удаление позиций корзины
def remove_orders_itemx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_orders_items"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

#Проыерка на дубли username
def check_dbfor_username(username):
    print('Проверка на существование записи username api_sqlite.py  67')
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT count(*) FROM storage_tgparse "
        #sql, parameters = update_format_args(sql, kwargs)
        #return con.execute(sql, parameters).fetchone()
        #sql, parameters = update_format(sql, kwargs)
        #parameters.append(user_id)
        dbrow = []
        #count = 0
        dbrow = con.execute(f"{sql}WHERE username = ?", [username]).fetchone()[0]
        #print(len(dbrow))
        print(dbrow)
        #count = len(dbrow)
        #print(str(dbrow['username']))
        #dbrow=dbrow.strip("(")
        #dbrow=dbrow.strip(")")
        #dbrow=dbrow.strip(",")
        #con.commit()
        print(f'Проверяем {username} в БД')
        return dbrow >= 1

# Удаление аккаунта ТГ
def remove_accountx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_tgaccounts"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

#Пользователи по статусам
def get_all_tgaccounts_states():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT source, groupname, state, count(username) FROM storage_tgparse GROUP BY source, groupname, state"
        return con.execute(sql).fetchall()

# Получение всех запросов продавцов
def get_all_tgaccounts_to_invite():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT * FROM storage_tgaccounts WHERE state='available'"
        return con.execute(sql).fetchall()

# Получение всех запросов продавцов
def get_all_avtgaccounts():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT * FROM storage_tgaccounts WHERE state='available'"
        return con.execute(sql).fetchall()

# Получение всех покупок
def get_all_partnersx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_partners"
        return con.execute(sql).fetchall()

# Получение номеров по статусам
def get_all_tgaccounts_time_wb():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT * FROM storage_tgaccounts WHERE state!='banned' ORDER BY date(waitfor24) ASC"
        return con.execute(sql).fetchall()

# Получение номеров по статусам
def get_all_tgaccounts_time():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT * FROM storage_tgaccounts ORDER BY date(waitfor24) ASC"
        return con.execute(sql).fetchall()

# Получение номеров по статусам
def get_all_tgaccounts():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT * FROM storage_tgaccounts"
        return con.execute(sql).fetchall()

# Получение всех запросов продавцов
def get_tgaccount_statecounts(account_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        #sql = "SELECT state, invited24, last FROM storage_tgaccounts "
        sql = "SELECT invited24 FROM storage_tgaccounts "
        return con.execute(f"{sql}WHERE account_id = ?", [account_id]).fetchone()

# Добавление аккаунта ТГ в БД
def add_tgacc_todb(username, user_id, access_hash, name, source, groupname, group_id, tag, state='created'):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_tgparse "
                    "(username, user_id, access_hash, name, source, groupname, group_id, tag, state) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [username, user_id, access_hash, name, source, groupname, group_id, tag, state])
        print("addok")
        con.commit()

def add_post_to_plan(ct, user_id, send_message, mode, caption=''):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        cur_time = datetime.datetime.now()
        #cur_time = datetime.utcnow().replace(tzinfo=pytz.utc)
        print(cur_time)
        if ct == 'text':
            ct, user_id, post_text, post_photo, post_video, post_animation, cur_time, mode, caption  = ct, user_id, send_message, 0, 0, 0, cur_time, mode, 0
        if ct == 'photo':
            ct, user_id, post_text, post_photo, post_video, post_animation, cur_time, mode, caption   = ct, user_id, 0, send_message, 0, 0, cur_time, mode, caption
        if ct == 'video':
            ct, user_id, post_text, post_photo, post_video, post_animation, cur_time, mode, caption   = ct, user_id, 0, 0, send_message, 0, cur_time, mode, caption
        if ct == 'animation':
            ct, user_id, post_text, post_photo, post_video, post_animation, cur_time, mode, caption   = ct, user_id, 0, 0, 0, send_message, cur_time, mode, caption
        state = "created"

        con.execute("INSERT INTO storage_posts "
                    "(ct, user_id, post_text, post_photo, post_video, post_animation, dtpost, mode_tohour, caption, state) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [ct, user_id, post_text, post_photo, post_video, post_animation, cur_time, mode, caption, state])

        con.commit()

# Получение всех запросов продавцов
def get_lastpost():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        #sql = "SELECT state, invited24, last FROM storage_tgaccounts "
        sql = "SELECT MAX(post_id) as post_id FROM storage_posts GROUP BY user_id"
        return con.execute(sql).fetchone()[0]


# Получение поста
def get_postx(post_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_posts "
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(f"{sql}WHERE post_id = ?", [post_id]).fetchone()
        #return con.execute(sql, parameters).fetchone()

#Получение городов и url каналов
def get_cities_places():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT id as place_id, city as place_name, vacs_url FROM data_cities WHERE vacs_url is not Null"
        return con.execute(sql).fetchall()

# Получение пользователя
def get_sending_postxx(user_id, post_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_posts_sending "
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(f"{sql}WHERE user_id = ? AND post_id=?", [user_id, post_id]).fetchone()
        #return con.execute(sql, parameters).fetchall()

# Получение пользователя
def get_postxx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_posts "
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение всех запросов продавцов
def get_3tohour_postx():
    with sqlite3.connect(PATH_DATABASE) as con:
        print("-->")
        sql = "SELECT * FROM storage_posts WHERE mode_remind=1 AND strftime('%s', dtpost) < strftime('%s', 'now') LIMIT 3"
        return con.execute(sql).fetchall()
        #posts = con.execute("SELECT * FROM storage_posts WHERE state = 'created' AND dtpost < datetime('now')").fetchall()
        #return posts

# Получение всех постов со статусом Создан и моментом меньше сейчас
def get_tohour_postx():
    with sqlite3.connect(PATH_DATABASE) as con:
        print("-->")
        sql = "SELECT * FROM storage_posts "
        return con.execute(
            f"{sql}WHERE state='created' AND strftime('%s', dtpost) < strftime('%s', 'now')"
        ).fetchall()

# Обновление статусов постов
def update_tohour_postx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.execute("UPDATE storage_posts SET state = 'sended' WHERE dtpost < datetime('now')")
        con.commit()

# Получение всех запросов продавцов
def update_3tohour_postx(post_ids):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.execute("UPDATE storage_posts SET remind_iter = remind_iter+1 WHERE post_id in(?)", [])
        con.commit()

# Получение всех запросов продавцов
def get_sellers_news_postx(tag = "selnews"):
    with sqlite3.connect(PATH_DATABASE) as con:
        print("-->")
        sql = "SELECT * FROM storage_posts "
        return con.execute(
            f"{sql}WHERE state = 'created' AND tag = ?", [tag]
        ).fetchall()


# Получение всех запросов продавцов
def get_planed_postx(mode_evening = "evening"):
    with sqlite3.connect(PATH_DATABASE) as con:
        print("-->")
        sql = "SELECT * FROM storage_posts "
        return con.execute(
            f"{sql}WHERE state = 'created' AND mode_evening = ?",
            [mode_evening],
        ).fetchall()



def get_planed_eventsx():
    with sqlite3.connect(PATH_DATABASE) as con:
        print("-->")
        sql = "SELECT event_photo, event_name || ' | ' ||event_description|| ' | ' || address as xxx FROM storage_events LEFT JOIN storage_places USING(place_id)"
        #return con.execute(sql + "WHERE strftime('%s', event_date) > strftime('%s', 'now')").fetchall()
        return con.execute(sql).fetchall()


# Редактирование запроса
def update_sending_post(sending_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_posts_sending SET "
        sql, parameters = update_format(sql, kwargs)
        parameters.append(post_id)
        con.execute(f"{sql}WHERE sending_id = ?", parameters)
        con.commit()



# Редактирование запроса
def update_post(post_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_posts SET "
        sql, parameters = update_format(sql, kwargs)
        parameters.append(post_id)
        con.execute(f"{sql}WHERE post_id = ?", parameters)
        con.commit()

# Редактирование запроса
def update_event(event_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_events SET "
        sql, parameters = update_format(sql, kwargs)
        parameters.append(event_id)
        con.execute(f"{sql}WHERE event_id = ?", parameters)
        con.commit()

#есть ли магазин у пользователя
def check_user_shop_exist(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT a.user_role, b.admin, b.name FROM storage_users a LEFT JOIN storage_shop b ON(a.user_id=b.admin)"
        shopadmin = con.execute(f"{sql}WHERE a.user_id = ?", [user_id]).fetchone()
        #print(shopadmin)
        if (
            shopadmin['user_role'] == "ShopAdmin"
            and shopadmin['admin'] is not None
        ): return shopadmin['name']
        elif shopadmin['user_role'] == "Admin": return False
        #else: return shopadmin['admin']

#есть ли магазин у пользователя
def check_user_artist_exist(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT a.user_role, b.admin, b.name FROM storage_users a LEFT JOIN storage_artists b ON(a.user_id=b.admin)"
        shopadmin = con.execute(f"{sql}WHERE a.user_id = ?", [user_id]).fetchone()
        print(shopadmin)
        if (
            shopadmin['user_role'] == "ShopAdmin"
            and shopadmin['admin'] is not None
        ): return shopadmin['name']
        elif shopadmin['user_role'] == "Admin": return False
        #else: return shopadmin['admin']

#есть ли магазин у пользователя
def check_user_events_exist(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT a.user_id, b.event_name, b.event_user_id FROM storage_users a LEFT JOIN storage_events b ON(a.user_id=b.event_user_id)"
        users_event = con.execute(f"{sql}WHERE a.user_id = ?", [user_id]).fetchone()
        print(users_event)
        #if shopadmin['user_role'] == "ShopAdmin" and not (shopadmin['admin'] is None): return shopadmin['name']
        #elif shopadmin['user_role'] == "Admin": return False
        #else: return shopadmin['admin']
        return users_event


# Добавление аккаунта ТГ в БД
def add_account_todb(xid, xhash, xphone, invited24, state='created'):
    with sqlite3.connect(PATH_DATABASE) as con:
        datenow = datetime.datetime.now()
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_tgaccounts "
                    "(tg_api_id, tg_api_hash, phone, invited24, date, state) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    [xid, xhash, xphone, invited24, datenow, state])
        con.commit()
        #print(con.lastrowid)

# Получение всех запросов продавцов
def get_lasttgaccount():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        #sql = "SELECT state, invited24, last FROM storage_tgaccounts "
        sql = "SELECT MAX(account_id) as acc FROM storage_tgaccounts GROUP BY account_id"
        return con.execute(sql).fetchone()[0]

# Группы в ТГ
def groups_telegram():
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT group_id, groupname, count(acc_id) as countacc FROM storage_tgparse WHERE groupname != '' AND source = 'groups' AND state = 'created' GROUP BY group_id ORDER BY group_id ASC"
        return con.execute(sql).fetchall()

# Пользователи группы для инвайта
def first_grouptoinvitebyid(groupid, start, count):
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_tgparse WHERE state = 'created' AND source = 'groups' AND group_id=? ORDER BY acc_id ASC LIMIT {start},{count}"
        return con.execute(sql, [groupid]).fetchall()

# Пользователи группы для инвайта
def first_grouptoinvite(groupname, start, count):
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_tgparse WHERE state = 'created' AND source = 'groups' AND groupname=? ORDER BY acc_id ASC LIMIT {start},{count}"
        return con.execute(sql, [groupname]).fetchall()

# Последние 10 покупок
def first_toinvite(state, start, count):
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_tgparse WHERE state = ? AND source = 'groups' ORDER BY acc_id ASC LIMIT {start},{count}"
        return con.execute(sql, [state]).fetchall()



def firstgeo_toinvite(state, start, count):
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_tgparse WHERE state = ? AND source = 'geoparse' ORDER BY acc_id ASC LIMIT {start},{count}"
        return con.execute(sql, [state]).fetchall()
        #return con.execute(sql).fetchall()

# Редактирование запроса
def update_tgparsex(acc_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_tgparse SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(acc_id)
        con.execute(f"{sql}WHERE acc_id = ?", parameters)
        con.commit()

# Редактирование запроса
def update_tgaccounts(account_id, pole):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        inc = ""
        if pole == 'available':
            inc = " state = 'available', invited24 = 0 "
        elif pole == 'banned':
            inc = " state = 'banned' "
        elif pole == 'invited24':
            inc = " invited24 = invited24 + 1, last = datetime('now') "
        elif pole == 'iter24':
            inc = " iter24 = iter24 + 1 "
        elif pole == 'waitfor24':
            inc = " state = 'wait', waitfor24 = datetime('now', '+1 day') "
        sql = f"UPDATE storage_tgaccounts SET {inc}"
        #sql, parameters = update_format(sql, kwargs)
        #parameters.append(account_id)
        con.execute(f"{sql}WHERE account_id = ?", [account_id])
        con.commit()

#удаление аккаунта
def delete_tgacc(acc_id):
    print(f"Удаляем аккаунт{acc_id}")
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_tgaccounts "
        #sql, parameters = update_format_args(sql, kwargs)
        #sql, user_id = update_format(sql, user_id)
        con.execute(f"{sql}WHERE account_id = ?", [acc_id])
        con.commit()

# Получение всех запросов продавцов
def get_delivery_seller_options(order_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_orders_users_items "
        return con.execute(f"{sql}WHERE order_id = ?", [order_id]).fetchone()

# Получение всех запросов продавцов
def get_users_by_citiesx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT user_city, user_city_id, count(user_id) as countu FROM storage_users WHERE user_city_id IS NULL GROUP BY user_city_id ORDER BY countu DESC"
        return con.execute(sql).fetchall()

def get_users_by_cities():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT user_city, user_city_id, count(user_id) as countu FROM storage_users GROUP BY user_city_id ORDER BY countu DESC"
        return con.execute(sql).fetchall()

def get_pm_category_count():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT d.category_id, d.level, d.parent_id, d.category as category, c.category as category2, COUNT(p.position_id) as countp FROM storage_position p LEFT JOIN cls_categories c ON(p.category_id=c.category_id) LEFT JOIN cls_categories d ON(d.category_id=c.parent_id) WHERE c.category_id<72 GROUP BY c.category"
        return con.execute(sql).fetchall()


def get_category_count(category_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT COUNT(position_id) as countp FROM storage_position WHERE category_id={category_id}"
        return con.execute(sql).fetchone()

# Получение всех запросов продавцов
def get_all_requestx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT DISTINCT requester as user_id FROM storage_requests GROUP BY requester ORDER BY datetime ASC"
        return con.execute(sql).fetchall()

# Получение всех позиций на согласование
def get_all_funds_adds_stated(state):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT refill_receipt FROM storage_refill WHERE refill_state=?"
        return con.execute(sql, [state]).fetchall()


# Получение всех позиций на согласование
def get_all_positions_requestx_stated(state):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT position_id FROM storage_position WHERE position_type=3 AND position_state=?"
        return con.execute(sql, [state]).fetchall()


# Получение всех запросов продавцов
def get_all_requestx_stated(state):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT DISTINCT requester as user_id FROM storage_requests WHERE state=? GROUP BY requester ORDER BY datetime ASC"
        return con.execute(sql, [state]).fetchall()

# Удаление запроса
def delete_position_requests_userx(position_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_position "
        #sql, parameters = update_format_args(sql, kwargs)
        #sql, user_id = update_format(sql, user_id)
        con.execute(f"{sql}WHERE position = ?", [position_id])
        con.commit()

# Удаление запроса
def delete_requests_userx(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_requests "
        #sql, parameters = update_format_args(sql, kwargs)
        #sql, user_id = update_format(sql, user_id)
        con.execute(f"{sql}WHERE requester = ?", [user_id])
        con.commit()


# Редактирование запроса
def update_requestx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_requests SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(f"{sql}WHERE requester = ?", parameters)
        con.commit()


# Проверка принадлежности позиции в каталоге
def check_position_owner(user_id, position_id):
    print('Проверка принадлежности позиции api_sqlite.py  86')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT position_user_id FROM storage_position "
        #sql, parameters = update_format_args(sql, kwargs)
        #return con.execute(sql, parameters).fetchone()

        #sql, parameters = update_format(sql, kwargs)
        #parameters.append(user_id)
        dbuser_id = con.execute(
            f"{sql}WHERE position_id = ?", [position_id]
        ).fetchone()
        #con.commit()
        print(f'Лот пользователя {dbuser_id} проверяем для {user_id} 97')
        return user_id in [dbuser_id['position_user_id'], 919148970]

#Добавление отправки асихронное
async def add_sending_postx3(user_id, post_id, msgid, current_state):
    await print(user_id)
    async with aiosqlite.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        con.row_factory = aiosqlite.Row
        #dt  = await get_unix()
        sending_id = await random.randint(1000000000, 9999999999)
        await asyncio.sleep(0.5)
        try:
            await con.execute("INSERT INTO storage_posts_sending "
                              "(sending_id, user_id, post_id, msgid, current_state) "
                              "VALUES (?, ?, ?, ?, ?)",
                              [sending_id, user_id, post_id, msgid, current_state])
            await con.commit()
            return sending_id
        except Exception:
            pass



# Добавление пользователя
def add_sending_postx7(sending_id, user_id, post_id, msgid, current_state):
    print(user_id)
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        dt = get_unix()
        #sending_id = random.randint(1000000000, 9999999999)
        con.execute("INSERT INTO storage_posts_sending "
                      "(sending_id, user_id, post_id, msgid, current_state, datetime) "
                      "VALUES (?, ?, ?, ?, ?, ?)",
                      [sending_id, user_id, post_id, msgid, current_state, dt])
        con.commit()

# Добавление рейтинга товара
def add_ratex(position_id, user_id, rate):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_rate "
                    "(rate_id, position_id, user_id, rate, datetime) "
                    "VALUES (?, ?, ?, ?, ?)",
                    [random.randint(1000000000, 9999999999), position_id, user_id, rate, get_unix()])
        con.commit()

#create_seller_request('919148970')
####################################################################################################
########################################### ЗАПРОСЫ К БД ###########################################

# Добавление пользователя
def add_userx(user_id, user_login, user_name, user_lang, user_role):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_users "
                    "(user_id, user_login, user_name, user_lang, user_role, user_balance, user_refill, user_date, user_unix) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, user_lang, user_role, 0, 0, get_date(), get_unix()])
        con.commit()


# Получение платежных реквизитов продавца
def get_user_language(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM storage_users WHERE user_id = ?", [user_id]).fetchone()

# Получение платежных реквизитов продавца
def get_user_lang(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT user_lang FROM storage_users WHERE user_id = ?", [user_id]).fetchone()

# Добавление пользователя
def add_userxo(user_id, user_login, user_name):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_users "
                    "(user_id, user_login, user_name, user_balance, user_refill, user_date, user_unix) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, 0, 0, get_date(), get_unix()])
        con.commit()

# Получение пользователя
def get_userxn(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users WHERE user_city_id IS NULL"
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql).fetchall()

# Получение пользователя
def get_userxxx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT user_id FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение пользователя
def get_userx_idname():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT user_id, user_name FROM storage_users"
        return con.execute(sql).fetchall()

def get_userx_name(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT user_name FROM storage_users WHERE user_id = ?", [user_id]).fetchone()

# Получение пользователя
def get_userxx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение пользователя
def get_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение админов магазинов
def get_shopadmins(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT user_id FROM storage_users WHERE user_role='ShopAdmin'"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение пользователей
def get_usersx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение всех пользователей
def get_all_usersx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        return con.execute(sql).fetchall()

# Получение всех пользователей
def get_all_usersxx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users WHERE user_city_id IS NOT NULL"
        return con.execute(sql).fetchall()

# Получение всех пользователей
def get_top_sellersx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users WHERE user_role='ShopAdmin' AND user_balance >0 ORDER BY user_balance DESC LIMIT 0,15"
        return con.execute(sql).fetchall()

# Редактирование пользователя
def update_refillx(receipt, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_refill SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(receipt)
        con.execute(f"{sql}WHERE refill_receipt = ?", parameters)
        con.commit()



# Редактирование пользователя
def update_userx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_users SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(f"{sql}WHERE user_id = ?", parameters)
        con.commit()

# Редактирование пользователя
def update_holdx(order_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_money_holds SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(order_id)
        con.execute(f"{sql}WHERE order_id = ?", parameters)
        con.commit()

# Удаление пользователя
def delete_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

# Получение платежных реквизитов продавца
def get_tron_profile(user_id, type_net):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        parameters = [user_id, type_net]
        return con.execute("SELECT tron_wallet, type_net, tron_secret_key FROM storage_payment WHERE user_id = ? AND type_net =?", parameters).fetchone()

# Получение платежных реквизитов продавца
def get_upaymentx(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM storage_payment WHERE user_id = ?", [user_id]).fetchone()

def get_upaycount(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT COUNT(*) as paycount FROM storage_payment WHERE user_id = ?", [user_id]).fetchone()


# Редактирование платежных систем
def update_tron_profile(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_payment SET "
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(f"{sql} WHERE user_id = ?", parameters)
        con.commit()

#Получение адреса трон плошадки
def get_system_tron_address():
    with sqlite3.connect(PATH_DATABASE) as con:
        print(user_id)
        con.row_factory = dict_factory
        sql = "SELECT tron_address FROM storage_crypto_payment WHERE private_key='Admin' and type_net='USDT'"
        return con.execute(sql).fetchone()

#Получение адреса трон плошадки
def get_system_crypto_address(type_net):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT tron_address FROM storage_crypto_payment WHERE private_key='Admin' and type_net=?"
        return con.execute(sql, [type_net]).fetchone()

#Получение адреса трон
def get_tron_address(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        print(user_id)
        con.row_factory = dict_factory
        sql = "SELECT tron_address FROM storage_crypto_payment WHERE user_id=?"
        return con.execute(sql, [user_id]).fetchone()

#Получение адреса трон
def get_crypto_address(user_id, crypto_coin):
    with sqlite3.connect(PATH_DATABASE) as con:
        print(user_id)
        con.row_factory = dict_factory
        sql = "SELECT tron_address FROM storage_crypto_payment WHERE user_id=? AND type_net=?"
        return con.execute(sql, [user_id, crypto_coin]).fetchone()

def create_crypto_payment_row(user_id, tron_address, crypto_net):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_crypto_payment "
                    "(user_id, tron_address, type_net)"
                    "VALUES (?, ?, ?)",
                    [user_id, tron_address, crypto_net])
        con.commit()

# Редактирование платежных систем
def update_crypto_address(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_crypto_payment SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(f"{sql}WHERE user_id = ?", parameters)
        con.commit()


def create_upayments_row(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_payment "
                    "(qiwi_login, qiwi_token, qiwi_secret, qiwi_nickname, way_form, way_number, way_nickname, user_id, yoo_token, yoo_client_id, yoo_redirect_url, yoo_acc_number, way_formy)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    ['', '', '', '', 'False', 'False', 'False', user_id, '', 0, '', 0, 'False'])
        con.commit()

# Получение платежных систем
def get_paymentx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_payment WHERE user_id=919148970"
        return con.execute(sql).fetchone()


# Редактирование платежных систем
def update_paymentx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_payment SET"
        sql, parameters = update_format(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

# Редактирование платежных систем
def update_upaymentx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_payment SET "
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(f"{sql} WHERE user_id = ?", parameters)
        con.commit()

# Получение настроек
def get_settingsx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_settings"
        return con.execute(sql).fetchone()


# Редактирование настроек
def update_settingsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_settings SET"
        sql, parameters = update_format(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Добавление пополнения
def add_refillx(user_id, user_login, user_name, refill_comment, refill_amount, refill_receipt,
                refill_way, refill_date, refill_unix, refill_state):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_refill "
                    "(user_id, user_login, user_name, refill_comment, refill_amount, refill_receipt, refill_way, refill_date, refill_unix, refill_stat) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, refill_comment, refill_amount, refill_receipt, refill_way,
                     refill_date, refill_unix, refill_state])
        con.commit()

# Добавление пополнения
def add_prepay(pay_user_id, type_net, coinprice, pay_amount, priceincoin, receipt):
    with sqlite3.connect(PATH_DATABASE) as con:
        a = D(coinprice)
        b = D(pay_amount)
        c = D(priceincoin)
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_prepay "
                    "(pay_user_id, type_net, coinprice, pay_amount, priceincoin, receipt) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    [(pay_user_id, type_net, a, b, c, receipt)])
        con.commit()

# Получение препополнения
def get_refillx2(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_prepay"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение пополнения
def get_refillx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_refill"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение пополнения
def get_refill2x(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_refill"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение пополнений
def get_refillsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_refill"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех пополнений
def get_all_refillx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_refill"
        return con.execute(sql).fetchall()


# Добавление категории
def add_categoryx(category_name):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_category (category_id, level, parent_id, category_name) VALUES (?, ?, ?, ?)",
                    [random.randint(1000000000, 9999999999), 1, 0, category_name])
        con.commit()


# Изменение категории
def update_categoryx(category_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_category SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(category_id)
        con.execute(f"{sql}WHERE category_id = ?", parameters)
        con.commit()


# Получение категории
def get_category_people(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM cls_categories"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение категории
def get_categoryx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_category"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение категорий
def get_categoriesx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_category"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение всех категорий
def get_all_shopx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_shop"
        return con.execute(sql).fetchall()

# Получение магазина
def get_eventxx(**kwargs):
    print('Получение магазина api_sqlite.py 581')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_events"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение магазина
def get_promocodex(**kwargs):
    print('Получение магазина api_sqlite.py 581')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_promocode"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение магазина
def get_shopsxy():
    print('Получение магазина api_sqlite.py 844')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_shop"
        return con.execute(sql).fetchall()

# Получение магазина
def get_shopsxx(**kwargs):
    print('Получение магазина api_sqlite.py 318')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_shop"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение магазина
def get_artistsxx(**kwargs):
    print('Получение артистов по критериям api_sqlite.py 318')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_artists"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение платежных реквизитов продавца
def get_my_shopx(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_shop "
        #sql, parameters = update_format(sql, kwargs)
        return con.execute(sql, "WHERE admin = ?", [user_id]).fetchall()

# Получение платежных реквизитов продавца
def get_my_shopx2(admin):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_shop "
        #sql, parameters = update_format(sql, kwargs)
        return con.execute(sql, "WHERE admin = ?", [admin]).fetchone()

# Получение всех категорий
def get_all_categoriespx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM cls_categories"
        return con.execute(sql).fetchall()

# Получение всех категорий
def get_all_categoriesx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_category"
        return con.execute(sql).fetchall()

# Получение всех категорий
def get_all_events():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_events a LEFT JOIN storage_places b USING(place_id) ORDER BY datetime(event_date) ASC"
        return con.execute(sql).fetchall()

# Получение всех категорий
def get_all_places():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_places"
        return con.execute(sql).fetchall()

# Удаление всех категорий
def clear_categoryx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_category"
        con.execute(sql)
        con.commit()

# Удаление категории
def remove_categoryx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_category"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

# Добавление магазина
def add_artistx(name, description, webadress, admin, logo, city, geocode, city_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_artists (artist_id, name, description, webaddress, admin, logo, city, geocode, city_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [random.randint(1000000000, 9999999999), name, description, webadress, admin, logo, city, geocode, city_id])
        con.commit()

# Добавление магазина
def add_eventx(name, description, webadress, event_user_id, logo, city, geocode, city_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_events (event_id, event_name, event_description, webaddress, event_user_id, event_photo, event_city, geocode, event_city_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [random.randint(1000000000, 9999999999), name, description, webadress, event_user_id, logo, city, geocode, city_id])
        con.commit()

# Добавление категории ? позиции
def add_position_vacx(position_id, position_type, position_photo, position_description, position_user_id, position_state, vacs_url):
#def add_position_vacx(position_id, position_city, position_city_id, position_name, position_price, position_type, position_rest, position_description, position_photo, category_id, store_id, position_user_id, position_source, position_local):
    print('Добавление позиции  api_sqlite_shop.py  294')
    with sqlite3.connect(PATH_DATABASE) as con:

        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_position "
                    "(position_id, position_type, position_photo, position_description, position_user_id, position_date, position_state, vacs_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    [position_id, position_type, position_photo, position_description, position_user_id, get_date(), position_state, vacs_url])
        con.commit()
        print(position_id)

# Добавление категории ? позиции
def add_positionx(position_id, position_city, position_city_id, position_name, position_price, position_type, position_rest, position_description, position_photo, category_id, store_id, position_user_id, position_source, position_local):
    print('Добавление позиции  api_sqlite_shop.py  294')
    with sqlite3.connect(PATH_DATABASE) as con:

        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_position "
                    "(position_id, position_name, position_price, position_type, position_rest, position_description, position_photo, position_date, category_id, position_city, store_id, position_city_id, position_user_id, source, local) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [position_id, position_name, position_price, position_type, position_rest, position_description,
                     position_photo, get_date(), category_id, position_city, store_id, position_city_id, position_user_id, position_source, position_local])
        con.commit()
        print(position_id)


# Изменение позиции
def update_shopx(shop_id, **kwargs):
    print('Изменение позиции api_sqlite.py 306')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_shop SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(shop_id)
        con.execute(f"{sql}WHERE shop_id = ?", parameters)
        con.commit()

# Изменение позиции
def update_positionx(position_id, **kwargs):
    print('Изменение позиции api_sqlite.py 306')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_position SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(position_id)
        con.execute(f"{sql}WHERE position_id = ?", parameters)
        con.commit()

# Изменение позиции
def update_artistx(artist_id, **kwargs):
    print('Изменение артиста api_sqlite.py 306')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_artists SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(artist_id)
        con.execute(f"{sql}WHERE artist_id = ?", parameters)
        con.commit()

# Получение магазина
def get_placesx(**kwargs):
    print('Получение магазина api_sqlite.py 642')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_places"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение магазина
def get_shopx(**kwargs):
    print('Получение магазина api_sqlite.py 642')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_shop"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение позиции
def get_artistx(**kwargs):
    print('Получение позиции api_sqlite.py 318')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_artists"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение позиции
def get_new_positionx():
    print('Получение позиции api_sqlite.py 318')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position WHERE position_id>709"
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql).fetchall()

# Получение позиции
def get_positionx(**kwargs):
    print('Получение позиции api_sqlite.py 318')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение сообщений для пользователя
def get_user_messagesx(**kwargs):
    print('Получение сообющений для пользователя api_sqlite.py  367')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_messages"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Обмновление статуса сообщения
def update_orderx(order_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_orders SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(order_id)
        con.execute(f"{sql}WHERE order_id = ?", parameters)
        con.commit()

# Изменение корзины
def update_orderx(order_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_orders SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(order_id)
        con.execute(f"{sql}WHERE order_id = ?", parameters)
        con.commit()

# Изменение холда
def update_holdsx(order_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_money_holds SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(order_id)
        con.execute(f"{sql}WHERE order_id = ?", parameters)
        con.commit()

# Получение продавцов корзины
def get_cart_sellersx(order_id):
    print('Получение продавцов корзины api_sqlite.py  777')
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sellers = con.execute(
            "SELECT DISTINCT owner_uid FROM storage_orders_items WHERE order_id = ?",
            [order_id],
        ).fetchall()
        print(len(sellers))
        slss=''
        slsss = ''.join(sellers)
        print(slsss)
        slsss1 = slsss.replace('(', '')
        slsss2 = slsss1.replace(')', '')
        return slsss2.replace(',', '')


# Получение позиций корзины
def get_cart_positionsx(order_id):
    print('Получение позиций корзины  api_sqlite.py  568')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute(
            "SELECT * FROM storage_orders_items LEFT JOIN storage_position USING(position_id) WHERE order_id = ?",
            [order_id],
        ).fetchall()

# Получение позиций корзины
def get_order_sellers(order_id):
    print('Получение позиций корзины  api_sqlite.py  568')
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        positions = con.execute(
            "SELECT DISTINCT owner_uid as owner_id FROM storage_orders_items WHERE order_id = ?",
            [order_id],
        ).fetchall()
        return json.dumps(positions)
        #return positions


# Получение данных холдов заказа
def get_orders_holdsx(order_id):
    print(f'Получение холдов заказа {order_id} 626')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute(
            "SELECT * FROM storage_money_holds WHERE order_id = ?", [order_id]
        ).fetchall()

# Получение позиций
def get_positionsax(category_id, position_city_id):
    print('Получение позиций (дубль)  api_sqlite.py  1272')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position WHERE category_id=? AND position_city_id=?"
        #sql, parameters = update_format_args(sql, kwargs)  OR category_id=? AND local=1
        return con.execute(sql, [category_id, position_city_id]).fetchall()

# Получение позиций
def get_positionsx(**kwargs):
    print('Получение позиций (дубль)  api_sqlite.py  1002')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение всех моих позиций
def get_positionsorder(category_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute(
            "SELECT * FROM storage_position WHERE сategory_id = ? ORDER BY position_name ASC",
            [category_id],
        ).fetchall()

# Получение всех категорий
def get_all_positionsidx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT position_id FROM storage_position"
        return con.execute(sql).fetchall()

# Получение всех категорий
def get_all_positionsx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position"
        return con.execute(sql).fetchall()


# Удаление всех позиций
def clear_positionx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_position"
        con.execute(sql)
        con.commit()

# Удаление позиции
def remove_shopx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_shop"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Удаление позиции
def remove_artistx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_artists"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()

# Удаление позиции
def remove_positionx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Добавление товара
def add_itemx(category_id, position_id, get_all_items, user_id, user_name):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory

        for item_data in get_all_items:
            if not item_data.isspace() and item_data != "":
                con.execute("INSERT INTO storage_item "
                            "(item_id, item_data, position_id, category_id, creator_id, creator_name, add_date) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?)",
                            [random.randint(1000000000, 9999999999), clear_html(item_data.strip()), position_id, category_id,
                             user_id, user_name, get_date()])
        con.commit()


# Изменение товара
def update_itemx(item_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_item SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(item_id)
        con.execute(f"{sql}WHERE item_id = ?", parameters)
        con.commit()

# Получение продавца заказа
def get_ordersellerx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение товара
def get_itemx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение товаров
def get_itemsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        rows = con.execute(sql, parameters).fetchall()
        return 0 if rows is None else rows

# Получение всех товаров
def get_all_itemsx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_item"
        return con.execute(sql).fetchall()

# Получение всех моих позиций
def get_all_my_positionsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(f"{sql}WHERE position_user_id = ?", [user_id]).fetchall()

# Получение всех моих позиций
def get_all_my_positionsnx(position_user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position"
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(
            f"{sql} WHERE position_user_id = ?", [position_user_id]
        ).fetchall()

# Получение всех моих товаров
def get_all_my_itemsnx(creator_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_item"
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(f"{sql} WHERE creator_id = ?", [creator_id]).fetchall()

# Получение всех моих товаров
def get_all_my_itemsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(f"{sql}WHERE creator_id = ?", [user_id]).fetchall()


# Очистка товаров
def clear_itemx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_item"
        con.execute(sql)
        con.commit()


# Удаление товаров
def remove_itemx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Покупка товаров
def buy_itemx(get_items, get_count):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        split_len, send_count, save_items = 0, 0, []

        for select_send_item in get_items:
            if send_count == get_count:
                break
            send_count += 1
            select_data = (
                f"{send_count}. {select_send_item['item_data']}"
                if get_count >= 2
                else select_send_item['item_data']
            )
            save_items.append(select_data)
            sql, parameters = update_format_args("DELETE FROM storage_item",
                                                 {"item_id": select_send_item['item_id']})
            con.execute(sql, parameters)

            if len(select_data) >= split_len: split_len = len(select_data)
        con.commit()

        split_len += 1
        get_len = math.ceil(3500 / split_len)

    return save_items, send_count, get_len

# Проверка существования заказа
def get_orderx(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute(
            "SELECT * FROM storage_orders WHERE user_id = ?", [user_id]
        ).fetchone()

# Проверка существования заказа
def get_orderxo(order_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute("SELECT * FROM storage_orders WHERE order_id = ?", [order_id]).fetchone()

# Последние 10 покупок
def get_alladmin_orderx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT DISTINCT b.order_id, b.order_state FROM storage_orders b"
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql).fetchall()

# Последние 10 покупок
def get_order_items(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_orders_items"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Последние 10 покупок
def get_seller_orderx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT DISTINCT a.order_id, a.owner_uid, b.order_state, count(DISTINCT a.owner_uid) as selbyo FROM storage_orders_items a LEFT JOIN storage_orders b USING(order_id) GROUP BY a.order_id"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Последние 10 покупок
def get_params_orderxx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_orders LEFT JOIN storage_orders_items USING(order_id)"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Последние 10 покупок
def get_params_orderx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_orders"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Проверка существования заказа
def get_userc_orderx(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        #con.row_factory = dict_factory
        sql = "SELECT order_state FROM storage_orders WHERE order_state='created' AND user_id = ?"
        order = con.execute(sql, [user_id]).fetchone()
        order=json.dumps(order)
        print(order)
        return order

# Проверка существования заказа
def get_user_orderx(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute(
            "SELECT * FROM storage_orders WHERE user_id = ?", [user_id]
        ).fetchone()


# Создание заказа
def create_orderx(user_id, user_login, user_name, order_state, order_date, order_unix):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_orders "
                    "(user_id, user_login, user_name, order_state, order_date, order_unix) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, order_state, order_date, order_unix])
        con.commit()

# Создание холда
def create_holdx(order_id, buyer, seller, amount, validity, state):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_money_holds "
                    "(order_id, buyer, seller, amount, validity, state) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    [order_id, buyer, seller, amount, validity, state])
        con.commit()

# Добавление товара в заказ
def add_order_itemx(user_id, order_id, position_id, count, price, receipt, owner_uid):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_orders_items "
                    "(user_id, order_id, position_id, count, price, receipt, owner_uid) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [user_id, order_id, position_id, count, price, receipt, owner_uid])
        con.commit()


# Добавление сообщения
def add_messagex(from_id, to_id, order_id, txtmessage, photo, state):
    print('Добавление позиции api_sqlite_shop.py  294')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_messages "
                    "(message_id, from_uid, to_uid, order_id, message, photo, state) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [random.randint(1000000000, 9999999999), from_id, to_id, order_id, txtmessage, photo, state])
        con.commit()

def get_params_messagesx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_messages"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Добавление покупки
def add_purchasex(user_id, user_login, user_name, purchase_receipt, purchase_count, purchase_price, purchase_price_one,
                  purchase_position_id, purchase_position_name, purchase_item, purchase_date, purchase_unix,
                  balance_before, balance_after):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_purchases "
                    "(user_id, user_login, user_name, purchase_receipt, purchase_count, purchase_price, purchase_price_one, purchase_position_id, "
                    "purchase_position_name, purchase_item, purchase_date, purchase_unix, balance_before, balance_after) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, purchase_receipt, purchase_count, purchase_price,
                     purchase_price_one, purchase_position_id, purchase_position_name, purchase_item, purchase_date,
                     purchase_unix, balance_before, balance_after])
        con.commit()



# Получение покупок
def get_purchasesbysellers():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT DISTINCT c.user_id FROM storage_purchases a LEFT JOIN storage_position b ON(a.purchase_position_id=b.position_id) LEFT JOIN storage_users c ON(c.user_id=b.position_user_id) WHERE c.user_id NOT NULL GROUP BY a.user_id, a.purchase_position_name"
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql).fetchall()


# Получение покупок
def get_purchasesxx2(user_id):
    #with sqlite3.connect(PATH_DATABASE) as con:
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = "SELECT c.user_id, a.purchase_position_name, SUM(a.purchase_count) as counts, SUM(a.purchase_price) as price FROM storage_purchases a LEFT JOIN storage_position b ON(a.purchase_position_id=b.position_id) LEFT JOIN storage_users c ON(c.user_id=b.position_user_id) WHERE c.user_id=? GROUP BY a.user_id, a.purchase_position_name"
    #result = cur.execute(query, (user_id,)).fetchall()
    result = cur.execute(query, [user_id]).fetchall()
    cur.close()
    return result

def get_purchasesx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_purchases"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

    # Получение покупок
def get_purchasesxx3(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        #cur = conn.cursor()
        sql = "SELECT c.user_id, a.purchase_position_name, SUM(a.purchase_count) as counts, SUM(a.purchase_price) as price FROM storage_purchases a LEFT JOIN storage_position b ON(a.purchase_position_id=b.position_id) LEFT JOIN storage_users c ON(c.user_id=b.position_user_id) WHERE c.user_id=? GROUP BY a.user_id, a.purchase_position_name"
        sql, parameters = update_format_args(sql, [user_id])
        return con.execute(sql, parameters).fetchall()


def get_purchasesxx(user_id):
    print('возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    #cur = conn.cursor()
    query = '''SELECT c.user_id, a.purchase_position_name, SUM(a.purchase_count) as counts, SUM(a.purchase_price) as price FROM storage_purchases a LEFT JOIN storage_position b ON(a.purchase_position_id=b.position_id) LEFT JOIN storage_users c ON(c.user_id=b.position_user_id) WHERE c.user_id=? GROUP BY a.user_id, a.purchase_position_name'''
    return conn.execute(query, (user_id,)).fetchall()

# Получение запросов
def get_requestx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_requests"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение всех покупок
def get_all_purchasesx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_purchases"
        return con.execute(sql).fetchall()

# Получение всех покупок
def getpurchasesbysellersx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_purchases LEFT JOIN storage_position USING(user_id)"
        return con.execute(sql).fetchall()


# Последние 10 покупок
def last_purchasesx(user_id, count):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_purchases WHERE user_id = ? ORDER BY increment DESC LIMIT {count}"
        return con.execute(sql, [user_id]).fetchall()


# Создание всех таблиц для БД
def create_dbx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory

        # Создание БД с хранением данных пользователей
        if len(con.execute("PRAGMA table_info(storage_users)").fetchall()) == 12:
            print("DB was found(1/12)")
        else:
            con.execute("CREATE TABLE IF NOT EXISTS storage_users("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_login TEXT,"
                        "user_name TEXT,"
                        "user_address TEXT,"
                        "user_phone TEXT,"
                        "user_balance INTEGER,"
                        "user_refill INTEGER,"
                        "user_date TIMESTAMP,"
                        "user_unix INTEGER,"
                        "user_city TEXT,"
                        "user_geocode TEXT,"
                        "user_role TEXT,"
                        "user_city_id INTEGER)")  # Добавил город
            print("DB was not found(1/12) | Creating...")

        # Создание БД с хранением данных платежных систем
        if len(con.execute("PRAGMA table_info(storage_payment)").fetchall()) == 18:
            print("DB was found(2/12)")
        else:
            con.execute("CREATE TABLE IF NOT EXISTS storage_payment("
                        "qiwi_login TEXT,"
                        "qiwi_token TEXT,"
                        "qiwi_secret TEXT,"
                        "qiwi_nickname TEXT,"
                        "way_form TEXT,"
                        "way_number TEXT,"
                        "way_nickname TEXT,"
                        "way_formy TEXT,"
                        "user_id INTEGER,"
                        "yoo_token TEXT,"
                        "yoo_client_id TEXT,"
                        "yoo_redirect_url TEXT,"
                        "yoo_acc_number INTEGER,"
                        "coinbase_key TEXT,"
                        "coinbase_secret TEXT,"
                        "way_coinbase TEXT,"
                        "way_freecredi TEXT)")

            con.execute("INSERT INTO storage_payment("
                        "qiwi_login, qiwi_token, qiwi_secret, qiwi_nickname, way_form, way_number, way_nickname, way_formy, yoo_token, yoo_client_id, yoo_redirect_url, yoo_acc_number) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        ['None', 'None', 'None', 'None', 'False', 'False', 'False', 'False', 'None', 'None', 'None', 'None'])
            print("DB was not found(2/12) | Creating...")

        # Создание БД с хранением настроек
        if len(con.execute("PRAGMA table_info(storage_settings)").fetchall()) == 10:
            print("DB was found(3/12)")
        else:
            con.execute("CREATE TABLE storage_settings("
                        "status_work TEXT,"
                        "status_refill TEXT,"
                        "status_buy TEXT,"
                        "misc_faq TEXT,"
                        "misc_support TEXT,"
                        "misc_bot TEXT,"
                        "misc_update TEXT,"
                        "misc_profit_day INTEGER,"
                        "misc_profit_week INTEGER,"
                        "type_trade TEXT)")

            con.execute("INSERT INTO storage_settings("
                        "status_work, status_refill, status_buy, misc_faq, misc_support, misc_bot, misc_update, misc_profit_day, misc_profit_week)"
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        ["True", "False", "False", "None", "None", "None", "False", get_unix(), get_unix()])
            print("DB was not found(3/12) | Creating...")

        # Создание БД с хранением пополнений пользователей
        if len(con.execute("PRAGMA table_info(storage_refill)").fetchall()) == 11:
            print("DB was found(4/12)")
        else:
            con.execute("CREATE TABLE storage_refill("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_login TEXT,"
                        "user_name TEXT,"
                        "refill_comment TEXT,"
                        "refill_amount INTEGER,"
                        "refill_receipt TEXT,"
                        "refill_way TEXT,"
                        "refill_date TIMESTAMP,"
                        "refill_unix INTEGER,"
                        "refill_state TEXT)")
            print("DB was not found(4/12) | Creating...")

        # Создание БД с хранением категорий
        if len(con.execute("PRAGMA table_info(storage_category)").fetchall()) == 5:
            print("DB was found(5/8)")
        else:
            con.execute("CREATE TABLE storage_category("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "level INTEGER,"
                        "parent_id INTEGER,"
                        "category_id INTEGER,"
                        "category_name TEXT)")
            print("DB was not found(5/12) | Creating...")


        # Создание БД с хранением позиций
        if len(con.execute("PRAGMA table_info(storage_position)").fetchall()) == 11:
            print("DB was found(6/12)")
        else:
            con.execute("CREATE TABLE IF NOT EXISTS storage_position("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "position_id INTEGER,"
                        "position_name TEXT,"
                        "position_price INTEGER,"
                        "position_description TEXT,"
                        "position_photo TEXT,"
                        "position_date TIMESTAMP,"
                        "category_id INTEGER,"
                        "store_id INTEGER,"
                        "position_city TEXT,"
                        "position_city_id INTEGER)")
            print("DB was not found(6/12) | Creating...")

        # Создание БД с хранением товаров
        if len(con.execute("PRAGMA table_info(storage_item)").fetchall()) == 9:
            print("DB was found(7/12)")
        else:
            con.execute("CREATE TABLE IF NOT EXISTS storage_item("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "item_id INTEGER,"
                        "item_data TEXT,"
                        "position_id INTEGER,"
                        "category_id INTEGER,"
                        "shop_id INTEGER,"
                        "creator_id INTEGER,"
                        "creator_name TEXT,"
                        "add_date TIMESTAMP)")
            print("DB was not found(7/12) | Creating...")

        # # Создание БД с хранением покупок
        if len(con.execute("PRAGMA table_info(storage_purchases)").fetchall()) == 15:
            print("DB was found(8/12)")
        else:
            con.execute("CREATE TABLE IF NOT EXISTS storage_purchases("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_login TEXT,"
                        "user_name TEXT,"
                        "purchase_receipt TEXT,"
                        "purchase_count INTEGER,"
                        "purchase_price INTEGER,"
                        "purchase_price_one INTEGER,"
                        "purchase_position_id INTEGER,"
                        "purchase_position_name TEXT,"
                        "purchase_item TEXT,"
                        "purchase_date TIMESTAMP,"
                        "purchase_unix INTEGER,"
                        "balance_before INTEGER,"
                        "balance_after INTEGER)")
            print("DB was not found(8/12) | Creating...")

            if len(con.execute("PRAGMA table_info(storage_shop)").fetchall()) == 3:
                print("DB was not found(9/12) | Creating...")
            else:
                # Создание БД с хранением магазинов
                con.execute("CREATE TABLE IF NOT EXISTS storage_shop("
                            "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "shop_id INTEGER,"
                            "shop_name TEXT)")

            # # Создание БД с хранением покупок
            if len(con.execute("PRAGMA table_info(storage_purchases)").fetchall()) == 15:
                print("DB was found(10/12)")
            else:
                con.execute("CREATE TABLE IF NOT EXISTS storage_purchases("
                            "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "user_id INTEGER,"
                            "user_login TEXT,"
                            "user_name TEXT,"
                            "purchase_receipt TEXT,"
                            "purchase_count INTEGER,"
                            "purchase_price INTEGER,"
                            "purchase_price_one INTEGER,"
                            "purchase_position_id INTEGER,"
                            "purchase_position_name TEXT,"
                            "purchase_item TEXT,"
                            "purchase_date TIMESTAMP,"
                            "purchase_unix INTEGER,"
                            "balance_before INTEGER,"
                            "balance_after INTEGER)")
            print("DB was not found(10/12) | Creating...")

            if len(con.execute("PRAGMA table_info(storage_orders)").fetchall()) == 15:
                print("DB was found(11/12)")
            else:
                con.execute("CREATE TABLE IF NOT EXISTS storage_orders("
                            "order_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "user_id INTEGER,"
                            "user_login TEXT,"
                            "user_name TEXT,"
                            "order_date TEXT,"
                            "order_state INTEGER,"
                            "order_unix INTEGER,"
                            "phone TEXT,"
                            "address TEXT)")

            print("DB was not found(11/12) | Creating...")

            if len(con.execute("PRAGMA table_info(storage_orders_items)").fetchall()) == 7:
                print("DB was found(12/12)")
            else:
                con.execute("CREATE TABLE IF NOT EXISTS storage_orders_items("
                            "order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "order_id INTEGER,"
                            "position_id INTEGER,"
                            "user_name TEXT,"
                            "count INTEGER,"
                            "price INTEGER,"
                            "receipt INTEGER)")

            print("DB was not found(12/12) | Creating...")


        con.commit()


# ================================================================================================================
# ==========                  Новые функции 11.08.22                            ==================================

# возвращает город пользователя и координаты
def get_city_user(user_id):
    print('возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select user_city_id from storage_users where user_id = ?'''
    result = cur.execute(query, (user_id,)).fetchone()
    cur.close()
    print(result)
    return result

# возвращает город пользователя и координаты
def get_user_city(user_id):
    print('возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select user_city, user_city_id from storage_users where user_id = ?'''
    result = cur.execute(query, (user_id,)).fetchone()
    cur.close()
    print(result)
    return result

# возвращает город пользователя и координаты
def get_parent_cat(category_id):
    print('возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select parent_id from cls_categories where category_id = ?'''
    result = cur.execute(query, (category_id,)).fetchone()
    cur.close()
    return result

# возвращает город пользователя и координаты
def get_parent_catc(category_id):
    print('возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select parent_id from storage_category where category_id = ?'''
    result = cur.execute(query, (category_id,)).fetchone()
    cur.close()
    return result

# возвращает город пользователя и координаты
def get_city_user3(user_id):
    print('возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select user_city, user_geocode, user_city_id from storage_users where user_id = ?'''
    result = cur.execute(query, (user_id,)).fetchone()
    cur.close()
    return result

# возвращает город пользователя и координаты
def get_city_artist(artist_id):
    print('возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select city, geocode, city_id from storage_artists where artist_id = ?'''
    result = cur.execute(query, (artist_id,)).fetchone()
    cur.close()
    print(result)
    return result


# возвращает город пользователя и координаты
def get_citytext_user(user_id):
    print('возвращает город пользователя и координаты api_sqlite.py 675')
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select user_city from storage_users where user_id = ?'''
    result = cur.execute(query, (user_id,)).fetchone()
    cur.close()
    return result


# позиции по городу и категории
def get_shops_on_city(city):
    print('позиции по городу и магазину api_sqlite.py 686')
    if city is None or city == 0:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_shop'''
        result = cur.execute(query).fetchall()
    else:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position left join storage_shop on(storage_position.store_id=storage_shop.shop_id) where position_city_id = ?'''
        items = [city]
        result = cur.execute(query, items).fetchall()

    cur.close()
    return result

# позиции по городу и категории
def get_paramposition_on_city(category_id, shop_id, city_id):
    print('позиции по городу и магазину api_sqlite.py 686')
    if city_id is None and shop_id != None:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position where store_id = ?'''
        result = cur.execute(query, (shop_id,)).fetchall()
        cur.close()
        print("|||VAR 1|||")
        return result
    elif city_id is None and category_id != None:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position where category_id = ?'''
        result = cur.execute(query, (catgory_id,)).fetchall()
        cur.close()
        print("|||VAR 2|||")
        return result
    elif shop_id is None:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position where position_city_id = ?'''
        items = [city_id]
        result = cur.execute(query, items).fetchall()
        cur.close()
        print("|||VAR 3|||")
        return result
    elif shop_id != '' and city_id != '':
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position where store_id = ? and position_city_id = ?'''
        items = [shop_id, city_id]
        result = cur.execute(query, items).fetchall()
        cur.close()
        print("|||VAR 4|||")
        return result


# позиции по городу и категории
def get_shopposition_on_city(shop_id, city_id):
    print('позиции по городу и магазину api_sqlite.py 686')
    if city_id == 0 or city_id is None:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position where store_id = ?'''
        result = cur.execute(query, (shop_id,)).fetchall()
    else:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position where store_id = ? and position_city_id = ?'''
        items = [shop_id, city_id]
        result = cur.execute(query, items).fetchall()

    cur.close()
    return result

# позиции по городу и категории
def get_position_in_city1(city):
    print('позиции по городу и магазину api_sqlite.py 686')
    if city is None or city == 0:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_shop'''
        result = cur.execute(query).fetchall()
    else:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position left join storage_shop on(storage_position.store_id=storage_shop.shop_id) where position_city_id = ?'''
        items = [city]
        result = cur.execute(query, items).fetchall()

    cur.close()
    return result

def get_cources_in_cityx(category_id, position_city_id, flagallc=1, position_type=1):
    print('Получение позиций api_sqlite.py 1749')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute(
            "SELECT DISTINCT position_id, position_name FROM storage_position WHERE flagallc=1 OR position_type=1 OR source=? AND category_id=? AND position_city_id=?",
            ["people", category_id, position_city_id],
        ).fetchall()

def get_people_positions_in_cityx(category_id, position_city_id, flagallc=1, position_type=1):
    print('Получение позиций api_sqlite.py 1749')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute(
            "SELECT DISTINCT position_id, position_name FROM storage_position WHERE flagallc=1 OR position_type=1 OR source=? AND category_id=? AND position_city_id=?",
            ["people", category_id, position_city_id],
        ).fetchall()

def get_positions_in_cityx(category_id, position_city_id): #, flagallc=1, position_type=1
    print('Получение позиций api_sqlite.py 1749')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute(
            "SELECT DISTINCT position_id, position_name, position_city_id FROM storage_position WHERE category_id=? AND position_city_id=?",
            [category_id, position_city_id],
        ).fetchall()
#flagallc=1 OR position_type=1 OR
def get_events_in_cityx(event_city_id, flagallc=1, position_type=1):
    print('Получение позиций api_sqlite.py 1749')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute(
            "SELECT DISTINCT event_id, event_name FROM storage_events WHERE flagallc=1 OR event_type=1 OR event_city_id=?",
            [event_city_id],
        ).fetchall()


def get_places_in_cityx(place_city_id, flagallc=1, position_type=1):
    print('Получение позиций api_sqlite.py 1749')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        return con.execute(
            "SELECT DISTINCT place_id, name, city_id FROM storage_places WHERE city_id=?",
            [place_city_id],
        ).fetchall()


# Получение всех категорий
def get_all_events():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_events a LEFT JOIN storage_places b USING(place_id) ORDER BY datetime(event_date) ASC"
        return con.execute(sql).fetchall()

# позиции по городу и категории
def get_position_on_city(category_id, city):
    print('позиции по городу и категории api_sqlite.py 686')
    if city is None:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position where category_id = ?'''
        result = cur.execute(query, (category_id,)).fetchall()
    else:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_position where category_id = ? and position_city_id = ?'''
        items = [category_id, city]
        result = cur.execute(query, items).fetchall()

    cur.close()
    return result

def get_eventx(event_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select distinct c.place_id, c.name
        from storage_places c join storage_events e on c.place_id=e.place_id where event_id = ? order by c.name asc'''
    return cur.execute(query, (event_id,)).fetchall()

# категории в городе
def get_events_in_place(place_id):
    if place_id is None:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select distinct * 
            from storage_places c join storage_events p on c.place_id=p.place_id order by c.name asc'''
        return cur.execute(query).fetchall()
    else:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select * from storage_events p where p.place_id = ?'''
        return cur.execute(query, (place_id,)).fetchall()


# категории в городе
def get_events_in_city(city_id):
    if city_id is None:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select distinct c.place_id, c.name
            from storage_places c join storage_events p on c.place_id=p.place_id order by c.name asc'''
        return cur.execute(query).fetchall()
    else:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select distinct c.place_id, c.name
            from storage_places c join storage_events p on c.place_id=p.place_id where event_city_id = ? order by c.name asc'''
        return cur.execute(query, (city_id,)).fetchall()

# категории в городе
def get_category_in_city(city_id):
    if city_id is None:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select distinct c.category_id, c.category_name
            from storage_category c join storage_position p on c.category_id=p.category_id order by c.category_name asc'''
        return cur.execute(query).fetchall()
    else:
        conn = sqlite3.connect(PATH_DATABASE)
        cur = conn.cursor()
        query = '''select distinct c.category_id, c.category_name
                from storage_category c join storage_position p on c.category_id=p.category_id where position_city_id = ? order by c.category_name asc'''
        return cur.execute(query, (city_id,)).fetchall()

def get_category_in_citypx(**kwargs):
    print('Получение категорий api_sqlite.py 1816')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT DISTINCT category_id, level, parent_id, category FROM cls_categories"
        sql, parameters = update_format_or_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

def get_curcategory_in_citypx(**kwargs):
    print('Получение категорий курсов api_sqlite.py 2831')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT DISTINCT category_id, level, parent_id, category FROM cls_curcategories"
        sql, parameters = update_format_or_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


def get_categories_in_cityx(parent_id, position_city_id):
    print('Получение категорий api_sqlite.py 2235')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT DISTINCT c.category_id, c.level, c.parent_id, c.category_name FROM storage_category c LEFT JOIN storage_position p ON c.category_id=p.category_id WHERE p.local=1 OR p.position_city_id=? AND c.parent_id=?"
        return con.execute(sql, [position_city_id, parent_id]).fetchall()

def get_category_in_cityx(**kwargs):
    print('Получение категорий api_sqlite.py 1816')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT DISTINCT c.category_id, c.level, c.parent_id, c.category_name FROM storage_category c LEFT JOIN storage_position p ON c.category_id=p.category_id"
        sql, parameters = update_format_or_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

def get_shop_in_cityx(**kwargs):
    print('Получение категорий api_sqlite.py 1833')
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT DISTINCT c.shop_id, c.name FROM storage_shop c LEFT JOIN storage_position p ON c.shop_id=p.store_id"
        sql, parameters = update_format_or_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Последние 10 покупок
def get_eventsxx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_events"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()
