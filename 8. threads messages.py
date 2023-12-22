import threading
import time


NUMBER_OF_MESSAGES = 20


def print_messages(messages):
    for mes in messages:
        print(mes)
        time.sleep(0.01)


# Создаем два потока
thread1 = threading.Thread(target=print_messages, args=(["||||||" for _ in range(NUMBER_OF_MESSAGES)],))
thread2 = threading.Thread(target=print_messages, args=(["------" for _ in range(NUMBER_OF_MESSAGES)],))

# Запускаем потоки
thread1.start()
thread2.start()
