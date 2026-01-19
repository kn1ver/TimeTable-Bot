const NS = require("netschoolapi").default;
const { getAnnouncements } = require("./methods/announcements.js");
const fs = require("fs");
require("dotenv").config({ path: "../.env" });

const user = new NS({
    origin: "https://asurso.ru/",
    login: "Курганов5",
    password: "5курганов",
    school: 2065,
});
exports.user = user;

// Скачивание одного файла через внутренний клиент библиотеки
async function downloadAttachment(attachment) {
    try {
        // Используем тот же клиент, что авторизован
        const url = `/attachments/${attachment.id}`;
        const res = await user.client.get(url, { raw: true }); // raw=true для получения Buffer
        const buffer = Buffer.from(await res.arrayBuffer());
        fs.writeFileSync(attachment.name, buffer);
        console.log(`Файл сохранён: ${attachment.name}`);
    } catch (err) {
        console.error(`Не удалось скачать файл ${attachment.name}`, err.message);
    }
}

// Скачивание всех вложений из всех объявлений
async function downloadAttachments(announcements) {
    for (const ann of announcements) {
        if (ann.attachments?.length) {
            for (const file of ann.attachments) {
                await downloadAttachment(file);
            }
        }
    }
}

// Основной блок
(async () => {
    try {
        const announcements = await getAnnouncements.call(user);
        console.log("Объявления:", announcements);

        // Скачиваем все файлы
        await downloadAttachments(announcements);

    } catch (err) {
        console.error("Ошибка:", err.message);
    }
})();
