import sys
import string
import math
import collections


class NbClassifier(object):
    """
    BEFORE TUNING THE CLASSIFIER:

        train.txt: 0.993
        dev.txt: 0.966
        test.txt: 0.982
   
    AFTER TUNING THE CLASSIFIER:

        train.txt: .997
        dev.txt: 0.980
        test.txt: 0.984

    *accuracy improved further after improving pre-processing*
    """
    """
    A Naive Bayes classifier object has three parameters, all of which are populated during initialization:
    - a set of all possible attribute types
    - a dictionary of the probabilities P(Y), labels as keys and probabilities as values
    - a dictionary of the probabilities P(F|Y), with (feature, label) pairs as keys and probabilities as values
    """
    
    def __init__(self, training_filename, stopword_file):
        self.attribute_types = set()
        self.label_prior = {}    
        self.word_given_label = {}   
        self.collect_attribute_types(training_filename)
        if stopword_file is not None:
            self.remove_stopwords(stopword_file)
        self.train(training_filename)

    """

    A helper function to transform a string into a list of word strings.
    You should not need to modify this unless you want to improve your classifier in the extra credit portion.
    """

    def extract_words(self, text):
        
        
        #punc = ["%", "*", "+", "@", "{", "}", "|", "~" ] # changes the punctuation to be removed
        no_punct_text = "".join([x for x in text.lower() if not x in string.punctuation])
        return [word for word in no_punct_text.split()]

    """
    Given a stopword_file, read in all stop words and remove them from self.attribute_types
    Implement this for extra credit.
    """

    def remove_stopwords(self, stopword_file):
        with open(stopword_file, 'r') as f:
            sw = self.extract_words(f.read())

        stop = set(sw)
        self.attribute_types = (self.attribute_types - stop)
        f.close()

    """

    Given a training datafile, add all features that appear at least m times to self.attribute_types
    """

    def collect_attribute_types(self, training_filename, m=1):

        longstr = ""
        with open(training_filename, 'r') as f:
            longstr = self.extract_words(f.read())

        wordcounter = collections.Counter(longstr)
        for word in longstr:
            if not word == "spam" and not word == "ham":
                if wordcounter[word] >= m:
                    #if not word == "spam" or not word == "ham":
                    self.attribute_types.add(word)
                    #elif wordcounter[word] >= m+1:
                        #self.attribute_types.add(word)

        f.close()
        print(len(self.attribute_types))
      
    """
    Given a training datafile, estimate the model probability parameters P(Y) and P(F|Y).
    Estimates should be smoothed using the smoothing parameter k.
    """

    def train(self, training_filename, k=1):

        self.label_prior = {}
        self.word_given_label = {}
        cardinality = len(self.attribute_types)
        totalwords = totalmsg = spamwords = spammsg = hamwords = hammsg = 0.0

        for word in self.attribute_types:
            self.word_given_label[word, "ham"] = 0.0
            self.word_given_label[word, "spam"] = 0.0
        
        with open(training_filename, 'r') as f:
            for line in f.readlines():
                words = self.extract_words(line)                
                label = words[0]
                words.remove(label)
                totalwords += len(words)
                totalmsg += 1
                
                if label == "ham":
                    hammsg += 1
                    hamwords += len(words)
                elif label == "spam":
                    spammsg += 1
                    spamwords += len(words)
                    
                for word in words:
                    if word in self.attribute_types:
                        self.word_given_label[word, label] += 1
                                   
        self.label_prior["ham"] = hammsg/totalmsg
        self.label_prior["spam"] = spammsg/totalmsg
         
        
        for j,v in self.word_given_label.items():
            count = v
            label = j[1]               
            if label == "spam":
                self.word_given_label[j] = (count + k)/(spamwords + k*cardinality)
            elif label == "ham":
                self.word_given_label[j] = (count + k)/(hamwords + k*cardinality)
         
        for j,v in self.word_given_label.items():
            if v <= 0.0001:
                print("less")
                
            
        f.close()

    """
    Given a piece of text, return a relative belief distribution over all possible labels.
    The return value should be a dictionary with labels as keys and relative beliefs as values.
    The probabilities need not be normalized and may be expressed as log probabilities. 
    """

    def predict(self, text):

        beliefs = {}
        spamp = math.log(self.label_prior["spam"])
        hamp = math.log(self.label_prior["ham"])
    
        for word in text:
            if (word, "ham") in self.word_given_label.keys():
                hamp += math.log(self.word_given_label[(word, "ham")])

            if (word, "spam") in self.word_given_label.keys():
                spamp += math.log(self.word_given_label[(word, "spam")])

        beliefs["ham"] = hamp
        beliefs["spam"] = spamp

        return beliefs

    """
    Given a datafile, classify all lines using predict() and return the accuracy as the fraction classified correctly.
    """

    def evaluate(self, test_filename):
        correct = total = 0.0

        with open(test_filename, 'r') as f:
            for l in f.readlines():
                line = self.extract_words(l)
                label = line[0]
                line.remove(label)
                p = self.predict(line)
                #p = self.predict('BIG BROTHER ALERT! The computer has selected u for 10k cash or #150 voucher. Call 09064018838. NNT PO Box CRO1327 18+ BT Landline Cost 150ppm mobiles vary')
                #print(p)
                predicted = max(p.keys(), key=(lambda k: p[k]))
                if predicted == label:
                    correct += 1
                total += 1
                
        f.close()
        return (correct/total)


if __name__ == "__main__":

    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("\nusage: ./hmm.py [training data file] [test or dev data file] [(optional) stopword file]")
        exit(0)

    elif len(sys.argv) == 3:
        classifier = NbClassifier(sys.argv[1], None)

    else:
        #sys.argv[3]
        classifier = NbClassifier(sys.argv[1], sys.argv[3])
    print(classifier.evaluate(sys.argv[2]))