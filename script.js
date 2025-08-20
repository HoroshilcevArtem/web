const tg = window.Telegram.WebApp;
let user = tg.initDataUnsafe ? tg.initDataUnsafe.user : null;

// Если открыто в браузере – читаем данные из URL
if (!user) {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");
    const username = params.get("username");
    const name = params.get("name");
    const avatar = params.get("avatar");

    if (id) {
        user = {
            id: id,
            username: username,
            first_name: name,
            photo_url: avatar
        };
    }
}

function loadProfile() {
    const profileDiv = document.getElementById("profile");

    if (user) {
        profileDiv.innerHTML =
            '<img src="' + (user.photo_url || "https://t.me/i/userpic/320/" + user.id + ".jpg") + '" alt="Аватар">' +
            '<div>' +
            '<h2>' + (user.first_name || "Неизвестно") + ' (ID: ' + user.id + ')</h2>' +
            '<p>@' + (user.username || "Не указано") + '</p>' +
            '</div>';
    } else {
        profileDiv.innerText = "❌ Данные пользователя не найдены.";
    }
}

// Запуск приложения
window.onload = function() {
    setTimeout(() => {
        document.getElementById("loader").classList.add("hidden");
        document.getElementById("app").classList.remove("hidden");
        loadProfile();
        if (tg) tg.expand();
    }, 1000); // 1 сек задержка
};