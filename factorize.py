import time
from multiprocessing import Pool, cpu_count

def factorize_single(number):
    factors = [i for i in range(1, number + 1) if number % i == 0]
    return factors

def factorize_sync(*numbers):
    result = [factorize_single(number) for number in numbers]
    return result

def factorize_parallel(*numbers):
    with Pool(cpu_count()) as pool:
        result = pool.map(factorize_single, numbers)
    return result

if __name__ == '__main__':
    # Тестові дані
    test_numbers = (128, 255, 99999, 10651060)

    a, b, c, d = test_numbers

    assert factorize_single(a) == [1, 2, 4, 8, 16, 32, 64, 128]
    assert factorize_single(b) == [1, 3, 5, 15, 17, 51, 85, 255]
    assert factorize_single(c) == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert factorize_single(d) == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    # Синхронна версія
    start_time = time.time()
    result_sync = factorize_sync(*test_numbers)
    end_time = time.time()
    print("Синхронна версія:")
    print(result_sync)
    print(f"Час виконання: {end_time - start_time:.4f} сек\n")

    # Паралельна версія
    start_time = time.time()
    result_parallel = factorize_parallel(*test_numbers)
    end_time = time.time()
    print("Паралельна версія:")
    print(result_parallel)
    print(f"Час виконання: {end_time - start_time:.4f} сек")