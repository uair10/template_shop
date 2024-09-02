document.addEventListener("DOMContentLoaded", function () {
    let context = $("#stat_chart").get(0).getContext('2d');

    let bot_started = JSON.parse(context.canvas.dataset.bot_started);
    let registered_users = JSON.parse(context.canvas.dataset.registered_users);
    let personal_order_clicks = JSON.parse(context.canvas.dataset.personal_order_clicks);
    let orders_created = JSON.parse(context.canvas.dataset.orders_created);
    let co_buy_order_clicks = JSON.parse(context.canvas.dataset.co_buy_order_clicks);
    let co_buys_created = JSON.parse(context.canvas.dataset.co_buys_created);
    let new_co_buy_users = JSON.parse(context.canvas.dataset.new_co_buy_users);
    let add_payment_clicks = JSON.parse(context.canvas.dataset.add_payment_clicks);
    let payments_paid = JSON.parse(context.canvas.dataset.payments_paid);
    let messages_sent = JSON.parse(context.canvas.dataset.messages_sent);
    let chart

    chart = new Chart(context, {
        type: 'bar',
        data: {
            datasets: [{
                label: "Бот запущен раз",
                data: [{
                    y: bot_started,
                },],
                fill: true,
                lineTension: 0.2,
                backgroundColor: "rgba(54, 162, 235, 0.5)",
                borderColor: "rgb(54, 162, 235)",
                borderWidth: 1.2
            },
                {
                    label: "Зарегистрировано пользователей",
                    data: [{
                        y: registered_users,
                    },],
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(70, 64, 255, 0.5)",
                    borderColor: "rgb(70,64,255)",
                    borderWidth: 1.2
                },
                {
                    label: "Кликов на 'Сертификат индивидуально'",
                    data: [{
                        y: personal_order_clicks,
                    },],
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(160, 64, 255, 0.5)",
                    borderColor: "rgb(160, 64, 255)",
                    borderWidth: 1.2
                },
                {
                    label: "Кликов на 'Сертификат в складчину'",
                    data: [{
                        y: co_buy_order_clicks,
                    },],
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(35,184,64, 0.5)",
                    borderColor: "rgb(35,184,64)",
                    borderWidth: 1.2
                },
                {
                    label: "Создано заказов",
                    data: [{
                        y: orders_created,
                    },],
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(48, 198, 124, 0.5)",
                    borderColor: "rgb(48, 198, 124)",
                    borderWidth: 1.2
                },
                {
                    label: "Создано складчин",
                    data: [{
                        y: co_buys_created,
                    },],
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(2, 177, 245, 0.5)",
                    borderColor: "rgb(2,177,245)",
                    borderWidth: 1.2
                },
                {
                    label: "Новых пользователей складчины",
                    data: [{
                        y: new_co_buy_users,
                    },],
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(255,184,0, 0.5)",
                    borderColor: "rgb(255,184,0)",
                    borderWidth: 1.2
                },
                {
                    label: "Переходов на оплату",
                    data: [{
                        y: add_payment_clicks,
                    },],
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(215,0,165, 0.5)",
                    borderColor: "rgb(215,0,165)",
                    borderWidth: 1.2
                },
                {
                    label: "Оплачено счетов",
                    data: [{
                        y: payments_paid,
                    },],
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(255, 51, 51, 0.5)",
                    borderColor: "rgb(255, 51, 51)",
                    borderWidth: 1.2
                },
                {
                    label: "Сообщений в рассылке",
                    data: [{
                        y: messages_sent,
                    },],
                    fill: true,
                    lineTension: 0.2,
                    backgroundColor: "rgba(26, 140, 206, 0.5)",
                    borderColor: "rgb(26, 140, 206)",
                    borderWidth: 1.2
                },
            ]
        },
        options: {
            responsive: true,
        },
    })
});
