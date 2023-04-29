Проект чат-бота для социальной сети [vk.com](http://www.vk.com). Бот создан для информирования и продажи авиабилетов вымешенной авиакомпании.

В [папке]( https://github.com/kirillsdnv/vk_chat_bot/tree/master/external_data/dialog ) можно увидеть диалог с ботом охватывающий все шаги сценария и доступные команды.

В общем виде логика работы чат-бота такова:
при запуске бота (файл [vk_bot.py](https://github.com/kirillsdnv/vk_chat_bot/blob/master/vk_bot.py)) `VkBotLongPoll` начинает "слушать" сервер
и при появлении события (`event`) вызывается метод `event_handler`; 
в зависимости от того, содержится ли команда в тексте сообщения, находится ли пользователь на одном из шагов сценария, вызывается соответствующий метод.

Бот имеет 5 команд:
  * `'/help'` отправляет пользователю текст и предлагает воспользоваться командами `'/cities'` и `'/routes'`, чтобы узнать об актуальных маршрутах
  * `'/cities'` выводит список обслуживаемых городов
  * `'/routes'` дополняет список направлений из каждого города

  * `'/ticket'` - запускает сценарий покупки билета (Ordering)
  * `'/restart'` - перезапускает бота

Все команды обрабатываются методом `commands_handler`.
В некоторых случаях для формирования ответа пользователю используются вспомогательные функции из модуля [utils.py](https://github.com/kirillsdnv/vk_chat_bot/blob/master/utils.py).

Сценарий Ordering так же запускается при наличии в сообщении ключевого слова-намерения `intent` в тексте сообщения.
За это отвечает метод `intent_searching`.

На каждом шаге сценария сообщение от пользователя обрабатывается соответствующим обработчиком (`handler`). Все функции-обработчики находятся в соответствующем файле
[handlers.py](https://github.com/kirillsdnv/vk_chat_bot/blob/master/handlers.py). В случае если данные пользователя корректны,
то информация от пользователя заносится в переменную `context`, где хранятся все данные о заказе: город вылета, город прибытия, время отправления и т.д.
В таком случае функция-обработчик возвращает `True`, текст ответа или клавиатуру. Иначе возвращается `False` и соответствующее сообщение об ошибке.
За обработку результата handler'ов отвечает метод `continue_scenario`.

На последнем шаге сценария Ordering генерируется посадочный талон для пользователя со всеми данными о его полёте.
За это отвечает модуль [generate_ticket.py](https://github.com/kirillsdnv/vk_chat_bot/blob/master/generate_ticket.py) и его одноимённая функция.
![14](https://user-images.githubusercontent.com/80598880/171870798-a9d28117-62f5-47f0-859e-d75aae9ea893.jpg)

Пример ответа пользователю со сгенерированным билетом.

Остальные модули:
  - [settings_by_default.txt](https://github.com/kirillsdnv/vk_chat_bot/blob/master/settings_by_default.txt) файл содержащий основные данные для работы бота:
      - токен
      - данные для соединения с СУБД
      - списки городов и команд
      - форматы даты и времени, используемые ботом
      - intents (слова-"намерения")
      - ответ по умолчанию - отправляется в случаях, когда пользователь отправил боту то, что он не может распознать
      - сценарии
  - [generate_flights.py](https://github.com/kirillsdnv/vk_chat_bot/blob/master/generate_flights.py) модуль генерирует расписание и маршруты
  - [utils.py](https://github.com/kirillsdnv/vk_chat_bot/blob/master/utils.py) содержит в себе утилиты различного функционала:
    - формируют ответы для пользователя
    - конфигурируют логирование
  - [models.py](https://github.com/kirillsdnv/vk_chat_bot/blob/master/models.py) отвечает за генерацию баз данных
  - [tests.py](https://github.com/kirillsdnv/vk_chat_bot/blob/master/tests.py) модуль с тестами бота
  - [dataset.py](https://github.com/kirillsdnv/vk_chat_bot/blob/master/dataset.py) содержит данные, используемые в тестах:
    генерирует имитацию сообщений от пользователя и ожидаемые ответы бота.
  - [keyboards.py](https://github.com/kirillsdnv/vk_chat_bot/blob/master/keyboards.py) формирует клавиатуру для выбора вариантов ответа бота

 
