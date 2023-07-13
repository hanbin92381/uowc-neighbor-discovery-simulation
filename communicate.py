import argparse
from sys import path_importer_cache


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--num', type=int,
                           help='number of nodes', default=2)
    #argparser.add_argument('--')
    args = argparser.parse_args()
    return args


def get_primes(n):
    '''
    线性筛求3~100之间的前n个质数
    '''
    primes = []  # 存储所有素数
    st = [False] * 100  # 标记数是否被筛掉
    cnt = 0  # 素数个数
    
    for i in range(2, 100):
        if not st[i]:
            primes.append(i)
            cnt += 1
        
        for j in range(cnt):
            if primes[j] * i >= 100:
                break

            st[primes[j] * i] = True
            if i % primes[j] == 0:
                break
    
    return primes[1:n + 1]


if __name__ == "__main__":
    args = get_args()
    num = args.num
    
    primes = get_primes(num)
    primes = [11, 13, 17]
    packages = {key: 0 for key in primes}
    total_time = primes[num - 1] * primes[num - 2]

    print(primes)
    
    for i in range(total_time):
        cur = 0
        for j in primes:
            if cur == -1:
                break
            if i % j == 0:
                cur = j if cur == 0 else -1

        if cur > 0:
            packages[cur] += 1
            print(f'time {i}: prime {cur} - packages {packages[cur]}')

    result = total_time
    for _, num in packages.items():
        result = min(result, num)

    print(f'result: {result} packages')
