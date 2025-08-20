// Берём данные от Telegram
const tg = window.Telegram.WebApp;
const user = tg.initDataUnsafe.user;

// Функция загрузки данных
function loadProfile() {
    const profileDiv = document.getElementById("profile");

    if (user) {
        profileDiv.innerHTML =
            '<img src="' + (user.photo_url || "https://t.me/i/userpic/320/" + user.id + ".jpg") + '" alt="Аватар">' +
            '<div>' +
            '<h2>' + user.first_name + ' (ID: ' + user.id + ')</h2>' +
            '<p>@' + (user.username || "Не указано") + '</p>' +
            '</div>';
    } else {
        profileDiv.innerText = "Данные пользователя не найдены.";
    }
}

// Эмуляция загрузки (можно убрать setTimeout и сразу показывать)
window.onload = function() {
    setTimeout(() => {
        document.getElementById("loader").classList.add("hidden");
        document.getElementById("app").classList.remove("hidden");
        loadProfile();
        tg.expand();
    }, 5000); // 5 сек задержка для красоты
};