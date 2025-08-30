import re
import nltk
from nltk import word_tokenize, pos_tag

# nltk.download("averaged_perceptron_tagger")

# --- Article before nouns -------------------------------------
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

# --- Active voice only ---------------------------------------

def is_active_voice(sentence):
    # Passive voice often uses "is/are/was/were ... by"
    passive_pattern = re.compile(r'\b(is|are|was|were|be|been|being)\b\s+\w+\b\s+by\b', re.IGNORECASE)
    return not passive_pattern.search(sentence)

if __name__ == "__main__":

    test_sentences = [
        "The cat sat on the mat.",
        "A dog barked loudly.",
        "This is a test sentence.",
        "Cat sat on the mat.",
        "Dog barked loudly.",
        "Is this a test sentence?"
    ]

    # Active voice examples
    active_sentences = [
        "The engineer fixed the machine.",
        "She writes the report every week.",
        "They will deliver the package tomorrow.",
        "John painted the fence.",
        "The chef cooked a delicious meal."
    ]

    # Passive voice examples
    passive_sentences = [
        "The machine was fixed by the engineer.",
        "The report is written by her every week.",
        "The package will be delivered tomorrow.",
        "The fence was painted by John.",
        "A delicious meal was cooked by the chef."
    ]

    # for sentence in test_sentences:
    #     print(f"Testing: {sentence}")
    #     if has_article_before_noun(sentence):
    #         print(" - Rule violated: Missing article before noun")
    #     else:
    #         print(" - Rule passed")

    for sentence in active_sentences+passive_sentences:
        print(f"Testing: {sentence}")
        if is_active_voice(sentence):
            print(" - Rule passed")
        else:
            print(" - Rule violated: Passive voice detected")