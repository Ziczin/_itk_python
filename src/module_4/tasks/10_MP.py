import csv
import multiprocessing
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool, Process, Queue, cpu_count


def generate_data(n):
    return [random.randint(2, 1000) for _ in range(n)]


# Делаем разложение на простые числа
def prime_factors_list(n):  # вайбкод
    if n <= 1:
        return []

    factors = []
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1
    if n > 1:
        factors.append(n)
    return factors


# Делаем разложение, но 1000 раз чтобы имитировать высокую нагрузку
def process_number(n):
    res = []
    for i in range(1000):
        res = prime_factors_list(n)
    return res


# Для каждого числа вызываем "высокую нагрузку" на одном ядре и потоке
def sequential_processing(data):
    results = []
    for num in data:
        factors = process_number(num)
        results.append((num, factors))
    return results


# Для каждого числа поднимаем поток, в него передаём "высокую нагрузку"
# Из-за GIL ожидаем что время будет больше, чем для линейного цикла, из-за
# расходов на поднятие потока. Количество ограничено по количеству ядер
def process_with_threadpool(data):
    results = []
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        # Тут генерим словарь с потоками, если я правильно понял,
        # то они тут сразу запускаются из пула
        future_to_num = {executor.submit(process_number, num): num for num in data}
        for future in as_completed(future_to_num):  # Ждём поток и возвращаем его
            num = future_to_num[future]  # Забрали число

            try:
                factors = future.result()  # Достали делители
                results.append((num, factors))

            except Exception as e:
                print(e)
                results.append((num, []))

    results.sort(key=lambda x: data.index(x[0]))
    return results


# Пул процессов, ожидаем что работать будет быстрее на больших датасетаз
# Поднять процесс тяжелее чем поток, на маленьких датасетах займёт больше
# времени, чем если бы обрабатывали в одном процессе
def process_with_processpool(data):
    results = []
    # Процессы по числу процессоров
    with Pool(processes=cpu_count()) as pool:
        # Создаём процессы и ждём их выполнения (синхронно)
        factors_list = pool.map(process_number, data)
        for num, factors in zip(data, factors_list):
            results.append((num, factors))
    return results


def worker(input_queue, output_queue):
    while True:
        try:
            task = input_queue.get(timeout=1)
            if task is None:
                break
            num = task
            factors = process_number(num)
            output_queue.put((num, factors))
        except Exception:
            break


# Ручное управление процессами, ожидаем что будет немного медленнее чем на
# пуле процессов. Предпологаю из-за того, что каждый раз их поднимаем, а не
# переиспользуем
def process_with_manual_processes(data):
    num_processes = cpu_count()
    input_queue = Queue()  # Отсюда берём
    output_queue = Queue()  # Сюда кладём

    # Кидаем данные в очередь для воркеров, чтобы они, из разных процессов
    # могли получить доступ к числам, очередь позволяет процессам брать данные
    # без блокировок
    for num in data:
        input_queue.put(num)

    # Кидаем в очередь сигналы для завершения
    for _ in range(num_processes):
        input_queue.put(None)

    # Запускаем процессы
    processes = []
    for _ in range(num_processes):
        p = Process(target=worker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    # Вытаскиваем данные из очереди
    results = []
    for _ in range(len(data)):
        result = output_queue.get()
        results.append(result)

    for p in processes:
        p.join()

    results.sort(key=lambda x: data.index(x[0]))
    return results


def save_results_to_csv(results, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["number", "factors", "factors_count"])
        for num, factors in results:
            factors_str = "×".join(str(f) for f in factors) if factors else "1"
            writer.writerow([num, factors_str, len(factors)])


def compare_performance(data):  # Вайбкод
    methods = {
        "Последовательный": sequential_processing,
        "ThreadPool": process_with_threadpool,
        "ProcessPool": process_with_processpool,
        "Ручные процессы": process_with_manual_processes,
    }

    results = {}
    timing_results = {}

    for name, func in methods.items():
        start_time = time.time()
        results[name] = func(data)
        timing_results[name] = time.time() - start_time

    if "ProcessPool" in results:
        save_results_to_csv(results["ProcessPool"], "results.csv")

    return timing_results, results


def main():  # Вайбкод
    random.seed(42)
    data = generate_data(100000)
    timing, all_results = compare_performance(data)

    print(f"{'Метод':<20} {'Время (сек)':<12} {'Ускорение':<10}")
    print("-" * 42)

    for name, time_taken in timing.items():
        if name == "Последовательный":
            speedup = 1.0
        else:
            speedup = timing["Последовательный"] / time_taken
        print(f"{name:<20} {time_taken:<12.2f} {speedup:<10.2f}x")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()


""" Сетап: "два ядра, два гига, игровая видеокарта"
Метод                Время (сек)  Ускорение
------------------------------------------
Последовательный     89.78        1.00      x
ThreadPool           92.84        0.97      x
ProcessPool          50.19        1.79      x
Ручные процессы      56.12        1.60      x
"""

""" Сетап: "восьмиядерный обогреватель, 16 процов, 16 гигов"
Метод                Время (сек)  Ускорение
------------------------------------------
Последовательный     68.34        1.00      x
ThreadPool           67.46        1.01      x
ProcessPool          15.71        4.35      x
Ручные процессы      18.25        3.74      x
"""
