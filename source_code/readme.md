::::Для себя::::
https://www.youtube.com/watch?v=QU1pPzEGrqw
https://pytmx.readthedocs.io/en/latest/
https://github.com/katmfoo/pygame-tiled-demo
https://pygame.readthedocs.io/en/latest/tiles/tiles.html
https://github.com/MyreMylar/pygame_gui_examples
https://github.com/Grimmys/rpg_tactical_fantasy_game

ДОРОЖНАЯ КАРТА

Сделано:
- Есть карта
- Есть анимированный персонаж
- Есть коллизии
- Аудио-оформление
- Рабочая система сохранений/загрузки (по итогу, когда все задачи по выбранным темам решены, возможность переместиться обратно в платформер и выбрать другие предметы -- основа заложена)
- Полноценный главный экран с параллаксом и возможностью сбросить/загрузить сохранение
- Экран паузы
- привести часть-платформер в нормальный вид (всё функционально, доделать оформление)

В процессе:
- Рисовка грифонов-npc
- добавить грифонов-npc (некоторые статичные, некоторые ходячие - добавить возможность диалога, а оттуда - решение задач)
- диалоги и задачи = сделать gui
- Составление примеров/задач (некоторые уже написаны)
- Доделка карты (добавить анимацию, навигацию (в каких-то местах будут стоять пробирки=химия, в других книги=литература и т.д.), сделать так, чтобы игрока не было видно, если он за каким-то препятствием)

В планах (по приоритету):


# Что нужно сделать:
### Самое насущное
- Перенести раннер-код из main.py в отдельные файлы, где возможно.
- Анимированный мир. Заодно добавить указатели-навигацию. Подсказки. 
- Пофиксить выбор предметов - переставить блоки, добавить подсказки и убрать уродства с карты.
- Добавить NPC в нормальном виде, убрать существующий плачевный код. 
- Вводный грифон, объяснящий управление и задачу игрока.
- Диалоги с NPC - переделать, придумать, добавить.
- Как вариант - при решении задачи выдаётся предмет, который понадоюится потом. Система инвентаря. (Опять же - если будет время)
- Связать интеракции NPC с сюжетом. 22 грифона по миру - 11 предметов, таким образом можно связать одного грифона двумя предметами, чтобы ни у одного грифона не было одновременно двух задач.
- Добавить сами задачи (графику мне помогают делать).
### Далее идёт багфиксинг и качество жизни.
- Пофиксить неровное отображение интерфейса в некоторых местах.
- Добавить настройки.