# Course ID:        CS3626
# Course name:      Cryptography
# Student name:     Marcelle Kembou Noukimi
# StudentID:        001024342
# Assignment #:     #2
# Due Date:         03/17/2021

# This function construct a linear key matrix, like for example, if
# if the plaintext is monarchy, then the linear key matrix will display MONARCHYBDEFGIKLPQSTUVWXZ
def Key(K):
    encryption_key = ''
    for char in K:
        # Unicode of characters of the alphabet in capital letter, ie, {A...Z} are in the range of [65,90] if the
        # unicode of a passed character is between the interval ]64,91[, then the char (in capital letter) is an
        # element of the alphabet
        if 64 < ord(char) < 91:
            # Change all 'J's in the plaintext to 'I'
            if char == 'J':
                char = 'I'
            encryption_key += char
    KM = ''
    for char in encryption_key:
        if char not in KM:
            KM += char
    return KM


# This function takes as input a plaintext (String type)
def Pre(P):
    # The preprocessing converts the plaintext into a list of two characters (PL)
    input_string = ''
    for char in P:
        # Unicode of characters of the alphabet in capital letter, ie, {A...Z} are in the range of [65,90] if the
        # unicode of a passed character is between the interval ]64,91[, then the char (in capital letter) is an
        # element of the alphabet
        if 64 < ord(char) < 91:
            # Change all 'J's in the plaintext to 'I'
            if char == 'J':
                char = 'I'
            input_string += char

    PL = ''
    # Know where we are in the list of 02 char blocks
    onFirstLetterOfCharBlocks = True
    for i in range(len(input_string)):
        if onFirstLetterOfCharBlocks:
            PL += input_string[i]

            # If the last block has one character, put an ‘x’ at the end
            if i + 1 == len(input_string):
                PL += 'X'

            # If two characters are equal, put an ‘x’ at the middle
            # or go onto second letter
            else:
                if input_string[i] == input_string[i + 1]:
                    PL += 'X'
                else:
                    onFirstLetterOfCharBlocks = False
        else:
            # just append second letter
            PL += input_string[i]
            onFirstLetterOfCharBlocks = True
    return PL


# The key matrix generator takes as input an encryption key and outputs the key
# matrix KM
def Display_5x5_KeyMatrix(K):
    print('Key Matrix:')
    KM = []
    for j in range(5):
        for i in range(5):
            KM.append(str(print(K[i + j * 5], ' ', end=' ')))
        print()
    print()
    return KM


# Break the message into two characters blocks
def break_plain_text_to_02_char_blocks(msg):
    space = True
    PL = []
    for char in msg:
        print(char, end='')
        space = not space
        if space:
            PL.append(str(print(' ', end='')))

    PL.append(str(print()))
    return PL


# This function takes as input the key matrix KM and the list of two characters PL
def Enc(KM, PL):
    outputString = ''
    for i in range(0, len(PL), 2):
        # extract letters in list of two characters PL
        lt1 = PL[i]
        lt2 = PL[i + 1]
        # find the key position
        pos1 = KM.find(lt1)
        pos2 = KM.find(lt2)
        # turn into coordinates
        crd1 = [pos1 % 5, pos1 // 5]
        crd2 = [pos2 % 5, pos2 // 5]

        # Case 1: If two characters are on the same column, each of which is replaced to a
        # character in the below cell. If a character is located at the bottom, a character in the
        # top cell should be taken.
        if crd1[1] == crd2[1] and lt1 + lt2 != 'XX':
            crd1[0] = (crd1[0] + 1) % 5
            crd2[0] = (crd2[0] + 1) % 5

        # Case 2: If two characters are on the same row, each of which is replaced to a
        # character in the right cell. If a character is located at the rightmost, a character in
        # the leftmost cell should be taken
        elif crd1[0] == crd2[0] and lt1 + lt2 != 'XX':
            crd1[1] = (crd1[1] + 1) % 5
            crd2[1] = (crd2[1] + 1) % 5

        # Case 3: “xx” will not be encrypted. It will be just “xx”.
        elif lt1 + lt2 == 'XX':
            outputString += 'XX'
            break

        # Case 4: Otherwise, two characters are replaced by the others on the other vertices,
        # e.g., List indices of two characters are (0, 4) and (3,1), then each of which is replaced
        # to a character in the (0,1) and (3,4), respectively
        else:
            tmp = crd2[0]
            crd2[0] = crd1[0]
            crd1[0] = tmp

        # go back from coordinates to key position
        pos1 = crd1[0] + 5 * crd1[1]
        pos2 = crd2[0] + 5 * crd2[1]

        # pull the new letter
        lt1 = KM[pos1]
        lt2 = KM[pos2]

        # build the output
        outputString += lt1
        outputString += lt2

    return outputString


# This function takes as input the key matrix KM and the list of two characters CL.
def Dec(K, CL):
    outputString = ''
    for i in range(0, len(CL), 2):
        # extract letters in list of two characters CL.
        lt1 = CL[i]
        lt2 = CL[i + 1]
        # find the key position
        pos1 = K.find(lt1)
        pos2 = K.find(lt2)
        # turn into coordinates
        crd1 = [pos1 % 5, pos1 // 5]
        crd2 = [pos2 % 5, pos2 // 5]

        # Case 1: If two characters are on the same column, each of which is replaced to a
        # character in the above cell. If a character is located at the top, a character in the
        # bottom cell should be taken.
        if crd1[1] == crd2[1] and lt1 + lt2 != 'XX':
            crd1[0] = (crd1[0] - 1) % 5
            crd2[0] = (crd2[0] - 1) % 5

        # Case 2: If two characters are on the same row, each of which is replaced to a
        # character in the left cell. If a character is located at the leftmost, a character in the
        # rightmost cell should be taken.
        elif crd1[0] == crd2[0] and lt1 + lt2 != 'XX':
            crd1[1] = (crd1[1] - 1) % 5
            crd2[1] = (crd2[1] - 1) % 5

        # Case 3: “xx” will not be decrypted. It will be just “xx”.
        elif lt1 + lt2 == 'XX':
            outputString += 'XX'
            break

        # Case 4: Otherwise, two characters are replaced by the others on the other vertices,
        # e.g., List indices of two characters are (0, 4) and (3,1), then each of which is replaced
        # to a character in the (0,1) and (3,4), respectively.
        else:
            tmp = crd2[0]
            crd2[0] = crd1[0]
            crd1[0] = tmp

        # go back from coordinates to key position
        pos1 = crd1[0] + 5 * crd1[1]
        pos2 = crd2[0] + 5 * crd2[1]

        # pull the new letter
        lt1 = K[pos1]
        lt2 = K[pos2]

        # build the output
        outputString += lt1
        outputString += lt2

    return outputString


def returnListOfTwoCharacters(P):
    PL = []
    for i in range(0, len(P), 2):
        PL.append(P[i:i + 2])
    return PL


# Test Part
while (1):
    choice = int(input("\nPlayfair cipher \n 1.Encryption \n 2.Decryption: \n 3.EXIT\nType your choice: "))
    if choice == 1:
        key = (input('Enter the key: ') + 'abcdefghijklmnopqrstuvwxyz').upper()
        KM = Key(key)
        P = (input('Enter the plain text: ')).upper()
        PL = Pre(P)
        print('\nStep 1: Construct key matrix')
        Display_5x5_KeyMatrix(KM)
        enc = Enc(KM, PL)
        print('Step 2: Preprocessing (break plain text to make two characters blocks)')
        print('Preprocessing: ', end=' ')
        break_plain_text_to_02_char_blocks(PL)
        print('\nStep 3: Encryption')
        print('Encrypted text: ', returnListOfTwoCharacters(enc))

    elif choice == 2:
        key = (input('Enter the key: ') + 'abcdefghijklmnopqrstuvwxyz').upper()
        K = Key(key)
        P = (input('Enter the cipher text: ')).upper()
        CL = Pre(P)
        print('\nStep 1: Construct key matrix')
        Display_5x5_KeyMatrix(K)
        dec = Dec(K, CL)
        print('Step 2: Preprocessing (break cipher text to make two characters blocks)')
        print('Preprocessing: ', end=' ')
        break_plain_text_to_02_char_blocks(CL)
        print('\nStep 3: Decryption')
        print('Decrypted text: ', returnListOfTwoCharacters(dec))

    elif choice == 3:
        exit()
    else:
        print("Incorrect choice! Choose the correct option:")
