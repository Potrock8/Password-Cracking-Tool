import zipfile
from colorama import Fore



file = str(input("Please inpute your zip file:"))
wordlist1 = str(input("Please inpute your wordlist:"))

def main():
	"""
	Zipfile password cracker using a brute-force dictionary attack.
	"""
	zipfilename = file
	dictionary = wordlist1

	password = None
	zip_file = zipfile.ZipFile(zipfilename)
	with open(dictionary, 'r') as f:
		for line in f.readlines():
			password = line.strip('\n')
			try:
				zip_file.extractall(pwd=password)
				password = 'Password found: %s' % password
			except:
				pass
	print("Password:"+ password)

if __name__ == '__main__':
	main()
