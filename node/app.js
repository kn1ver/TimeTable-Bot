const express = require("express");
const NS = require("netschoolapi").default;
const { getAnnouncements, downloadFile } = require("./methods/announcements.js");
require("dotenv").config({ path: "../.env" });

const PORT = process.env.PORT || 3000;
const API_TOKEN = "odrigjdorijgdokjdnvkdfjwooweigjnoedredi"

const user = new NS({
        origin: "https://asurso.ru/",
        login: "Курганов5",
        password: "5курганов",
        school: 2065,
    });

const app = express();
app.use(express.json());

/** Простая авторизация по API-токену */
app.use((req, res, next) => {
    if (API_TOKEN) {
        const token = req.header("X-API-Token") || req.query.token;
        if (!token || token !== API_TOKEN) {
            return res.status(401).json({ error: "Unauthorized" });
        }
    }
    next();
});

/** Получение списка объявлений */
app.get("/announcements", async (req, res) => {
    try {
        await user.logIn();

        const announcements = await getAnnouncements.call(user);
        const annsIds = {};

        for (const ann of announcements) {
            if (ann.attachments?.length > 0) {
                annsIds[ann.id] = ann.attachments[0]; // берём первый
            }
        }

        await user.logOut();
        res.json(annsIds);

    } catch (err) {
        console.error("GET /announcements error:", err);
        res.status(500).json({ error: err.message });
    }
});

/** Скачать конкретное вложение */
app.post("/attachment", async (req, res) => {
    try {
        await user.logIn();

        const file_data = await downloadFile.call(user);
        const base64 = file_data[0].toString("base64");

        res.json({ 
            success: true,
            data: base64,
            name: file_data[1]
        });

    } catch (err) {
        console.error("GET /announcements error:", err);
        res.status(500).json({ error: err.message });
    }
});

/** Запуск сервера */
app.listen(PORT, () => {
    console.log(`TimetableBot-API running on http://localhost:${PORT}`);
});
