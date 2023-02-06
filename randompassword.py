import secrets
import codecs
import math

#number of Words in password
numWords = 3
#which languages should be included in the password
english = True
german = False
#digit and specialChar of your preference
numberChar = "1"
specialChar = "!"

#Website Requirements
#This list of specials is not for security, security is provided by the words alone, it is to please password requirements of websites
specials = "!@#$%^&*()-+?_=,<>/" #should be accepted by every website

#testcases = [["te˝st\n","te˝st\n","te˝st\n","te˝st\n"],["test","test","test","test","test","test","test"],["T","T","T","T"],["1","1","1","1"]]

def listIsSet(list):
        return len(set(list)) == len(list)

#outputs the length of random generated password with 52 english alphabet letters and 33 special characters corresponding to amount of combinations
def combinationsToLenRand(num):
        return round(math.log(num,85),1)
        

def verifyWordlist(list, strPath):
        if not listIsSet(list):
                print("duplicate words found, check wordlist quality of: " + strPath)
        else:
                print("no duplicates found, wordlist:"+strPath+" is OK")


class lang:

        def __init__(self, wordlistPath, top10kPath, encoding):
                f = codecs.open(wordlistPath, 'r', encoding)
                f10k = codecs.open(top10kPath, 'r', encoding)
                self.wordList = [line.strip() for line in f.readlines()]
                self.top10k = [line.strip() for line in f10k.readlines()]
                self.numWords = len(self.wordList)
                verifyWordlist(self.wordList, wordlistPath)
                verifyWordlist(self.top10k, top10kPath)

        def randomWords(self, wordcount):
                words = []
                for i in range(0, wordcount):
                        word = secrets.choice(self.wordList)
                        words.append(word)
                return words

        def isTop10k(self, strWord):
                return strWord in self.top10k

#paths
en = lang("words.txt", "top10keng.txt", "utf-8")
de = lang("wortliste.txt", "top10kde.txt", "utf-8")
langs = []
if english:
        langs.append(en)
if german:
        langs.append(de)

#closeOnEnter
close = False

#Calculation of password strength for the selected parameters
sumWordsOfLangs = 0
for lang in langs:
        sumWordsOfLangs = sumWordsOfLangs + lang.numWords

numCombinations = math.pow(sumWordsOfLangs, numWords)

print("\nApproximate Strength with selected Parameters:\n" + str(round(math.log(numCombinations, 2),1))+"bits " +str(combinationsToLenRand(numCombinations)) +" random chars*.")

numCombinationsSpecials = numCombinations * 9 *len(specials)
print("\nApproximate Strength for random special version:\n" + str(round(math.log(numCombinationsSpecials, 2),1))+"bits " +str(combinationsToLenRand(numCombinationsSpecials)) +" random chars*.")
print("random chars*: Corresponding to a pseudorandom password with upper and lowercase letters of the english alphabet and the OWASP recommended 33 special symbols")	
#in case all words are of a top10k wordlist, this will get checked for each password
numCombinations10k = math.pow(10000*len(langs), numWords)
numBits10k = round(math.log(numCombinations10k, 2), 1)



def listToString(words, linebreak):
        word = words[0]
        spacer = ""
        if linebreak:
                spacer = "\n"

        for i in range(1,len(words)):
                word = word + spacer + words[i]
        return word
        

def formatWithSpecials(shuffledWords, random):
        hasUpper = False
        hasNumber = False
        hasSpecial = False
        hasLower = False
        wrd = listToString(shuffledWords, False)
        for c in wrd:
                if(c.isupper()):
                        hasUpper=True
                if(c.isdigit()):
                        hasNumber=True
                if not c.isalnum():
                        hasSpecial = True
                if(c.islower()):
                        hasLower = True

        #convert first lowercase letter to uppercase, in almost all cases this will be the first char
        for i in range(0, len(wrd)):
                if wrd[i].isalpha():#and wrd[i].islower:
                        wrdlist = list(wrd)
                        wrdlist[i] = wrdlist[i].upper()
                        wrd = ''.join(wrdlist)
                        hasUpper = True
                        break;

        #append random number and special char to the end
        if random:
                if not hasNumber:
                        wrd = wrd + str(secrets.randbelow(10))
                if not hasSpecial:
                        wrd = wrd + secrets.choice(list(specials))
        # always append the user-chosen values for ease of remembering
        else:
                wrd = wrd + numberChar + specialChar;
        
        if not hasUpper or not hasLower:
                print("Generated password has no upper-case or lower-case character. This can only happen if a password was generated with either no upper or no lowercase letters, which theoretically can happen but the chances are quite low (with default wordlists and non-zero amount of words).")

        return wrd

while True:

        allWords = []

        #choose numWords words at random from each language
        for lang in langs:
                randWords = lang.randomWords(numWords)
                for word in randWords:
                        allWords.append((word, lang))

        words = []
        #pick numWords words from all the randomly selected words, this is the easiest way I could come up with to pick a random number of words from each language save for combining all word lists into a single one
        for i in range(0, numWords):
                choice = secrets.choice(allWords)
                allWords.remove(choice)
                words.append(choice)
        # check if all random words are part of a top10k list
        allTop10 = True
        
        for wordLangPair in words:
                if not wordLangPair[1].isTop10k(wordLangPair[0]):
                        allTop10 = False

        #get rid of the lang
        words = next(zip(*words))

        if allTop10:
                print("WARNING: all words are part of a top10k words list, this could reduce the strength of the password to approximately: " + str(numBits10k)+"bits, " + str(combinationsToLenRand(numCombinations10k)) + " random chars" )

        print("\nRandom Words:")
        print(listToString(words, True))
        print()

        print("Formatted:")
        pwstr = listToString(words, False)
        #recalculate password strength (if the password ends up short enough, it will be easier to brute-force than to dictionary attack it, this is extremely unlikely with the default wordlists as it requires that the generated password is shorter than 3 letters)
        #assuming english alphabet: TODO analyze alphabet of generated password?
        numCombinationsBF = math.pow(52, len(pwstr))
        numBitsBF = round(math.log(numCombinationsBF, 2), 1)
        if numCombinationsBF < numCombinations:
        	print("WARNING: password is too short and vulnerable to brute-force attacks, actual strength of the password: " + str(numBitsBF)+"bits, " + str(combinationsToLenRand(numCombinationsBF)) + " random chars")
        print(pwstr)
        print()

        


        print("Formatted with Specials:")
        print(formatWithSpecials(words, False))
        print()

        print("Formatted with random specials:")
        print(formatWithSpecials(words, True))
        print()

        msg = "Press Enter to re-run"
        if close:
                msg = "Press Enter to exit"

        keypress = input(msg)
        if keypress == "" and close:
                break




