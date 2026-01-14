import threading


event = threading.Event()


def wait_for_event():
    print("Ожидание события")
    event.wait()  # Ждем, пока событие не будет установлено
    print("Событие установлено")


thread = threading.Thread(target=wait_for_event)
thread.start()

input("Нажмите Enter для установки события\n")
event.set()  # Устанавливаем событие, чтобы поток мог продолжить работу
thread.join()
