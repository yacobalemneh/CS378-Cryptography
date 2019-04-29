import random 
from math import *

# Yacob Alemneh
# CS 378
# SPRING 2019


def euclidsGcd(a,b): # this function computes GCD using euclids algorith,
    
    if a % b == 0: # if no remainder return b
        return b
    else:
        a = a % b # else set a as a % b
        return euclidsGcd(b,a) # call itself with new inputs


def randomPrime(lim): # function to generate random prime

	p = random.randrange(lim, pow(lim, 100)) # raise the given number to 100
	temp = p * (pow(10, 95)) # temp to store second value, to make sure second
	q = random.randrange(p, temp) # number is 10^95 greater than first. 

	while True: # while loop to check if generated numbers are prime. 
		if (fermatTest(p) == False and fermatTest(q) == False): # use fermatsTest
			p = random.randrange(lim, pow(lim, 100)) # generate again until prime
			temp = p * (pow(10, 95))
			q = random.randrange(p, temp)
		else:
			break # break if they're prime

	return p,q; # return the primes generated


def modularExp(a,p,n): # modular exponentiation algorithm

    if p == 0: # return 1 if p is 0
        return 1

    if p == 1: # return it self if only raised to 1
        return a

    q,r = divmod(p,2) # divmod returns the quotient and the remainder 

    if r == 1:
        return modularExp(a*a % n, q, n) * a % n # if remainder one call self with given arguments
    else:
        return modularExp(a*a % n, q, n) 


def extendedEuclids(a, b): # Takes in two numbers, finds gcd(a, b) and returns 
    if a == 0:			# gcd(a, b) = d, ax + by = d i.e (g, x, y) where y = d
        return (b, 0, 1)  

    else:
        temp = b % a # temp to store b mod a
        g, x, y = extendedEuclids(temp, a) # call self with temp value and a
        y = y - (b // a) * x # set y to new value
        return (g, y, x) # return 
 

def modularInverse(a, b): # function uses extendedEuclic and returns 
    g, x, y = extendedEuclids(a, b) # mod inverse

    if g != 1:
        return None
    return x % b


def fermatTest(n): # function to test primality

    checkList =[]
    if n < 2:
        return False

    x =  n - 1
    for i in range(5): # check with 5 different values of a
        a = random.randrange(2, x-1)
        if (modularExp(a, x, n) == 1):
            checkList.append('checked')
        
    if len(checkList) == 5:
        return True
    else:
        return False


def keySetup():
	myListPublic =[]
	myListPrivate = []

	p, q = randomPrime(5) # generate primes
	n = p * q # set up n
	phi = (p - 1) * (q -1) # set up phi
	e = 65537 

	while True:
		if (euclidsGcd(phi, 65537) == 1): # check if e and phi are co-prime
			break
		else:
			p, q = randomPrime(5) # generate new primes if not
			n = p * q
			phi = (p - 1) * (q -1)

	publiic_key = open("publiic_key.txt", "w+") # open files to write
	private_key = open("private_key.txt", "w+")
	
	myListPublic.append(str(n)) # store n and e in files
	myListPublic.append(str(e))
	for i in myListPublic:
		publiic_key.write(str(i)) 
		publiic_key.write('\n')
	publiic_key.close()

	
	privateKey = modularInverse(e, phi) # calculate d using modular inverse
	private_key.write(str(privateKey)) # algorithm and store in file
	private_key.close()



def encryption():

	myKeyPublic =[]
	myMessage = []
	ciphertext = open("ciphertext.txt", "w+") # open files to read and 
	publiic_key = open("publiic_key.txt", "r") # write on
	message = open("message.txt", "r") 

	for key in publiic_key:
		myKeyPublic.append(key.rstrip('\n')) # retrieve n and e

	n = int(myKeyPublic[0])
	e = int(myKeyPublic[1])
	
	for messages in message:
		myMessage.append(messages) # retrieve message from file


	mesToEncrypt = int(myMessage[0]) 
	encryptedMessage = modularExp(mesToEncrypt, e, n) # encrypt using modular
	ciphertext.write(str(encryptedMessage)) # exponentiatoin algorithm
	ciphertext.close()


def decryption():

	myKeyPrivate = [] 
	myKeyPublic = []
	cipherMessage = []
	ciphertext = open("ciphertext.txt", "r") # open files to be read and written on
	private_key = open("private_key.txt", "r")
	publiic_key = open("publiic_key.txt", "r")
	decrypted_message = open("decrypted_message.txt", "w+")

	for key in private_key: # read private key
		myKeyPrivate.append(key.rstrip('\n')) 

	for key in publiic_key: # read public key
		myKeyPublic.append(key.rstrip('\n'))

	n = int(myKeyPublic[0]) # retirece n, e and d
	e = int(myKeyPublic[1])
	d = int(myKeyPrivate[0])

	for message in ciphertext: # retrieve cipher message
		cipherMessage.append(message)

	mesToDecrypt = int(cipherMessage[0])
	
	decryptedMessage = modularExp(mesToDecrypt, d, n) # decrypt using modular exponentiaion
	decrypted_message.write(str(decryptedMessage)) 	# algorithm
	decrypted_message.close()
	
	
def main(): # main function
  
	keySetup()  # call to key setup
	encryption() # call to encryption
	decryption() # call to decryption

main()



















