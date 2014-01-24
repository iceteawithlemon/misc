# Intro to Quantics Term Project
# Quantum Cryptography Simulation

from random import randint


# Photons & polaroid filters

photon_symbols = ["_", "\\", "|", "/"] # 0 & 2 (resp. 1 & 2) must be of same scheme (x or +),  _ & \ = 0, | & / = 1
filters_symbols = ["+", "x"] # = schemes

def get_photons(length): # returns a list of photons and a list of their corresponding filters
	photons = ''
	filters = ''
	for i in range(0, length):
		n = randint(0, 3) 			 # pseudo-random
		photons += photon_symbols[n]
		filters += filters_symbols[n%2]
	return photons, filters

def filter_photons_random(photons): # returns a list of photons filtered through randomly chosen filters and the filters used
	filters = ''
	filtered = ''
	for photon in photons:
		f = randint(0, 1)
		filters += filters_symbols[f]
		photon = filter_given(photon, filters_symbols[f])
		filtered += photon
	return filtered, filters



def filter_photons_given(photons, filters): # returns values from correctly filtering values
	for i in range(0, len(photons)):
		photons[i] = filter_given(photons[i], filters[i])
	return photons

def filter_given(given_photon, given_filter): # filters a given photon through a given filter and returns the resulting photon (= polaroid)
	p = photon_symbols.index(given_photon)
	f = filters_symbols.index(given_filter)
	if p%2 == f: # then same filter
		return given_photon
	else:
		return photon_symbols[f + randint(0,1)*2]

def get_values_photons(photons): # returns list of corresponding numeric value for each photon
	values = ''
	for photon in photons:
		values += str(int((photon_symbols.index(photon) >= 2)))
	return values

def compare_filters_photons(photons, a_filters, b_filters): # returns list of photons that were correctly measured by both a and b
	correct_photons = ''
	for i in range(0, len(photons)):
		if a_filters[i] == b_filters[i]:
			correct_photons += photons[i]
	return correct_photons

def compare_filters_values(values, a_filters, b_filters): # returns list of values that were correctly measured by both a and b
	correct_values = ''
	for i in range(0, len(values)):
		if a_filters[i] == b_filters[i]:
			correct_values += values[i]
	return correct_values


def error_count(a_values, b_values):
	errors = 0
	n = 0
	for i in range(0, len(a_values)):
		n += 1
		if a_values[i] != b_values[i]:
			errors += 1
	return (errors/n)*100


def check_if_NSA(a_values, b_values): # checks a small amount of values 
	for i in range(len(a_values)):
		if a_values[i] != b_values[i]:
			return True
	return False












# Vernam cipher / 'one-time pad'
accepted_punctuation = [' ', '.', ',', '?', '!', ':'] # no more than 6
def char_to_ascii(char, punctuation = True): # A/a => 0 => 00000 ... Z => 25, ' ' => 26, '.' => 27, ',' => 28, '?' => 29, '!' => 30
	ascii = ord(char) # ascii 
	if 65 <= ascii and ascii <= 90:
		return ascii - ord('A') # returns an int
	elif punctuation and char in accepted_punctuation:
		return 26 + accepted_punctuation.index(char) 

def ascii_to_binary(ascii):
	binary = bin(ascii)[2:] # converts int to binary in form '0b11' then to form '11' (string)
	binary =  '0'*(5-len(binary)) + binary # adds '0's to binary (string)
	return binary

def char_to_binary(char, punctuation = True):
	return ascii_to_binary(char_to_ascii(char, punctuation))


def binary_to_char(binary, punctuation = True):
	char = ''
	binary = int(binary, 2) # converts binary (as string) to decimal (as int) 
	if binary <= 25:
		return chr(ord('A') + binary)
	elif punctuation and (binary - 26) < 6:
		return accepted_punctuation[binary-26]

def encrypt_vernam(plain_text, key):
	plain_text = plain_text.upper() #string
	cipher_text = ''
	i = 0
	for char in plain_text:
		tmp = ''
		binary = char_to_binary(char) #get binary of char
		for bit in binary:
			tmp += str(int(bit != key[i%len(key)])) # str(int()) converts the boolean to 0 or 1, and != <=> XOR, i%len(key) ensures wrap-around in case key is too short
			i += 1
		cipher_text += binary_to_char(tmp) # converts encrypted binary back to char
	return cipher_text

def transfer_noisy_channel(photons):
	out = ''
	for i in range(0, len(photons)):
		if i % 10 == 0:
			out += photon_symbols[randint(0, 3)]
		else:
			out += photons[i]
	return out



input("Continue? ")
# Simulation PART 1 (finding a key, no spy)

# 1. Alice sends a series of 50 photons to Bob
print()
alice_sends = get_photons(100)
alice_photons = alice_sends[0]
alice_filters = alice_sends[1]
alice_values = get_values_photons(alice_photons)

# 2. Bob receives the photons and passes each one through a randomly chosen filter

bob_gets = filter_photons_random(alice_photons)

bob_photons = bob_gets[0]
bob_filters = bob_gets[1]
bob_values = get_values_photons(bob_photons)

print("Alice sent: ", alice_photons)
print("Bob received", bob_photons)
print()
alice_photons = ''
bob_photons = ''

# 3. Alice and Bob publicly compare filters and keep the values found with the correct filters

print("Alice's filters: \n\t" + alice_filters)
print("Bob's filters: \n\t" + bob_filters)
print()
print("Alice sent: ", alice_values)
print("Bpb got: ", bob_values)
print("Error count: \n\t" + str(error_count(alice_values, bob_values)) + "%")
print()

alice_values = compare_filters_values(alice_values, alice_filters, bob_filters)
bob_values = compare_filters_values(bob_values, alice_filters, bob_filters)

# 4. Alice and Bob publicly compare some of their values to see if they have the same values. If yes, all is well. If not, they've been spied on.

alice_check = alice_values[:10]
bob_check = bob_values[:10]

print("Alice's values to check: \n\t" + alice_check)
print("Bob's values to check: \n\t" + bob_check)
print()
print("Alice and Bob have been spied on: " + str(check_if_NSA(alice_check, bob_check)))
print()
key = alice_values[10:]

print("Alice and Bob now have a key that only they know: \n\t" + key)

print()

input("Continue? ")

# Simulation PART 2 (using the key)

print("Alice will now encrypt a message using this key, and Bob will decrypt it. ")

#test = "Intro to Quantics Term Project: Quantum Cryptography Simulation"
test = input("Message to encrypt? ")
test_encrypt = encrypt_vernam(test, key)
print("Key: \n\t" + key)
print("Plain-text: \n\t" + test.upper())
print("(Alices encrypts and sends) 1st encryption: \n\t" + test_encrypt)
print("(Bob gets and decrypts) 2nd (un)encryption: \n\t" + encrypt_vernam(test_encrypt, key))


print()
print()
print()
print("But what if someone spies on them?\n")


input("Continue? ")
# Simulation PART 1B (finding a key, with spy)

# 1. Alice sends a series of 50 photons to Bob

alice_sends = get_photons(100)
alice_photons = alice_sends[0]
alice_filters = alice_sends[1]
alice_values = get_values_photons(alice_photons)

# 2. A. The NSA receive the photons and pass each one through a randomly chosen filter, then send them on to Bob

nsa_gets = filter_photons_random(alice_photons)
nsa_photons = nsa_gets[0]
nsa_filters = nsa_gets[1]
nsa_values = get_values_photons(nsa_photons)


# 2.B. Bob recieves the tampered-with photons and passes them through his randomly chosen filters

bob_gets = filter_photons_random(nsa_photons)

bob_photons = bob_gets[0]
bob_filters = bob_gets[1]
bob_values = get_values_photons(bob_photons)

# print(alice_photons)
# print(bob_photons)
# print(nsa_photons)

alice_photons = ''
bob_photons = ''
nsa_photons = ''


# 3. Alice and Bob publicly compare filters and keep the values found with the correct filters

print("Alice's filters: \n\t" + alice_filters)
print("The NSA's filters: \n\t" + nsa_filters)
print("Bob's filters: \n\t" + bob_filters)
print("Error count: \n\t" + str(error_count(alice_values, bob_values)) + "%")

alice_values = compare_filters_values(alice_values, alice_filters, bob_filters)
bob_values = compare_filters_values(bob_values, alice_filters, bob_filters)

# 4. Alice and Bob publicly compare some of their values to see if they have the same values. If yes, all is well. If not, they've been spied on.

alice_check = alice_values[:10]
bob_check = bob_values[:10]

print("Alice's values to check: \n\t" + alice_check)
print("Bob's values to check: \n\t" + bob_check)


print("Alice and Bob have been spied on: " + str(check_if_NSA(alice_check, bob_check)))

#print("Key: \n\t" + alice_values[10:])