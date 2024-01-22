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