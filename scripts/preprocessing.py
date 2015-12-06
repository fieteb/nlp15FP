import string;

# NB stop words start

excludedWords = set();
with open("../data/uninterestingWords.txt") as f :
    for line in f:
        excludedWords.add(line.strip());
punct = set(string.punctuation);
# NB stop words end




def nbPreprocess(tokenizedLine) :
    # check for excluded words
    tmp = ' '.join(w.lower() for w in tokenizedLine if w.lower() not in excludedWords).strip();
    # check for punctuation
    return ''.join(ch for ch in tmp if ch not in punct).split();
    