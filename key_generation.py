import random
from first_primes_list import FirstPrimesManager

class RSA:

    MILLER_RABIN_TRIALS = 20

    def __init__(self, key_size):
        self.n = 2048
        self.primes = FirstPrimesManager()
        self.first_primes_list = self.primes.load_cache('primes_cache')

    def _n_bit_random(self) -> int:
        '''
        Return a number between
        (2^(n-1))+1 and (2^n)-1
        '''
        return (random.randrange(2**(self.n-1)+1, (2**self.n)-1))

    def _miller_rabin_test(self, miller_rabin_candidate) -> bool:
        '''
        Perform 20 iterations of the Miller-Rabin Primality test.
        Successfully passing this test once means there is a 75% chance a given number is prime.
        Therefore, the pobability of a candidate prime number being not prime is 1/(2^128) after 20 successful tests. 
        This extremely low probability means we can proceed with RSA knowing we have generated a prime number.
        '''
        max_divisions_by_two = 0
        even_component = miller_rabin_candidate-1

        while even_component % 2 == 0:
            even_component >>= 1
            max_divisions_by_two += 1
        assert(2**max_divisions_by_two * even_component == miller_rabin_candidate-1)

        def _trial_composite(round_tester):
            if pow(round_tester, even_component,
                miller_rabin_candidate) == 1:
                return False
            for i in range(max_divisions_by_two):
                if pow(round_tester, 2**i * even_component, miller_rabin_candidate) == miller_rabin_candidate-1:
                    return False
            return True
        
        for i in range(RSA.MILLER_RABIN_TRIALS):
            round_tester = random.randrange(2,miller_rabin_candidate)
            if _trial_composite(round_tester):
                return False
        return True

    def _get_low_level_prime(self):
        '''Generate a prime candidate not divisible
        by first primes list'''
        # Repeat until a number satisfying
        # the test isn't found
        while True: 
            prime_candidate = self._n_bit_random()
    
            for divisor in self.first_primes_list: 
                if prime_candidate % divisor == 0 and divisor**2 <= prime_candidate:
                    break
                # If no divisor found, return value to take the Miller-Rabin Test
                else: 
                    return prime_candidate

    def generate_primes(self):
        primes = [0] * 3
        for i in range(0, len(primes)):
            while True:
                prime_candidate = self._get_low_level_prime()
                if i == (len(primes) - 1):                        #Section calculates the value e and stores it as the last element in the primes[] list
                    while True:
                        e_candidate = self._get_low_level_prime()
                        if e_candidate >= ((primes[0] - 1) * (primes[1] - 1)):
                            continue
                        else:
                            if not self._miller_rabin_test(e_candidate):
                                continue
                            else:
                                prime_candidate = e_candidate
                            break

                if not self._miller_rabin_test(prime_candidate):
                    continue
                else:
                    primes[i] = prime_candidate
                    print(self.n, "bit prime is: \n", primes[i])
                    if primes[(len(primes) - 1)] != 0:
                        print("e = ", primes[(len(primes) - 1)])
                    break