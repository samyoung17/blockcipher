import sys
import time
import string

def toBin(s):
	return bin(int.from_bytes(s.encode('ascii'),'big')).lstrip('0b')

def toString(b):
	n = int(b,2)
	return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('ascii', 'replace')

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

def isPrinatble(c):
	return c in string.printable and c not in '\t\n\r\x0b\x0c'

def isText(c):
	return c in string.ascii_lowercase or c == ' '

def matches(text):
	return all(list(map(isText,text)))

def printText(text):
	printableText = ''.join(list(filter(isPrinatble,text)))
	whiteSpace = (len(text) - len(printableText)) * ' '
	sys.stdout.write('\r' + printableText + whiteSpace)
	sys.stdout.flush()

def bruteForce(keyLength, cipher):
	plainText = ''
	for l in range(1, keyLength):
		for i in range(1, 2**l):
			try:
				k = bin(i).lstrip('0b').zfill(l)
				plainText = decrypt(cipher, k)
				if i % 1000 == 0:
					printText(plainText)
				if matches(plainText):
					printText(plainText)
					break
			except UnicodeDecodeError:
				sys.stdout.write('\r' + 'afds')
				continue
		if matches(plainText):
					break

def main():
	print('***** Brute force attack analysis tool *****')
	plainText = input('Enter text to encrypt: ')
	key = input('Enter binary encryption key: ')
	print('Encrypting secret message...')
	time.sleep(1)
	print('***** Begin secret message *****')
	cipher = encrypt(plainText, key)
	print(cipher)
	print('***** End secret message *****')
	input('Press enter to commence attack...')
	print('***** Starting brute force attack *****')
	start = time.time()
	bruteForce(200, cipher)
	end = time.time()
	print('\n***** Brute force attack successful *****')
	print('Decrypted in ' + str(end - start) + 's')

if __name__ == '__main__':
	main()
