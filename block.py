import sys
import time

WORDS = ['the ', ' of ', ' and ', ' to ', ' in ', ' for ', ' is ', ' on ', ' that ', ' by ', ' this ', ' with ', ' you ', ' it ', ' not ', ' or ', ' be ', ' are ', ' from ', ' at ', ' as ', ' your ', ' all ', ' have ', ' new ', ' more ', ' an ', ' was ', ' we ', ' will ', ' home', ' can ', ' us ', ' about ', ' if ', ' page ', ' my ', ' has ', ' search ', ' free ', ' but ', ' our ', ' one ', ' other ', ' do ', ' no ', ' information ', ' time ', ' they ', ' site ', ' he ', ' up ', ' may ', ' what ', ' which ', ' their ', ' news ', ' out ', ' use ', ' any ', ' there ', ' see ', ' only ', ' so ', ' his ', ' when ', ' contact ', ' here ', ' business ', ' who ', ' web ', ' also ', ' now ', ' help ', ' get ', ' pm ', ' view ', ' online ', ' first ', ' am ', ' been ', ' would ', ' how ', ' were ', ' me ', ' services ', ' some ', ' these ', ' click ', ' its ', ' like ', ' service ', ' than ', ' find ']

def toBin(s):
	return bin(int.from_bytes(s.encode('ascii'),'big')).lstrip('0b')

def toString(b):
	n = int(b,2)
	return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('ascii')

def repeatBinary(b, l):
	div = l // len(b)
	r = l % len(b)
	return bin(int(b * div + b[:r],2)).lstrip('0b')

def xor(a,b):
	return bin(int(a,2) ^ int(b,2)).lstrip('0b').zfill(len(a))

def encrypt(text, key):
	textBin = toBin(text)
	repeatedKeyBin = repeatBinary(key, len(textBin))
	return xor(textBin, repeatedKeyBin)

def decrypt(cipher, key):
	repeatedKeyBin = repeatBinary(key, len(cipher))	
	return toString(xor(cipher, repeatedKeyBin))

def testDeciphering():
	key = bin(2**14 - 132).lstrip('0b')
	cipher = encrypt('the cat in the hat', key)
	print(cipher)
	decipher = decrypt(cipher, key)
	print(decipher)

def matches(text):
	for word in WORDS:
		if text.find(word) >= 0:
			return True
	return False

def bruteForce(keyLength, cipher):
	for i in range(1, 2**keyLength):
		try:
			k = bin(i).lstrip('0b').zfill(keyLength)
			plainText = decrypt(cipher, k)
			sys.stdout.write('\r' + plainText)
			sys.stdout.flush()
			if matches(plainText):
				break
		except UnicodeDecodeError:
			continue

def testBruteForce():
	l = 22
	key = bin(2**l - 132).lstrip('0b')
	cipher = encrypt('the cat in the hat generated a massive pink cat ring', key)
	print('Starting brute force attack...')
	start = time.time()
	bruteForce(l, cipher)
	end = time.time()
	print('\nDecrypted in ' + str(end - start) + 's')

if __name__ == '__main__':
	testBruteForce()
