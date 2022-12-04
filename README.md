# TelegramGoodsInbot
A store with the functionality of multi-cities.
Бот - магазин в Телеграм с функциональностями:
- мульти-города и местонахождение покупателя.
- мульти-правдцов.
- индивидуальные реквизиты продавцов.
- безопасная сделка и корзина.
- 192 города России в справочнике


**Функции для пользователя**
- каталог двух уровней, категория - товар
- корзина
- поддержка (контакты) - ссылка в диалог с администратором
- FAQ - сообщение для пользователей с HTML разметкой
- подробная Статистика бота: кол-во пополнений, покупок, пользователей, позиций, категорий, чистой прибыли
- определение местонахождения пользователя


**Функции продавца**
- управление товарами
- добавление собственных реквизитов QIWI, YooMoney


**Функции администратора**
- режим технических работ
- проверка наличия обнолвения при запуске
- активация/деактивация функций продажи и оплаты
- добавление неограниченного количества глобальных администраторов
- согласование запросов на роль администратора магазина, управляющего своими товарами в каталоге
- добавление неограниченного количества администраторов магазинов
- удобная и многофункциональная админ панель
- определение и хранение города нахождения товара
- поиск покупателей и просмотр профилей
- поиск чеков покупок
- рассылка сообщений всем пользователям бота
- изменение и пополнение баланса пользователя
- отчет о продажах продавцов


**Оплата товаров**
- используется библиотеки QIWI и YooMoney
- настраивается администратором бота через админку
- проверка работоспособности из админки
- вывод баланса кошелька QIWI


**Каталог и товары**
- User-friendly каталог
- товары имеют одно изображение
- гибкое управление товарами администраторами
- выгрузка всех товаров


**Защита**
- админ-фильтры на все хендлеры, гарантирующие приватность админ функционала
- защита от оплаты в тенге при пополнении баланса
- защита от неправильного HTML синтаксиса
- защита от повторной выдачи баланса
- защита от спама в боте (Middlewares)


**Настройки settings.ini**
- установить токен Бота, полученный у @BotFather
- установить Telegram ID администратора


**Настройка**
1. Скопируйте папку бота. Перейдите в папку бота.
2. Выполните в командной строке "pip install -r requirements.txt".
2. Заполните файл settings.ini.
3. Стартовать бот. 
4. Заполнить информационные поля. 
5. Наполнить каталог товарами.
6. Привлекать пользователей в каталог.


**Процесс администрирования площадки**
1. Согласование продавцов
2. Администрирование каталога
3. Администрирование денежных средств
4. Поддержка и ведение сделок, разрешение споров


**Процесс покупки для покупателя**
1. Выбор товара. 
2. Пополнение счета. 
3. Ожидание звонка продавца и уточнение параметров домтааки. 
4. Получение товара. 
5. Подтверждение получения.
6. Отправка отзыва о покупателей.


**Процесс продажи для продавца**
1. Получение сообщения о заказе. 
2. Звонок покупателю. 
3. Отправка товара покупателю.
4. Получение отзыва о покупателей.


**PRO версия:**
- карточка магазина.
- три режима работы площадки: real | digital | hybrid.


**TODO:**
- карточка магазина.
- вывод средств продавцами.


Работающий экземпляр пока только по России в 192 городах; https://t.me/Goodsinbot
Чтобы торговать своими товарами в текущем экземпляре, отправьте запрос на продавца из бота, нажав "Я продавец".
Инструкция и описание находятся здесь: <a href='https://github.com/rashidovich2/TelegramGoodsInbot/wiki/Главная-TelegramGoodsinbot---меню-бота-для-разных-ролей'>Документация</a>
По вопросам пишите пожалуйста в телеграм: **@raclear**
