## Phil Lane

import math
import time
import matplotlib.pyplot as plt
import tracemalloc


class PrimeGenerator:

    @staticmethod
    def sieve_of_sundaram(limit):
        sieve = [True] * (limit // 2 + 1)
        primes = [2]

        for i in range(1, (limit // 2) + 1):
            j = i
            while (i + j + 2 * i * j) <= (limit // 2):
                sieve[i + j + 2 * i * j] = False
                j += 1

        for i in range(1, (limit // 2) + 1):
            if sieve[i]:
                primes.append(2 * i + 1)

        return primes

    @staticmethod
    def sieve_of_eratosthenes(limit):
        sieve = [False, False] + [True] * (limit - 1)

        for i in range(2, int(math.sqrt(limit)) + 1):
            if sieve[i]:
                for j in range(i * i, limit + 1, i):
                    sieve[j] = False

        primes = []
        for num in range(2, limit + 1):
            if sieve[num]:
                primes.append(num)

        return primes

    @staticmethod
    def segmented_sieve(limit):
        base_primes = PrimeGenerator.sieve_of_eratosthenes(int(math.sqrt(limit)))

        segment_size = int(math.sqrt(limit))
        primes = []

        for low in range(2, limit + 1, segment_size):
            high = min(low + segment_size - 1, limit)
            segment = [True] * (high - low + 1)

            for prime in base_primes:
                first_multiple = max(prime * prime, (low + prime - 1) // prime * prime)
                for j in range(first_multiple, high + 1, prime):
                    segment[j - low] = False

            primes.extend([i + low for i in range(len(segment)) if segment[i]])

        return primes


class PrimePerformanceAnalyzer:
    @staticmethod
    def analyze_performance_and_memory(limits):
        methods = [
            ("Sieve of Eratosthenes", PrimeGenerator.sieve_of_eratosthenes),
            ("Segmented Sieve", PrimeGenerator.segmented_sieve),
            ("Sundaram", PrimeGenerator.sieve_of_sundaram)
        ]

        performance_results = {}

        for limit in limits:
            performance_results[limit] = {}

            for name, method in methods:
                # Start memory tracking
                tracemalloc.start()

                start_time = time.time()
                start_memory = tracemalloc.get_traced_memory()[0]

                # Generate primes
                primes = method(limit)

                end_time = time.time()
                end_memory = tracemalloc.get_traced_memory()[0]

                # Stop memory tracking
                tracemalloc.stop()

                performance_results[limit][name] = {
                    "execution_time": end_time - start_time,
                    "prime_count": len(primes),
                    "first_primes": primes[:5],
                    "last_primes": primes[-5:],
                    "primes": primes,
                    "memory_used": end_memory - start_memory,  # Memory in bytes
                }

        return performance_results

    @staticmethod
    def visualize_performance(results):
        limits = list(results.keys())

        eratosthenes_times = [
            results[limit]["Sieve of Eratosthenes"]["execution_time"]
            for limit in limits
        ]
        segmented_times = [
            results[limit]["Segmented Sieve"]["execution_time"]
            for limit in limits
        ]

        sundaram_times = [
            results[limit]["Sundaram"]["execution_time"]
            for limit in limits
        ]

        plt.figure(figsize=(10, 6))
        plt.plot(limits, eratosthenes_times, label='Sieve of Eratosthenes', marker='o')
        plt.plot(limits, segmented_times, label='Segmented Sieve', marker='x')
        plt.plot(limits, sundaram_times, label='Sundaram', marker='*')

        plt.title('Prime Generation Algorithm Performance Comparison')
        plt.xlabel('Upper Limit')
        plt.ylabel('Execution Time (seconds)')
        plt.legend()
        plt.xscale('log')
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def visualize_memory_usage(results):
        limits = list(results.keys())

        eratosthenes_memory = [
            results[limit]["Sieve of Eratosthenes"]["memory_used"] / 1024 / 1024  # Convert to MB
            for limit in limits
        ]
        segmented_memory = [
            results[limit]["Segmented Sieve"]["memory_used"] / 1024 / 1024  # Convert to MB
            for limit in limits
        ]
        sundaram_memory = [
            results[limit]["Sundaram"]["memory_used"] / 1024 / 1024  # Convert to MB
            for limit in limits
        ]

        plt.figure(figsize=(10, 6))
        plt.plot(limits, eratosthenes_memory, label='Sieve of Eratosthenes', marker='o')
        plt.plot(limits, segmented_memory, label='Segmented Sieve', marker='x')
        plt.plot(limits, sundaram_memory, label='Sundaram', marker='*')

        plt.title('Prime Generation Algorithm Memory Usage')
        plt.xlabel('Upper Limit')
        plt.ylabel('Memory Usage (MB)')
        plt.legend()
        plt.xscale('log')
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def visualize_gaps(results, title, ylabel):
        plt.figure(figsize=(10, 6))
        plt.plot(results, label=title, marker='*')

        plt.title(f'{title}')
        plt.xlabel('Upper Limit')
        plt.ylabel(ylabel)
        plt.legend()
        plt.xscale('log')
        plt.grid(True)

        plt.tight_layout()
        plt.show()


def main():
    test_limits = [10_000, 100_000, 1_000_000, 10_000_000]

    performance_results = PrimePerformanceAnalyzer.analyze_performance_and_memory(test_limits)

    primes = performance_results[100_000]["Sieve of Eratosthenes"]["primes"]

    prime_gaps = [primes[i] - primes[i - 1] for i in range(1, len(primes))]

    twin_primes = [
        (primes[i - 1], primes[i])
        for i in range(1, len(primes))
        if primes[i] - primes[i - 1] == 2
    ]

    twin_prime_gaps = [
        twin_primes[i][0] - twin_primes[i - 1][0]
        for i in range(1, len(twin_primes))
    ]

    for limit, methods in performance_results.items():
        print(f"\nPerformance Analysis for Limit: {limit}")
        for method_name, stats in methods.items():
            print(f"\n{method_name}:")
            print(f"  Execution Time: {stats['execution_time']:.4f} seconds")
            print(f"  Prime Count: {stats['prime_count']}")
            print(f"  Memory Used: {stats['memory_used'] / 1024 / 1024:.4f} MB")
            print(f"  First 5 Primes: {stats['first_primes']}")
            print(f"  Last 5 Primes: {stats['last_primes']}")

    PrimePerformanceAnalyzer.visualize_performance(performance_results)
    PrimePerformanceAnalyzer.visualize_memory_usage(performance_results)
    PrimePerformanceAnalyzer.visualize_gaps(prime_gaps, 'Prime Number Gaps', 'Gap Size (number of non-primes)')
    PrimePerformanceAnalyzer.visualize_gaps(twin_prime_gaps, 'Twin Prime Gaps', 'Gap Size Between Twin Primes')

if __name__ == "__main__":

    main()
