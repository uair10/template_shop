### Base messages ###
confirm-btn = ✅ Подтвердить
back-btn = ⬅️ Назад
main-menu-btn = ↪️ В главное меню

### Errors ###
wrong-file-extension = ❌ Поддерживаемые расширения файла: .xlsx

### DB errors ###
error-msg = ❗️ Что-то пошло не так
not-enough-balance =❗ Недостаточный баланс. Ваш баланс: { $balance } $
error-during-order-create =
    ❗ Ошибка при создании заказа
    Попробуйте еще раз или обратитесь в тех. поддержку
error-during-order-update =
    ❗ Ошибка при обновлении заказа
    Попробуйте еще раз или обратитесь в тех. поддержку
unknown-server-error = ❗️ Произошла ошибка на сервере
user-not-exists-msg = Пользователь не существует
user-already-exists-msg = Такой пользователь уже существует
order-already-exists-msg = Такой заказ уже существует
order-not-exists-msg = Заказ не существует


### Menu messages ###
welcome =
    Здравствуйте, { $user }!
    Чтобы начать, просто выберите нужную вам опцию.
buy-btn = 🛒 PSD шаблоны
profile-btn = 👤 Личный кабинет
change-lang-btn = 🌎 Change language
select-lang-msg = Выберите язык
admin-btn = ⚙️ Панель администратора

### Create Order ###
select-country-msg = Выберите страну
select-template-type-msg = Выберите тип шаблона
documents-btn = 🪪 Документы
cards-btn = 💳 Карты
select-category-msg = Выберите категорию
select-products-msg = Выберите товары
cart-total = Сумма корзины: { $cart_total }$
select-payment-method-msg = Выберите метод оплаты
clear-cart-btn = 🗑️ Очистить корзину
go-to-order-btn = Перейти в заказ

### Product info ###
product-title = Название: { $product_title }
product-price = Цена: { $product_price }$
add-to-cart-btn = 🛒 Купить шаблон
order-doc-drawing-btn = 🎨 Заказать отрисовку

### Account messages ###
your-account = <b>Ваш аккаунт {"\u000A"}</b>
your-balance = Ваш баланс: { $balance } $
your-orders-count = Заказов: { $orders_count }
registered_date = Зарегистрирован: { $reg_date }
add-balance-btn = 💵 Пополнить баланс
enter-promocode-btn = 📟 Ввести промокод
orders-btn = 🗂 Мои заказы
payments-btn = 📄 История платежей


### Payments messages ###
payment-history = Ваши платежи:
payment-details = Информация о платеже {"\u000A"}
payment_id = Номер платежа: { $payment_id }
payment_summ = Сумма платежа: { $payment_summ }
payment_status = Статус платежа: { $status }
created_at = Создан: { $created_at }
waiting_payment = Ожидает оплаты
paid = Оплачен
payment_failed = Не удалось оплатить
select-payment-method-msg = Выберите метод оплаты
select-payment-amount-rub-msg =
    Введите сумму пополнения в <b>долларах</b>, не больше 2 цифр после разделителя. Пример: 99.99 или 99
    {"\u000A"}Оплата происходит в рублях по курсу ЦБ РФ
    {"\u000A"}<b>Текущий курс:</b> { $usd_rate } руб. за $. Курс фиксируется на время оплаты
select-payment-amount-usd-msg =
    Введите сумму пополнения в <b>долларах</b>, не больше 2 цифр после разделителя. Пример: 99.99 или 99
qiwi-btn = Карта (QIWI)
crypto-btn = USDT
payment-msg =
    Оплатите счет, кликнув по кнопке "Оплатить"{"\u000A"}
    ℹ️ Если у вас есть промокод на бонус к пополнению, введите его до оплаты{"\u000A"}
    ❓ Если оплата не была подтверждена в течение 20 минут, обратитесь в тех.поддержку{"\u000A"}
    <a href="https://telegra.ph/Instrukciya-po-oplate-USDT-10-25">Инструкция по оплате</a>

payment-msg-in-order =
    {"\u000A"}<b>✅ После подтверждения оплаты нажмите на кнопку "Вернуться к заказу"</b>
payment-msg-in-account =
    {"\u000A"}<b>✅ После подтверждения оплаты нажмите на кнопку "Вернуться к аккаунту"</b>
back-to-order-btn = ↪️ Вернуться к заказу
back-to-account-btn = ↪️ Вернуться к аккаунту
enter-different-sum-btn = ⬅️ Ввести другую сумму
pay-btn = 💳 Оплатить
payment-successful = ✅ На ваш баланс зачислено { $payment_summ } $
payment-waiting = ⌛ Ожидаю зачисления
payment-fail =
    ❗️ Не удалось подтвердить вашу оплату
    Сумма оплаты: { $payment_summ }$
    Номер оплаты: <code>{ $payment_id }</code>
contact-support-btn = 👨‍💻 Связаться с тех. поддержкой


### Order messages ###
order-created-msg =
   Спасибо за заказ!
   Для того, чтобы скачать файлы, перейдите в заказ
   Если у Вас возникли технические вопросы или проблемы, вы можете обратиться в тех.поддержку @popoze
drawing-order-created-msg =
    Спасибо за заказ! Мы вскоре свяжемся с вами.
orders-history-msg = Ваши заказы:
order-was-updated = ✅ Заказ был обновлен
order-overview = <b>Ваш заказ</b> {"\u000A"}
order-id = ID: { $order_id }
order-summ = Сумма заказа: { $order_summ }$
discount-summ = Сумма скидки: { $discount_summ }$.
waiting_payment = Ждет оплаты
payed = Оплачен
order-status = Статус: { $status }
order-was-created = Создан: { $was_created }
order-payed-msg = ✅ Заказ оплачен!
export-to-xlsx = 📥 Экспорт товаров в excel
excel-info-msg =
    ❗По всем техническим вопросам необходимо обращаться @popoze.
no-products-in-order = В заказе отсутствуют товары


### Promocode messages ###
enter-promocode = Введите промокод
wrong-promocode = Промокод недействителен. Проверьте правильность набора
promocode-already-used = Промокод уже был использован вами
promocode-usage-limit-reached = Промокод был использован максимальное количество раз
activate-promocode-in-payment = Активируйте этот промокод при оплате в разделе "Пополнить баланс"
activate-promocode-in-order = Активируйте этот промокод при оформлении заказа
balance-promocode-activated = ✅ Промокод активирован! На ваш счет добавлено { $amount } $
bonus-promocode-activated =
    ✅ Промокод активирован!
    Вы получите бонус в размере { $amount }% к следующему пополнению
discount-promocode-activated =
    ✅ Промокод активирован!
    Вы получите скидку на следующий заказ в размере {$amount}%

### Notifications ###
new-order-notification =
    🛒 Новый заказ
    ID заказа: { $order_id }
    Сумма заказа: <b>{ $summ } $</b>
    Скидка: { $discount_summ } $
new-order-for-drawing =
    🎨 Новый заказ на отрисовку
    Товар: { $product_name }
    Заказчик: <code>@{ $user_name }</code>
    TG ID заказчика: <code>{ $user_tg_id }</code>
