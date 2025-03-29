# Импортируем необходимые модули
 import multiprocessing  # Для параллельных вычислений
 import sys  # Для работы с аргументами командной строки
 import os   # Для получения информации о системе
 
 # Функция для чтения матрицы из файла
 def read_matrix(filename):
 @@ -19,6 +20,9 @@
         for line in f:
             # Убираем лишние пробелы и символы перевода строки
             line = line.strip()
             # Проверяем, не является ли строка пустой
             if not line:
                 continue  # Пропускаем пустые строки
             # Разделяем строку на отдельные элементы по пробелам
             str_numbers = line.split()
             # Преобразуем каждую строку в число (float)
 @@ -93,60 +97,68 @@
         for j in range(result_cols):
             indices.append((i, j))  # Добавляем кортеж индексов (i, j)
 
     # Определяем количество процессов
     num_processes = 4  # Задаем заранее количество процессов, например, 4
     # Определяем количество процессов автоматически
     # Используем количество процессоров в системе
     num_cores = multiprocessing.cpu_count()
 
     # Можно ограничить максимальное количество процессов, если это необходимо
     max_processes = 8  # Например, не более 8 процессов
     num_processes = min(num_cores, max_processes)
 
     print(f"Количество ядер в системе: {num_cores}")
     print(f"Будет использовано процессов: {num_processes}")
 
     # Создаем менеджер для управления общими ресурсами
     manager = multiprocessing.Manager()
     lock = manager.Lock()  # Создаем Lock для синхронизации записи в файл
 
     # Имя промежуточного файла для записи элементов сразу после вычисления
     intermediate_file = 'intermediate_results.txt'
 
     # Перед началом вычислений очищаем (если существует) или создаем новый промежуточный файл
     open(intermediate_file, 'w').close()
 
     # Подготавливаем аргументы для функции compute_and_write_element
     args = []  # Инициализируем список аргументов
     for index in indices:
         args.append((index, A, B, intermediate_file, lock))  # Добавляем необходимые аргументы
 
     # Создаем пул процессов для параллельного выполнения
     with multiprocessing.Pool(processes=num_processes) as pool:
         # Параллельно вычисляем элементы и записываем их в файл
         pool.map(compute_and_write_element, args)
 
     # После вычислений необходимо собрать результаты из промежуточного файла и сформировать итоговую матрицу
     # Инициализируем пустую матрицу нужного размера
     result_matrix = []
     for i in range(result_rows):
         result_matrix.append([0] * result_cols)
 
     # Читаем данные из промежуточного файла
     with open(intermediate_file, 'r') as f:
         for line in f:
             # Убираем лишние пробелы и символы перевода строки
             line = line.strip()
             if not line:
                 continue  # Пропускаем пустые строки
             # Разбиваем строку на индексы и значение
             i_str, j_str, value_str = line.split()
             i = int(i_str)
             j = int(j_str)
             value = float(value_str)
             # Записываем значение в соответствующую позицию результирующей матрицы
             result_matrix[i][j] = value
 
     # Записываем результирующую матрицу в файл
     with open('result_matrix.txt', 'w') as f:
         for row in result_matrix:
             # Преобразуем числа в строки
             str_numbers = [str(num) for num in row]
             # Объединяем числа через пробел и добавляем перевод строки
             line = ' '.join(str_numbers) + '\n'
             # Записываем строку в файл
             f.write(line)
 
 # Проверяем, является ли данный скрипт основным (а не импортированным модулем)
 if __name__ == '__main__':
     # Запускаем основную функцию
