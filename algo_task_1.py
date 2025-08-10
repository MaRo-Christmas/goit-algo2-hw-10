import random
import time
import sys
from typing import List, Callable
import matplotlib.pyplot as plt
import pandas as pd

def _partition_lomuto(arr: List[int], low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def _deterministic_quicksort(arr: List[int], low: int, high: int) -> None:
    if low < high:
        mid = (low + high) // 2
        arr[mid], arr[high] = arr[high], arr[mid]
        p = _partition_lomuto(arr, low, high)
        _deterministic_quicksort(arr, low, p - 1)
        _deterministic_quicksort(arr, p + 1, high)


def deterministic_quick_sort(arr: List[int]) -> List[int]:
    a = list(arr)
    _deterministic_quicksort(a, 0, len(a) - 1)
    return a


def _randomized_quicksort(arr: List[int], low: int, high: int) -> None:
    if low < high:
        pivot_index = random.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
        p = _partition_lomuto(arr, low, high)
        _randomized_quicksort(arr, low, p - 1)
        _randomized_quicksort(arr, p + 1, high)


def randomized_quick_sort(arr: List[int]) -> List[int]:
    a = list(arr)
    _randomized_quicksort(a, 0, len(a) - 1)
    return a


def time_function(func: Callable[[List[int]], List[int]], data: List[int], repeats: int = 5) -> float:
    timings = []
    for _ in range(repeats):
        arr_copy = list(data)
        start = time.perf_counter()
        sorted_arr = func(arr_copy)
        end = time.perf_counter()
        assert all(sorted_arr[i] <= sorted_arr[i + 1] for i in range(len(sorted_arr) - 1)), "Помилка сортування"
        timings.append(end - start)
    return sum(timings) / len(timings)


def run_benchmark(sizes=(10_000, 50_000, 100_000, 500_000), repeats=5, seed=42):
    random.seed(seed)
    results = []
    for n in sizes:
        data = [random.randint(-10**9, 10**9) for _ in range(n)]
        avg_rand = time_function(randomized_quick_sort, data, repeats)
        avg_det = time_function(deterministic_quick_sort, data, repeats)
        results.append((n, avg_rand, avg_det))
        print(f"Розмір масиву: {n}")
        print(f"   Рандомізований QuickSort: {avg_rand:.4f} секунд")
        print(f"   Детермінований QuickSort: {avg_det:.4f} секунд\n")
    return results

if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)

    results = run_benchmark()

    # Таблиця
    df = pd.DataFrame(results, columns=["Розмір масиву", "Рандомізований QuickSort (с)", "Детермінований QuickSort (с)"])
    print(df)

    # Графік
    plt.figure(figsize=(7, 5))
    plt.plot(df["Розмір масиву"], df["Рандомізований QuickSort (с)"], marker="o", label="Рандомізований QuickSort")
    plt.plot(df["Розмір масиву"], df["Детермінований QuickSort (с)"], marker="o", label="Детермінований QuickSort")
    plt.xlabel("Розмір масиву")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння рандомізованого та детермінованого QuickSort")
    plt.legend()
    plt.tight_layout()
    plt.show()
