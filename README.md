# Document-Language-Similarity
A simple NLP algorithm implementation to determine the language of a document. Done for a project in CS2810 at Northeastern. 

Overview:
This program uses frequencies of trigrams to make a prediction of the language of a document. A trigram in this case is defined as a 
three character subsequence in a training document. This program only deals with ASCII characters. As such, there are only 27 allowed
characters, the lowercase letters and the space character. For example, the string "Hello World" is broken down into the following
trigrams. 

"Hel", "ell", "llo", "lo ", "o W", " Wo", "Wor", "orl", and "rld" 

Several documents of known languages are given to this program as input, and each document is scanned, recording the counts of all
trigrams in a vector containing all 27^3 possible trigrams. Once the training is complete, the models for each language are then
"normalized", converting them from vectors of counts to vectors of frequencies. Finally, the program constructs similar vectors for
each unknown document, recording the counts of each trigram. Once these vectors have been constructed, they are compared to each of
the vectors for the known languages using cosine similarity. The angle between any two vectors is calculated, and the cosine of this
angle is taken, resulting in a value from -1 to 1. The smaller the angle between the two vectors, the closer the cosine of the angle 
is to 1. Finally, all of these similarities are sorted in descending order and outputted to a text file, displaying the language and 
its similarity to the document. 

Command Line Arguments:
This program will take in input at the program level and give output at the program level (command line). So, when you the program
is run it would look like:

python main.py input.txt output.txt

Input:
The input to the program is a text file of filenames and their associated languages. It is assumed that these test files are stored
in the same directory as the main python file

French frenchtest1.txt
French frenchtest2.txt
Spanish spanishtest1.txt
Croatian croatiantest1.txt
English englishtest1.txt
Unknown unknowntext.txt
Unknown unknowntext2.txt

If a document's langugage is "Unknown" then it will be the document tested. More than one unknown document can be tested at a time. 

Output:

The output of your program will be a text file of filenames and their associated language. It will look something like the following

unknowntext
    French xx
    Spanish xx
    Croatian xx
    English xx
unknowntext2
    Croatian xx
    English xx
    French xx
    Spanish xx