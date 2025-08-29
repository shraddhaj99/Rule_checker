import re
import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

class RuleChecker:
    def __init__(self, autocorrect: bool = False):
        self.autocorrect = autocorrect

    def check_text(self, text: str) -> Dict:
        doc = nlp(text)
        results = []

        for idx, sent in enumerate(doc.sents, start=1):
            sentence_text = sent.text.strip()
            issues = []
            corrected = sentence_text

            # Rule 1: Articles before nouns
            if re.match(r"^[A-Z][a-z]+ [a-z]+", sentence_text):  # naive
                issues.append("Missing article before noun")

            # Rule 2: Passive voice detection
            if any(tok.dep_ == "auxpass" for tok in sent):
                issues.append("Sentence is in passive voice")

            # Rule 3: Multiple instructions (check for multiple verbs joined by 'and')
            verbs = [tok for tok in sent if tok.pos_ == "VERB"]
            if "and" in sentence_text and len(verbs) > 1:
                issues.append("Multiple instructions in one sentence")

            # Rule 4: Imperative form (should start with VERB)
            first_token = sent[0]
            if first_token.pos_ != "VERB":
                issues.append("Not in imperative form")

            # Rule 5: Max sentence length
            if len(sent) > 20:
                issues.append("Sentence too long (>20 words)")

            results.append({
                "sentence_number": idx,
                "original": sentence_text,
                "issues": issues,
                "corrected": corrected if self.autocorrect else None
            })

        return {"violations": results}
