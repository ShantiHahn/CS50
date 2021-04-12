import math

def is_prime(n):

	#we know numbers less than 2 are not prime
	if n<2:
		return False
		
	# Checking factors up to sqrt(n)
	for i in range(2, int(math.sqrt(n)) + 1):
		
	
		#If i is a factor return false
		#print(i)
		if n % i == 0:
			return False
			
	# If no factors were found, return true
	
	return True



#for i in range(2, 100):
#	print( i, ":", is_prime(i))

#print(is_prime(89))
#print(is_prime(4))

def test_prime(n, expected):
	if is_prime(n) != expected:
		print(f"Error on is_prime({n}), expected {expected}")
