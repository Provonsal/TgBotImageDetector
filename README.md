Это моя дипломная работа. Она представляет из себя телеграмм бота, который управляет нейросетью по определению объектов на фото.

Конкретнее, находит границы изображений на присланных фото и видео и гифках:

![file_308](https://github.com/Provonsal/Diplom/assets/117067474/bce81e65-2f02-414a-88b7-745c05c78283)

Для работы нейросети требуется производительная видеокарта, мой вариант это 3060 ти.

При запуске бота из файла bot.py, предварительно создав бота и токен в bot father, плодами работы нейросети сможет воспользоваться любой желающий если обратиться к боту.

Бот является в каком то роде интерфейсом к нейросети, я посчитал нужным использовать бота, поскольку это бесплатно, быстро, просто, безопаснее чем например делать белый ip, платить и быть подверженным кибер атакам извне.

У проекта есть проблемы, он не закончен в этом плане, но на то она и дипломная работа, задумка не моя и где можно это реализовать я не особо представляю. Например использовать саму обученную нейросеть для более сложной нейросети, состоящей из нескольких.

Проблема в том что если пользователь попробует начать сразу несколько обработок файлов, то он может быстро заполнить ОЗУ компьютера и память видеокарты, что приведет к зависанию компьютера и очень долгому отклику бота пользователю.

Решается это путем добавления ограничения на количество обрабатываемых файлов за раз, создание очереди, реализовать можно с помощью БД. Она там присутствует и используется. Файл Sql.py, БД sqlite