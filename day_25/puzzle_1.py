import math
inputfile = open("./day_25/input.txt", "r")

'''
Dictionaries converting between decimal and SNAFU digits.
'''
SNAFUDigitsInDecimal = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
decimalDigitsInSNAFU = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}

'''
Function to convert a SNAFU number to decimal.
Removes the last digit, and adds it (multiplied by the appropriate power of 5) to the sum.
After going over every digit, return the sum.
'''
def SNAFUToDecimal(snafuNumber):
    decimal = 0
    for i in range(len(snafuNumber)):
        lastDigit = snafuNumber.pop()
        decimal += SNAFUDigitsInDecimal[lastDigit] * (5 ** i)
    return decimal

'''
Function to convert a decimal number to SNAFU.
For easier manipulation, we will use -1 and -2 instead of - and = for the most part, converting to the latter in the end.
We start off with an empty array.
We calculate the 5-based logarithm of the decimal number, and take the _ceil_ of that (usually when converting between bases, we take the floor of this logarithm, but because of our weirdly behaving digits, it is a possibility that the first digit represents a value bigger than our actual number, with the following digit representing a negative value).
We iterate over all powers of 5 starting from this logarithm and descending to 0 (inclusive). In each iteration, we do the following:
    1. Calculate the quotient of the decimal number and the power of 5.
    2. Check if the quotient is 0, 1, or 2.
        a) If this is the case, we just append the quotient to the array.
        b) If this is not the case, i.e. the quotient is 3 or 4, we increment the lastly added digit with 1, and then append -2 or -1, respectively.
    3. Subtract the quotient times the power of 5 from the decimal number.
After this, we still have a problem: if in 2/a) we incremented a value that's already maximal in this system (2), the digit and the one before that should change accordingly. For this, we iterate through all digits starting from the right (smallest values), and check if the digit is 3: if it is, we replace it with -2, and increment the digit just before (to the left of) that.
Now we just have to remove the possible, but not guaranteed leading 0, and finally we can convert the list to SNAFU digits using the decimalDigitsInSNAFU dictionary.
'''
def decimalToSNAFU(decimalNumber):
    SNAFUDecimalRepresentation = []
    maxPower = math.ceil(math.log(decimalNumber, 5))
    for i in range(maxPower, -1, -1):
        intDivided = decimalNumber // (5 ** i)
        if intDivided <= 2:
            SNAFUDecimalRepresentation.append(intDivided)
        else:
            SNAFUDecimalRepresentation[-1] += 1
            SNAFUDecimalRepresentation.append(-2 if intDivided == 3 else -1)
        decimalNumber -= intDivided * (5 ** i)
    for i in range(len(SNAFUDecimalRepresentation)-1, 0, -1):
        if SNAFUDecimalRepresentation[i] == 3:
            SNAFUDecimalRepresentation[i] = -2
            SNAFUDecimalRepresentation[i-1] += 1
    if SNAFUDecimalRepresentation[0] == 0:
        SNAFUDecimalRepresentation.pop(0)
    SNAFU = [decimalDigitsInSNAFU[digit] for digit in SNAFUDecimalRepresentation]
    return SNAFU

'''
Read the input into a list. Each element is also a list, representing a SNAFU number.
'''
numbers = []
for line in inputfile:
    numbers.append(list(line.strip()))

'''
We calculate the sum of the SNAFU numbers converted to decimal.
Then we finally print the sum, converted to SNAFU.
'''
sumOfNumbers = 0
for number in numbers:
    sumOfNumbers += SNAFUToDecimal(number)

print(''.join(decimalToSNAFU(sumOfNumbers)))

inputfile.close()