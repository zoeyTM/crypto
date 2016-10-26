# Affine Cipher

import sys, pyperclip, cryptoMath, random
SYMBOLS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~""" # note the space at the front


def main():
    myMessage = input('Enter your text: ')
    while True:
        myMode = input('encrypt or decrypt? ') # set to 'encrypt' or 'decrypt'
        if myMode.lower() == 'decrypt':
            myKey = int(input('Enter your decryption key: '))
            print()
            break
        elif myMode.lower() == 'encrypt':
            myKey = getRandomKey()
            print()
            break
        else:
            print("Please enter either 'encrypt' or 'decrypt'.")
            print()
    
    if myMode.lower() == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode.lower() == 'decrypt':
        translated = decryptMessage(myKey, myMessage)
    print('Key: %s' % (myKey))
    print('%sed text: ' %(myMode.title()))
    print(translated)
    pyperclip.copy(translated)
    print('Full %sed text copied to clipboard.' %(myMode))


def getKeyParts(key):
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)
    return (keyA, keyB)


def checkKeys(keyA, keyB, mode):
    if keyA == 1 and mode == 'encrypt':
        print('The affine cipher becomes incredibly weak when key A is set to 1. Choose a different key.')
        sys.exit()
    if keyB == 0 and mode == 'encrypt':
        print('The affine cipher becomes incredibly weak when key B is set to 0. Choose a different key.')
        sys.exit()
    if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS) - 1:
        print('Key A must be greater than 0 and Key B must be between 0 and %s.' %(len(SYMBOLS) - 1))
        sys.exit()
    if cryptoMath.gcd(keyA, len(SYMBOLS)) != 1:
        print('Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' %(keyA, len(SYMBOLS)))
        sys.exit()


def encryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'encrypt')
    ciphertext = ''
    for symbol in message:
        if symbol in SYMBOLS:
            # encrypt this symbol
            symIndex = SYMBOLS.find(symbol)
            ciphertext += SYMBOLS[(symIndex * keyA + keyB) % len(SYMBOLS)]
        else:
            ciphertext += symbol # just append this symbol unencrypted
    return ciphertext


def decryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'decrypt')
    plaintext = ''
    modInverseOfKeyA = cryptoMath.findModInverse(keyA, len(SYMBOLS))

    for symbol in message:
        if symbol in SYMBOLS:
            # decrypt this symbol
            symIndex = SYMBOLS.find(symbol)
            plaintext += SYMBOLS[(symIndex - keyB) * modInverseOfKeyA % len(SYMBOLS)]
        else:
            plaintext += symbol # just append this symbol undecrypted
    return plaintext


def getRandomKey():
    while True:
        keyA = random.randint(2, len(SYMBOLS))
        keyB = random.randint(2, len(SYMBOLS))
        if cryptoMath.gcd(keyA, len(SYMBOLS)) == 1:
            return keyA * len(SYMBOLS) + keyB


# If affineCipher.py is run (instead of imported as a module) call
# the main() function.
if __name__ == "__main__":
    main()

