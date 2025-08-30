import re
import nltk
from nltk import word_tokenize, pos_tag

# nltk.download("averaged_perceptron_tagger")

def tokenize(sentence):
    return re.findall(r'\b\w+\b', sentence.lower())

def has_article_before_noun(sentence):
    tokens = tokenize(sentence)
    tags = pos_tag(tokens)
    for i, (word, tag) in enumerate(tags):
        if tag in ['NN', 'NNS']:
            if i == 0 or tags[i-1][0].lower() not in ['the', 'a', 'an', 'this', 'that', 'these', 'those']:
                return True
            return False
    return True  # No noun found, so rule not violated


if __name__ == "__main__":

    test_sentences = [
        "The cat sat on the mat.",
        "A dog barked loudly.",
        "This is a test sentence.",
        "Cat sat on the mat.",
        "Dog barked loudly.",
        "Is this a test sentence?"
    ]

    for sentence in test_sentences:
        print(f"Testing: {sentence}")
        if has_article_before_noun(sentence):
            print(" - Rule violated: Missing article before noun")
        else:
            print(" - Rule passed")