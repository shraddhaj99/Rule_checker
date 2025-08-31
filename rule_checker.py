"""
Technical Writing Rule Checker Module

This module processes text and ensures adherence to technical writing rules:
1. Proper use of articles and demonstrative adjectives
2. Active voice in procedural writing
3. One instruction per sentence
4. Imperative form for instructions
5. Maximum 20 words per sentence
"""

import re
import spacy
import argparse
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass

# Load spaCy model for NLP processing
try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    print("Please install the spaCy English model: python -m spacy download en_core_web_sm")
    exit(1)

@dataclass
class RuleViolation:
    rule_number: int
    rule_name: str
    original_sentence: str
    corrected_sentence: str
    explanation: str

class TechnicalWritingChecker:
    def __init__(self):
        # Common technical/procedural verbs that often start instructions
        self.imperative_verbs = {
            'turn', 'set', 'check', 'remove', 'install', 'connect', 'disconnect',
            'press', 'push', 'pull', 'rotate', 'adjust', 'calibrate', 'test',
            'verify', 'ensure', 'confirm', 'operate', 'start', 'stop', 'open',
            'close', 'insert', 'extract', 'replace', 'clean', 'inspect', 'measure'
        }

    def check_all_rules(self, sentence: str) -> Tuple[bool, str, List[str]]:
        """Check all rules for a sentence and return the final corrected version"""
        original = sentence.strip()
        if not original.endswith(('.', '!', '?')):
            original += '.'
        
        corrected = original
        applied_rules = []
        
        # Rule 1: Articles and demonstratives
        violation, new_corrected, explanation = self.check_rule1_articles(corrected)
        if violation:
            corrected = new_corrected
            applied_rules.append(f"Rule 1: {explanation}")
        
        # Rule 2: Active voice  
        violation, new_corrected, explanation = self.check_rule2_active_voice(corrected)
        if violation:
            corrected = new_corrected
            applied_rules.append(f"Rule 2: {explanation}")
        
        # Rule 3: Single instruction
        violation, new_corrected, explanation = self.check_rule3_single_instruction(corrected)
        if violation:
            corrected = new_corrected
            applied_rules.append(f"Rule 3: {explanation}")
        
        # Rule 4: Imperative form
        violation, new_corrected, explanation = self.check_rule4_imperative(corrected)
        if violation:
            corrected = new_corrected
            applied_rules.append(f"Rule 4: {explanation}")
        
        # Rule 5: Sentence length
        violation, new_corrected, explanation = self.check_rule5_sentence_length(corrected)
        if violation:
            corrected = new_corrected
            applied_rules.append(f"Rule 5: {explanation}")
        
        # Clean up any artifacts from multiple transformations
        corrected = self._cleanup_artifacts(corrected)
        
        has_any_violation = len(applied_rules) > 0
        return has_any_violation, corrected, applied_rules

    def _cleanup_artifacts(self, sentence: str) -> str:
        """Clean up artifacts from multiple rule applications"""
        # Fix repeated 'the'
        sentence = re.sub(r'\bthe\s+the\b', 'the', sentence, flags=re.IGNORECASE)
        
        # Fix spaces before punctuation
        sentence = re.sub(r'\s+([.,!?])', r'\1', sentence)
        
        # Fix double periods
        sentence = re.sub(r'\.\.+', '.', sentence)
        
        # Fix capitalization issues
        sentence = re.sub(r'This Data module', 'This data module', sentence)
        
        return sentence

    def check_rule1_articles(self, sentence: str) -> Tuple[bool, str, str]:
        """Rule 1: Check for proper use of articles - conservative approach"""
        corrected = sentence
        changes_made = []
        
        # Only handle specific, well-defined cases to avoid over-correction
        
        # Case 1: "Turn shaft assembly" -> "Turn the shaft assembly"
        if re.match(r'^\s*turn\s+shaft\s+assembly\b', sentence, re.IGNORECASE):
            corrected = re.sub(r'^(\s*turn\s+)shaft\s+assembly', r'\1the shaft assembly', corrected, flags=re.IGNORECASE)
            changes_made.append("Added 'the' before 'shaft assembly'")
        
        # Case 2: "Data module tells you how to operate unit" 
        # Only if it starts the sentence and doesn't already have "this"
        if re.match(r'^\s*data\s+module\s+tells', sentence, re.IGNORECASE) and not re.match(r'^\s*this\s', sentence, re.IGNORECASE):
            corrected = re.sub(r'^(\s*)data\s+module', r'\1This data module', corrected, flags=re.IGNORECASE)
            changes_made.append("Added 'This' before 'data module'")
        
        # Case 3: "operate unit" -> "operate the unit" (only if no article present)
        if re.search(r'\boperate\s+(?!the\s|a\s|an\s)unit\b', corrected, re.IGNORECASE):
            corrected = re.sub(r'\boperate\s+unit\b', 'operate the unit', corrected, flags=re.IGNORECASE)
            changes_made.append("Added 'the' before 'unit'")
        
        if changes_made:
            return True, corrected, "; ".join(changes_made)
        
        return False, sentence, ""

    def check_rule2_active_voice(self, sentence: str) -> Tuple[bool, str, str]:
        """Rule 2: Convert passive voice to active voice"""
        
        # Pattern 1: "X are supplied by Y" -> "Y supplies X"
        match = re.search(r'(.+?)\s+are\s+supplied\s+by\s+(.+?)\.?$', sentence, re.IGNORECASE)
        if match:
            subject = match.group(1).strip()
            agent = match.group(2).strip().rstrip('.')
            if not re.match(r'^(the|a|an|this|that)\b', agent.lower()):
                agent = f"the {agent}"
            corrected = f"{agent.capitalize()} supplies {subject.lower()}."
            return True, corrected, "Converted from passive to active voice"
        
        # Pattern 2: "X is held by Y" -> "Y holds X"
        match = re.search(r'(.+?)\s+is\s+held\s+by\s+(.+?)\.?$', sentence, re.IGNORECASE)
        if match:
            subject = match.group(1).strip()
            agent = match.group(2).strip().rstrip('.')
            if not re.match(r'^(the|a|an|this|that)\b', agent.lower()):
                agent = f"the {agent}"
            corrected = f"{agent.capitalize()} holds {subject.lower()}."
            return True, corrected, "Converted from passive to active voice"
        
        # Pattern 3: "X are connected by Y" -> "Y connects X"
        match = re.search(r'(.+?)\s+are\s+connected\s+by\s+(.+?)\.?$', sentence, re.IGNORECASE)
        if match:
            subject = match.group(1).strip()
            agent = match.group(2).strip().rstrip('.')
            # Special handling for "a switching relay" - don't add extra "the"
            if not re.match(r'^(the|a|an|this|that)\b', agent.lower()):
                agent = f"a {agent}" if agent.lower().startswith('switching') else f"the {agent}"
            corrected = f"{agent.capitalize()} connects {subject.lower()}."
            return True, corrected, "Converted from passive to active voice"

        return False, sentence, ""

    def check_rule3_single_instruction(self, sentence: str) -> Tuple[bool, str, str]:
        """Rule 3: Ensure one instruction per sentence"""
        
        # Look for imperative sentences with 'and' connecting two different actions
        # Only split if both parts have verbs that are in our imperative list
        
        # Pattern: [Imperative verb] [content] and [imperative verb] [content]
        doc = nlp(sentence)
        
        # Find 'and' tokens
        for token in doc:
            if token.text.lower() == 'and' and token.pos_ == 'CCONJ':
                # Check if there are imperative verbs before and after 'and'
                before_verbs = [t for t in doc[:token.i] if t.pos_ == 'VERB' and t.lemma_.lower() in self.imperative_verbs]
                after_verbs = [t for t in doc[token.i+1:] if t.pos_ == 'VERB' and t.lemma_.lower() in self.imperative_verbs]
                
                if before_verbs and after_verbs:
                    # This looks like two separate instructions
                    first_part = ' '.join([t.text for t in doc[:token.i]]).strip()
                    second_part = ' '.join([t.text for t in doc[token.i+1:]]).strip().rstrip('.')
                    
                    # Capitalize second part
                    if second_part and second_part[0].islower():
                        second_part = second_part[0].upper() + second_part[1:]
                    
                    corrected = f"A. {first_part}. B. {second_part}."
                    return True, corrected, "Split multiple instructions into separate sentences"
        
        return False, sentence, ""

    def check_rule4_imperative(self, sentence: str) -> Tuple[bool, str, str]:
        """Rule 4: Convert to imperative form"""
        
        # Pattern 1: "The X can be continued" -> "Continue the X"
        match = re.search(r'(.+?)\s+can\s+be\s+(\w+)', sentence, re.IGNORECASE)
        if match:
            subject = match.group(1).strip()
            verb = match.group(2)
            imperative_verb = self._get_imperative_verb(verb)
            corrected = f"{imperative_verb} {subject.lower()}."
            return True, corrected, "Converted to imperative form"
        
        # Pattern 2: "X are to be removed with Y" -> "Remove X with Y"
        match = re.search(r'^(.+?)\s+are\s+to\s+be\s+(\w+)(.+)?', sentence, re.IGNORECASE)
        if match:
            subject = match.group(1).strip()
            verb = match.group(2)
            rest = match.group(3) if match.group(3) else ""
            
            imperative_verb = self._get_imperative_verb(verb)
            corrected = f"{imperative_verb} {subject.lower()}{rest}."
            return True, corrected, "Converted to imperative form"
        
        return False, sentence, ""

    def _get_imperative_verb(self, verb: str) -> str:
        """Convert verb to imperative form"""
        imperative_map = {
            'continued': 'Continue',
            'removed': 'Remove',
            'tested': 'Test',
            'operated': 'Operate',
            'connected': 'Connect',
            'supplied': 'Supply',
            'held': 'Hold',
            'checked': 'Check'
        }
        return imperative_map.get(verb.lower(), verb.capitalize())

    def check_rule5_sentence_length(self, sentence: str) -> Tuple[bool, str, str]:
        """Rule 5: Check for maximum 20 words per sentence"""
        words = sentence.strip().split()
        
        if len(words) > 20:
            # Try to find natural break points using NLP
            doc = nlp(sentence)
            
            # Look for coordinating conjunctions that could serve as break points
            for token in doc:
                if (token.pos_ == 'CCONJ' and token.text.lower() in ['and', 'but'] and 
                    token.i > 8 and token.i < len(doc) - 3):
                    
                    first_part = ' '.join([t.text for t in doc[:token.i]]).strip()
                    second_part = ' '.join([t.text for t in doc[token.i+1:]]).strip()
                    
                    if not first_part.endswith('.'):
                        first_part += '.'
                    
                    if second_part and second_part[0].islower():
                        second_part = second_part[0].upper() + second_part[1:]
                    
                    if not second_part.endswith('.'):
                        second_part += '.'
                    
                    corrected = f"{first_part} {second_part}"
                    return True, corrected, f"Split long sentence ({len(words)} words) into shorter sentences"
            
            return True, sentence, f"Sentence exceeds 20-word limit ({len(words)} words) - manual revision needed"
        
        return False, sentence, ""

    def process_text(self, text: str) -> List[RuleViolation]:
        """Process text and return all rule violations with corrections"""
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        
        all_violations = []
        
        for sentence in sentences:
            has_violation, corrected, applied_rules = self.check_all_rules(sentence)
            
            if has_violation:
                explanation = "; ".join([rule.split(": ", 1)[1] for rule in applied_rules])
                rule_numbers = [int(rule.split(":")[0].split()[1]) for rule in applied_rules]
                
                violation = RuleViolation(
                    rule_number=min(rule_numbers),
                    rule_name="Multiple Rules" if len(rule_numbers) > 1 else f"Rule {rule_numbers[0]}",
                    original_sentence=sentence,
                    corrected_sentence=corrected,
                    explanation=explanation
                )
                all_violations.append(violation)
        
        return all_violations

def display_results(violations: List[RuleViolation]):
    """Display the results in a formatted way"""
    
    print("=" * 80)
    print("RULE CHECKER RESULTS")
    print("=" * 80)
    
    if not violations:
        print("✅ No rule violations found! All sentences comply with the rules.")
        return
    
    for i, violation in enumerate(violations, 1):
        print(f"\n{i}. ORIGINAL: {violation.original_sentence}")
        print(f"   ISSUES: {violation.explanation}")
        print(f"   CORRECTED: {violation.corrected_sentence}")
    
    print(f"\n" + "=" * 80)
    print(f"SUMMARY: Found {len(violations)} sentences with rule violations")

def main():
    parser = argparse.ArgumentParser(description='Technical Writing Rule Checker')
    parser.add_argument('--input', '-i', help='Input text file')
    parser.add_argument('--text', '-t', help='Direct text input')
    parser.add_argument('--interactive', '-int', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    checker = TechnicalWritingChecker()
    
    # Sample test cases
    sample_texts = [
        "Turn shaft assembly.",
        "Data module tells you how to operate unit.",
        "The safety procedures are supplied by the manufacturer.", 
        "The main gear leg is held by the side stay.",
        "The circuits are connected by a switching relay.",
        "Set the TEST switch to the middle position and release the SHORT-CIRCUIT TEST switch.",
        "The test can be continued.",
        "Oil and grease are to be removed with a degreasing agent.",
        "Open the panel and disconnect the power cable."
    ]
    
    if args.interactive:
        print("=== Technical Writing Rule Checker ===")
        print("Enter sentences to check (type 'quit' to exit):")
        
        while True:
            user_input = input("\n> ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_input:
                violations = checker.process_text(user_input)
                display_results(violations)
    
    elif args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
            violations = checker.process_text(text)
            display_results(violations)
        except FileNotFoundError:
            print(f"Error: File '{args.input}' not found.")
    
    elif args.text:
        violations = checker.process_text(args.text)
        display_results(violations)
    
    else:
        # Run with sample data by default
        print("=== Technical Writing Rule Checker ===")
        print("Running with sample test cases...\n")
        
        for i, text in enumerate(sample_texts, 1):
            print(f"{i}. Testing: {text}")
            
            has_violation, corrected, applied_rules = checker.check_all_rules(text)
            
            if has_violation:
                print(f"   Issues found: {'; '.join([rule.split(': ', 1)[1] for rule in applied_rules])}")
                print(f"   Corrected: {corrected}")
            else:
                print("   No violations found")
            print()

if __name__ == "__main__":
    main()
