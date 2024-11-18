### Base messages ###
confirm-btn = ✅ Confirm
back-btn = ⬅️ Back
main-menu-btn = ↪️ Main menu


### Errors ###
wrong-file-extension = ❌ Supported file extensions: .xlsx

### DB errors ###
error-msg = ❗️ Something went wrong
not-enough-balance =❗ Insufficient balance. Your balance: { $balance } $
error-during-order-create =
    ❗ Error when creating an order
    Try again or contact technical support
error-during-order-update =
    ❗ Error when updating an order
    Try again or contact technical support
unknown-server-error = ❗️ An server error occurred
user-not-exists-msg = The user doesn't exist
user-already-exists-msg = Such a user already exists
order-already-exists-msg = Such an order already exists
order-not-exists-msg = The order doesn't exist


### Menu messages ###
welcome =
    Hello, { $user }!
    Select option to start.
buy-btn = 🛒 PSD templates
profile-btn = 👤 Profile
change-lang-btn = 🌎 Изменить язык
select-lang-msg = Select language
admin-btn = ⚙️ Admin panel


### Create Order ###
select-country-msg = Select country
select-template-type-msg = Select template type
documents-btn = 🪪 Documents
cards-btn = 💳 Cards
select-category-msg = Select category
select-products-msg = Select products
select-payment-method-msg = Select a payment method
cart-total = Cart total: { $cart_total }$
clear-cart-btn = 🗑️ Clear cart
go-to-order-btn = Go to order

### Product info ###
product-title = Name: { $product_title }
product-price = Price: { $product_price }$
order-doc-drawing-btn = 🎨 Order document drawing
add-to-cart-btn = 🛒 Buy template


### Account messages ###
your-account = <b>Your account {"\u000A"}</b>
your-balance = Balance: { $balance } $
your-orders-count = Order count: { $orders_count }
registered_date = Was registered: { $reg_date }
add-balance-btn = 💵 Top-up balance
enter-promocode-btn = 📟 Enter promocode
orders-btn = 🗂 My orders
payments-btn = 📄 Payment history


### Payments messages ###
payment-history = Your payments:
payment-details = Payment details {"\u000A"}
payment_id = Payment ID: { $payment_id }
payment_summ = Payment amount: { $payment_summ }
payment_status = Status: { $status }
created_at = Was created: { $created_at }
waiting_payment = Waiting payment
paid = Paid
payment_failed = Payment failed
select-payment-method-msg = Select a payment method
select-payment-amount-rub-msg =
    Enter the top-up amount in <b>dollars</b>, no more than 2 digits after the separator. Example: 99.99 or 99
    {"\u000A"}Payment is made in rubles at the exchange rate of the Central Bank of Russia
    {"\u000A"}<b>Current ratee:</b> { $usd_rate } rub. for $. The rate is fixed at the time of payment
select-payment-amount-usd-msg =
    Enter the top-up amount in <b>dollars</b>, no more than 2 digits after the separator. Example: 99.99 or 99
qiwi-btn = Card (QIWI)
crypto-btn = USDT
payment-msg =
    Pay the invoice by clicking on the "Pay" button{"\u000A"}
    ℹ️ If you have a promocode for a recharge bonus, enter it before you pay.{"\u000A"}
    ❓ If payment has not been confirmed within 20 minutes, please contact support{"\u000A"}
    <a href="https://telegra.ph/Instrukciya-po-oplate-USDT-10-25">Payment instructions</a>

payment-msg-in-order =
    {"\u000A"}<b>✅ Once payment is confirmed, click on the "Back to order"</b> button.
payment-msg-in-account =
    {"\u000A"}<b>✅ After confirming payment, click on the "Back to account"</b> button.
back-to-order-btn = ↪️ Back to order
back-to-account-btn = ↪️ Back to account
enter-different-sum-btn = ⬅️ Enter a different amount
pay-btn = 💳 Pay
payment-successful = ✅ You have { $payment_summ } $ credited to your balance
payment-waiting = ⌛ Pending enrollment
payment-fail =
    ❗️ Failed to confirm your payment
    Payment amount: { $payment_summ }$
    Payment ID: <code>{ $payment_id }</code>
contact-support-btn = 👨‍💻 Contact support


### Order messages ###
order-created-msg =
   Thank you for ordering!
   In order to download the files, go to order
   If you have any technical questions or problems, you can contact tech support @popoze
drawing-order-created-msg =
    Thank you for order! We will contact you soon.
orders-history-msg = Your orders:
order-was-updated = ✅ Order was updated
order-overview = <b>Your order</b> {"\u000A"}
order-id = ID: { $order_id }
order-summ = Order amount: { $order_summ }$
discount-summ = Discount amount: { $discount_summ }$.
waiting_payment = Waiting payment
paid = Paid
order-status = Status: { $status }
order-was-created = Was created: { $was_created }
order-paid-msg = ✅ Order paid!
export-to-xlsx = 📥 Export products to excel
excel-info-msg =
    ❗For all technical questions please contact @popoze.
no-products-in-order = There are no items in the order


### Promocode messages ###
enter-promocode = Enter promocode
wrong-promocode = The promocode is invalid. Check if you typed it correctly
promocode-already-used = The promocode has already been used by you
promocode-usage-limit-reached = The promocode has been used the maximum number of times
activate-promocode-in-payment = Activate this promocode at checkout in the "Topup balance" section
activate-promocode-in-order = Activate this promocode at checkout
balance-promocode-activated = ✅ Promocode activated! { $amount } $ has been added to your account.
bonus-promocode-activated =
    ✅ Promocode activated!
    You will receive a bonus of { $amount }% on your next deposit
discount-promocode-activated =
    ✅ Promocode activated!
    You will receive a discount on your next order in the amount of {$amount}%

### Notifications ###
new-order-notification =
    🛒 Новый заказ
    ID заказа: { $order_id }
    Сумма заказа: <b>{ $summ } $</b>
    Скидка: { $discount_summ } $
new-order-for-drawing =
    🎨 Новый заказ на отрисовку
    Товар: { $product_name }
    Заказчик: @{ $user_name }
    TG ID заказчика: <code>{ $user_tg_id }</code>