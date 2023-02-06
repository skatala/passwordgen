# passwordgen
Python script to randomly generate a secure and memorable passphrase.
The script calculates the strength of the password based on the wordlists, and if the generated password is too short, or the words all happen to be in the top 10k most frequent words of each language will issue a warning.
Toggle the length and which languages you want in your password at this point in passwordgen.py:

```
#number of Words in password
numWords = 2
#which languages should be included in the password
english = True
german = False
```

## Usage
Install python and run the passwordgen.py

## Security Recommendations

Length: For websites 3 words will be enough (equivalent to 8-9 completely random characters assuming 52 letters + 33 special symbols).
For anything that does not rate-limit guesses or that allows for offline attacks like your home wifi-key use as many words as possible.
For my password manager password I use 7 words.

Add as many languages as you speak, this will probably make the password more memorable to you as well as increase security, although if you have an easier time remembering words of just one language just stick to one. 


## Adding Languages

Modify this part of the code. 
The expected format of the wordlists are a text file where each line is a word.
I recommend adding a wordlist that contains at least 100k words and a wordlist that contains the most frequent words of the same language.
If you cannot find the latter, just add an empty text file although this will disable verification of the password.

```
#paths
en = lang("words.txt", "top10keng.txt", "utf-8")
de = lang("wortliste.txt", "top10kde.txt", "utf-8")
yourLanguage = lang("example.txt", "exampleTop10000words.txt" , "encoding")
langs = [yourLanguage]
if english:
        langs.append(en)
if german:
        langs.append(de)

```

## Sources
I do not own any of the wordlists, refer to the original sources here

worliste.txt taken from https://github.com/davidak/wortliste  
words.txt taken from https://github.com/dwyl/english-words  
top10keng.txt taken from https://github.com/first20hours/google-10000-english (google-10000-english.txt)  
top10kde.txt taken from https://github.com/signalwerk/pwd/tree/master/wordlists  

