# -*- coding: utf-8 -*-
'''RSA.py'''

# LARGE PRIME NUMBER GENERATION FOR RSA

#Random number generation by calling nBitRandom(bitsize)
#Basic division test by calling getLowLevelPrime(prime_candidate)
#Rabin Miller Test by calling isMillerRabinPassed(prime_candidate)

import random
from first_primes_list import FirstPrimesManager

# Pre generated primes. We want a prime candidate not divisible by the first primes.
primes = FirstPrimesManager()
first_primes_list = primes.load_cache('primes_cache')

def nBitRandom(L):
   
    # Returns a random number
    # between (2^(n-1))+1 and (2^n)-1

      return(random.randrange(2**(n-1)+1, (2**n)-1))

def getLowLevelPrime(n):
    '''Generate a prime candidate not divisible
      by first primes'''
   
    # Repeat until a number satisfying
    # the test isn't found
    while True: 
   
        # Obtain a random number
        prime_candidate = nBitRandom(n)
   
        for divisor in first_primes_list: 
            if prime_candidate % divisor == 0 and divisor**2 <= prime_candidate:
                break
            # If no divisor found, return value to take the Miller-Rabin Test
            else: 
              return prime_candidate

  #MILLER-RABIN TEST
  #20 iterations of Rabin Miller Primality test run here
  #Successfully passing this test once means there is a 75% chance the number is prime
  #The pobability of the candidate prime number being not prime is 1/(2^128) after 20 successful tests. (Very low probability)

def isMillerRabinPassed(miller_rabin_candidate):

	maxDivisionsByTwo = 0
	evenComponent = miller_rabin_candidate-1

	while evenComponent % 2 == 0:
		evenComponent >>= 1
		maxDivisionsByTwo += 1
	assert(2**maxDivisionsByTwo * evenComponent == miller_rabin_candidate-1)

	def trialComposite(round_tester):
		if pow(round_tester, evenComponent,
			miller_rabin_candidate) == 1:
			return False
		for i in range(maxDivisionsByTwo):
			if pow(round_tester, 2**i * evenComponent, miller_rabin_candidate) == miller_rabin_candidate-1:
				return False
		return True

	# Set number of trials here
	numberOfRabinTrials = 20
	for i in range(numberOfRabinTrials):
		round_tester = random.randrange(2,miller_rabin_candidate)
		if trialComposite(round_tester):
			return False
	return True

# PROGRAM START
# Large primes p & q are found and stored in a list called primes[]
# L controls the bit security of RSA

if __name__ == '__main__':
  primes = [0] * 3
for i in range(0, len(primes)):
    while True:
          n = 1024   # Set n to be the key length
          prime_candidate = getLowLevelPrime(n)
          if i == (len(primes) - 1):                                              #Section calculates the value e and stores it as the last element in the primes[] list
            while True:
              e_candidate = getLowLevelPrime(n)
              if e_candidate >= ((primes[0] - 1) * (primes[1] - 1)):
                continue
              else:
                if not isMillerRabinPassed(e_candidate):
                  continue
                else:
                  prime_candidate = e_candidate
                  break

          if not isMillerRabinPassed(prime_candidate):
            continue
          else:
              primes[i] = prime_candidate
              print(n, "bit prime is: \n", primes[i])
              if primes[(len(primes) - 1)] != 0:
                print("e = ", primes[(len(primes) - 1)])
              break

# KEY GENERATION

# The modInverse function takes e and the totient and return d to be part of the secret key. 
# inverse of e under modulo totient. This is an Iterative approach using the extended Euclidean algorithm.

# Returns modulo inverse of e with respect to the totient using extended Euclid Algorithm Assumption: e and the totient are
# coprimes, i.e., gcd(a, m) = 1

# Private Key Generator

def modInverse(a, m):
    m0 = m
    y = 0
    x = 1

    if (m == 1):
        return 0

    while (a > 1):
        # q is quotient
        q = a // m

        t = m

        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y

        # Update x and y
        y = x - q * y
        x = t

    # Make x positive
    if (x < 0):
        x = x + m0

    return x

p = primes[0]
q = primes[1]
n = p*q
totient = (p - 1) * (q - 1)

e = primes[2]

# Function call
d = modInverse(e, totient)

print("Modular multiplicative inverse is",d)

print("p = ", p)
print("q = ", q)
print("n = ", n)
print("totient = ", totient)
print("d = ", d)
print("e = ", e)

# Cipher Text Generation
def encrypt(msg, e, n):
  for i in range(len(msg)):
    msg[i] = pow(msg[i], e, n)
  return msg

msg = "Hello RSA!"
ascii_values = [ord(character) for character in msg]
c = encrypt(ascii_values, e, n)
print(c)

# Decryption
def decrypt(c, d, n):
  for i in range(len(c)):
    c[i] = pow(c[i], d, n)
  return msg

#ascii_values = [ord(character) for character in msg]
msg = decrypt(c, d, n)
print(msg)
