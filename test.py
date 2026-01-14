import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Параметры, которые можно менять (относительные пути)
INPUT_FILE = "files/20 ноября.xlsx"  # путь к Excel относительно папки скрипта
CLASS_NAME = "11А"                    # нужный класс
OUTPUT_IMAGE = "files/11A.png"        # куда сохранить изображение

# Получаем абсолютный путь от текущей директории скрипта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(BASE_DIR, INPUT_FILE)
output_path = os.path.join(BASE_DIR, OUTPUT_IMAGE)

# Создадим директорию, если её нет
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 1. Читаем файл
df = pd.read_excel(input_path, header=None)

# 2. Ищем ячейку с названием класса
pos = np.where(df.astype(str).eq(CLASS_NAME))
if len(pos[0]) == 0:
    raise ValueError(f"Класс {CLASS_NAME} не найден")

row_class, col_class = pos[0][0], pos[1][0]

# 3. Заголовки предположительно на строку ниже
row_header = row_class + 1

# 4. Поиск столбцов 'Предмет' и 'Каб.'
subj_col = None
cab_col = None

for c in range(df.shape[1]):
    cell = str(df.iloc[row_header, c]).strip().lower()
    if cell == "предмет":
        subj_col = c
    if cell == "каб.":
        cab_col = c

if subj_col is None or cab_col is None:
    raise ValueError("Не найдены столбцы Предмет/Каб.")

# 5. Поиск конца блока — следующей строки c текстом 'Время урока'
end_row = None
for r in range(row_class + 1, len(df)):
    if str(df.iloc[r, 0]).startswith("Время урока"):
        end_row = r
        break

if end_row is None:
    end_row = len(df)

# 6. Извлекаем блок расписания
schedule = df.iloc[row_header + 1 : end_row, :]

# 7. Достаём нужные столбцы
result = schedule[[0, subj_col, cab_col]].copy()
result.columns = ["Время", "Предмет", "Кабинет"]
result = result[result["Предмет"].notna()]

print(result)

# 8. Создание изображения
fig, ax = plt.subplots(figsize=(8, len(result) * 0.6))
ax.axis("off")

table_data = [result.columns.tolist()] + result.values.tolist()

table = ax.table(
    cellText=table_data,
    loc='center',
    cellLoc='center'
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.3)

plt.tight_layout()
plt.savefig(output_path, dpi=200)
plt.close()

print(f"Готово! Файл сохранён в: {output_path}")
