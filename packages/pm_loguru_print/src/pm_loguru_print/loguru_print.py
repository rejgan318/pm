"""
Ислользование Loguru для отладочной печати. Для меня это самый простой и удобный способ добавить цвет в вывод

1. Настраивается формат вывода, очень короткий и лаконичный
2. Определяются короткие лямбда-функции для лаконичной отладочной печати. Это и есть главная цель этого модуля

Для активации логирования нужно вызвать функцию `start_loguru()`

[Цвета в loguru](https://loguru.readthedocs.io/en/stable/api/logger.html#color)

Цвета:
<black> <k>
<blue> <e>
<cyan> <c>
<green> <g>
<magenta> <m>
<red> <r>
<white> <w>
<yellow> <y>

Для светлых цветов добавляется префикс `light-` или `l` для сокращённой формы <light-blue> <le>
Для фона цвета в верхнем регистре <GREEN>, <G>, `LIGHT-` или `L`

Стили:
<bold> <b>; <italic> <i>; <underline> <u>; <strike> <s>; <reverse> <v>
<level> - стиль уровня логирования
"""

from loguru import logger
import sys
import time


__all__ = ["start_loguru", "logger", "reset_time_loguru", "logd", "logi", "logs", "logw", "loge", "logc"]

# создаём глобальную переменную для хранения времени старта
__START_TIME = 0

# шаблон без абсолютного времени. Вместо него отображается таймер от старта {extra[elapsed]} из функции-форматтера.
# icon;short timer;message
LOGURU_FORMAT = (
    '{level.icon}'
    '<d><w>[{extra[elapsed]}]</></> '
    # '<green>[{extra[elapsed]}]</green> '
    '{message}'     # цвет по умолчанию
    # '<level>{message}</level>'  # вариант с цветами уровня вывода
    '\n'  # Важно: при использовании функции-форматтера в конце нужен \n
)

# То, ради чего всё затевалось, короткие лямбда-функции для отладочной печати
logd = lambda x: logger.opt(colors=True).debug(x)
logi = lambda x: logger.opt(colors=True).info(x)
logs = lambda x: logger.opt(colors=True).success(x)
logw = lambda x: logger.opt(colors=True).warning(x)
loge = lambda x: logger.opt(colors=True).error(x)
logc = lambda x: logger.opt(colors=True).critical(x)

# возможно несколько аргументов как в print. Но проще использовать один аргумент и f-строки
# logw = lambda *args: logger.opt(colors=True).warning(" ".join(map(str, args)))


def start_loguru(level: str = "INFO", loguru_format: str = LOGURU_FORMAT):
    """
    This must be done to activate logging.

    Configures and activates logging with specified parameters using Loguru.
    This sets up the logging framework by removing any default handlers and adding a new
    handler to log messages to the standard output. The logging behavior is defined by the
    specified log level and format.

    :param level: Minimum log severity level used to filter the logs. It accepts values
        like "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL".
    :param loguru_format: Format string that defines the structure of log messages,
        including fields like time, level, and message content.
    :return: None
    """
    logger.remove()

    # Фиксируем время старта модуля, а не время импорта
    global __START_TIME
    __START_TIME = time.time()

    # we received a string, turn it into a dynamic formatter function
    def dynamic_formatter(record):
        # loguru_format, переданный как параметр может не использовать record["extra"]["elapsed"],
        # а выводить традиционно time. В этом случае форматтер нормально сработает, но ни на что не влияет

        # Calculate elapsed time
        elapsed = time.time() - __START_TIME
        # Write to extra for display in the format template
        record["extra"]["elapsed"] = f"{elapsed:.1f}s"
        return loguru_format

    chosen_formatter = dynamic_formatter
    logger.add(sys.stdout, level=level, format=chosen_formatter, colorize=True)


def reset_time_loguru():
    global __START_TIME
    __START_TIME = time.time()
    
    
if __name__ == '__main__':
    print("loguru_print demo with custom formatter\n")
    # logger.info("loguru_print demo with custom formatter")

    start_loguru()
    logi("<b>Levels demo, standard Loguru possibility</>")
    start_loguru("ERROR")
    logi("INFO level is disabled. This message is not logged")
    loge("ERROR level is setting")

    start_loguru(level="DEBUG")
    logd("Restart with DEBUG level\n")

    logi("<b>Turn logging off/on, timer interval demo</>")

    # Logging can be enabled and disabled using standard loguru methods
    logger.disable("")
    logd("This message is not logged")
    logger.enable("")
    time.sleep(2.)  # pause for a timer demo
    logs("a few seconds later... This message is logged again\n")

    logi("<b>Colors and styles demo</>")
    logd("<b>Instead</> <s>print</> <u>logging</>"
         " with <lr><i>color</i></> or <LG>with</> <G><m>color</></> <level>level</> <v>is used</v> "
         "\n"
         "<k>k</><e>e</><c>c</><g>g</><m>m</><r>r</><w>w</><y>y</>"
         "\n"
         "<lk>k</><le>e</><lc>c</><lg>g</><lm>m</><lr>r</><lw>w</><ly>y</>"
         "\n"
         # тёмные света как результат применения стиля dim могут не поддерживаться встроенным терминалом Pycharm 
         # и отображаться как обычные. Можно включить опцию Emulate terminal in output console, тёмные цвета будут
         # отображаться, но некоторые широкие unicode иконки могут урезаться по ширине
         # В Windows терминале отображаются корректно
         "<d><k>k</><e>e</><c>c</><g>g</><m>m</><r>r</><w>w</><y>y</></d>"  
         "\n"
         "<K> </><E> </><C> </><G> </><M> </><R> </><W> </><Y> </>"
         "\n"
         "<LK> </><LE> </><LC> </><LG> </><LM> </><LR> </><LW> </><LY> </>"
         "\n"
         )

    logi("<b>Examples of color pairs «Context», «Accent»</>")
    logs("c,    y: <c>CalendarEvent</> started. result=<y>134.334</>")
    logs("m,   lc: <m>CalendarEvent</> started. result=<lc>134.334</>")
    logs("e,    g: <e>CalendarEvent</> started. result=<g>134.334</>")
    logs("e,   le: <e>CalendarEvent</> started. result=<le>134.334</>")
    logs("e, le+u: <e>CalendarEvent</> started. result=<le><u>134.334</></>")
    logs("e, le+b: <e>CalendarEvent</> started. result=<le><b>134.334</></>")
    logs("e, le+i: <e>CalendarEvent</> started. result=<le><i>134.334</></>")
    logs("e,  e+v: <e>CalendarEvent</> started. result=<e><v>134.334</></>")
    logs("b,    v: <b>CalendarEvent</> started. result=<v>134.334</>")

    time.sleep(0.5)

    new_loguru_format = '{level.icon}<light-green>[{time:hh:mm:ss.SS}]</> <level>{message}</level>\n'
    start_loguru(level="DEBUG", loguru_format=new_loguru_format)

    print()
    logi("<b>Custom format demo</>")
    logd('DEBUG: New')
    logi('INFO: format — absolute time')
    logs('SUCCESS: in light color and')
    logw('WARNING: text color')
    loge('ERROR: as level always')
    logc('CRITICAL: by default')

    print()
    logi("<b>Custom icon demo</>")
    logger.level("DEBUG", icon="🪲")
    logd("New nice DEBUG icon")
    logger.level("SUCCESS", icon="🎯")
    logs("New nice SUCCESS icon")
    logger.level("WARNING", icon="📢")
    logw("New nice WARNING icon")
