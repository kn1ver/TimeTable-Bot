"use strict";

const fs = require("fs");
const { sessionValid } = require("netschoolapi/dist/utils/checks");

/**
 * Получение списка объявлений
 */
async function getAnnouncements() {
    // this = экземпляр NetschoolAPI
    const { client } = await sessionValid.call(this);

    const response = await client.get("announcements").then(r => r.json());

    return response.map(item => ({
        id: item.id,
        name: item.name,
        author: item.author,
        attachments: item.attachments || []
    }));
}

/**
 * Загрузка файла вложения
 */
async function downloadFile() {
    // this = экземпляр NetschoolAPI
    const { client } = await sessionValid.call(this);
    const attachments = [];

    const response = await client.get("announcements").then(r => r.json());

    const anns = response.map(item => ({
        id: item.id,
        name: item.name,
        author: item.author,
        attachments: item.attachments || []
    }));

    for (const ann of anns) {
            if (ann.attachments?.length > 0) {
                attachments.push(ann.attachments[0]); // берём первый
            }
        }

    try {
        // Используем тот же клиент, что авторизован
        const url = `/attachments/${attachments[0].id}`;
        const res = await client.get(url, { raw: true }); // raw=true для получения Buffer
        return [Buffer.from(await res.arrayBuffer()), attachments[0].name];
    } catch (err) {
        console.error(`Не удалось скачать файл ${attachments[0].name}`, err.message);
    }

}

module.exports = {
    getAnnouncements,
    downloadFile
};
