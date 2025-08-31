# Technical Writing Rule Checker

A Python-based module for automatically detecting and correcting violations of technical writing standards. This tool processes text and ensures adherence to five essential rules for clear, professional technical documentation.

## Overview

The Technical Writing Rule Checker analyzes text against established technical writing guidelines and provides corrected versions of non-compliant sentences. It uses Natural Language Processing (NLP) to understand sentence structure and applies specific corrections based on predefined rules.

## Supported Rules

1. **Articles and Demonstratives**: Ensures proper use of articles (the, a, an) or demonstrative adjectives (this, these, that, those) before nouns or noun clusters
2. **Active Voice**: Converts passive voice constructions to active voice in procedural writing
3. **Single Instruction**: Ensures only one instruction per sentence, splitting compound instructions as needed
4. **Imperative Form**: Converts sentences to command form for instructional content
5. **Sentence Length**: Enforces maximum 20-word limit per sentence, suggesting splits for longer sentences

## Code Architecture

### Core Modules

#### TechnicalWritingChecker Class
The main processing engine that contains all rule-checking logic.

**Key Methods:**
- `check_all_rules(sentence)` - Orchestrates all rule checks for a single sentence
- `process_text(text)` - Processes complete text input and returns violations
- `check_rule1_articles(sentence)` - Validates article and demonstrative usage
- `check_rule2_active_voice(sentence)` - Detects and converts passive voice
- `check_rule3_single_instruction(sentence)` - Ensures single instruction per sentence
- `check_rule4_imperative(sentence)` - Converts to imperative form
- `check_rule5_sentence_length(sentence)` - Validates sentence length constraints

#### RuleViolation Dataclass
Stores information about detected violations and their corrections.

**Attributes:**
- `rule_number` - Numeric identifier of the violated rule
- `rule_name` - Human-readable name of the rule
- `original_sentence` - The input sentence with violations
- `corrected_sentence` - The corrected version
- `explanation` - Description of what was changed

#### Utility Functions
- `display_results(violations)` - Formats and displays violation reports
- `_get_imperative_verb(verb)` - Converts verbs to imperative form
- `main()` - Entry point handling command-line arguments and execution modes

### NLP Dependencies

The module uses spaCy for natural language processing tasks:
- **Part-of-speech tagging (POS Tagging)** - Identifies nouns, verbs, and other grammatical components
- **Dependency parsing** - Understands grammatical relationships between words
- **Sentence tokenization** - Properly segments text into individual sentences

## Installation

### Prerequisites

1. Install Python 3.7 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the spaCy English language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage Instructions

### Command Line Interface

The script supports multiple execution modes:

#### 1. Sample Data Mode (Default)
Runs the checker against built-in test cases to demonstrate functionality:
```bash
python rule_checker.py
```

#### 2. Interactive Mode
Allows real-time testing of individual sentences:
```bash
python rule_checker.py --interactive
```
or
```bash
python rule_checker.py -int
```

**Interactive Commands:**
- Enter any sentence to check for violations
- Type `quit`, `exit`, or `q` to terminate the session

#### 3. File Input Mode
Processes text from a specified file:
```bash
python rule_checker.py --input filename.txt
```
or
```bash
python rule_checker.py -i filename.txt
```

#### 4. Direct Text Input Mode
Processes text provided directly as a command-line argument:
```bash
python rule_checker.py --text "Your sentence to check goes here."
```
or
```bash
python rule_checker.py -t "Your sentence to check goes here."
```

### Usage Examples

#### Processing Sample Data
```bash
python rule_checker.py
```

Expected output format:
```
=== Technical Writing Rule Checker ===
Running with sample test cases...

1. Testing: Turn shaft assembly.
   Issues found: Added 'the' before 'shaft assembly'
   Corrected: Turn the shaft assembly.

2. Testing: Data module tells you how to operate unit.
   Issues found: Added 'This' before 'data module' and 'the' before 'unit'
   Corrected: This data module tells you how to operate the unit.
```



#### Interactive Session
```bash
python rule_checker.py --interactive
```

```
=== Technical Writing Rule Checker ===
Enter sentences to check (type 'quit' to exit):

> Turn valve clockwise.
No violations found

> Safety check can be performed.
Issues found: Converted to imperative form
Corrected: Perform the safety check.

> quit
```

#### File Processing
Create a text file (e.g., `technical_doc.txt`) with content:
```
Turn shaft assembly.
Data module tells you how to operate unit.
The test can be continued.
```
Or use the input.txt file which has some sample cases. 

Run the checker:
```bash
python rule_checker.py --input technical_doc.txt
```

## Error Handling

The module includes comprehensive error handling for:
- Missing spaCy language models with installation instructions
- File not found errors with clear error messages
- Malformed input text with graceful degradation
- Edge cases in rule application with fallback behaviors

## Extending the Module

### Adding New Rules
To add additional rules, implement a new method following the pattern:

```python
def check_rule6_new_rule(self, sentence: str) -> Tuple[bool, str, str]:
    """Rule 6: Description of the new rule"""
    # Implementation logic here
    return has_violation, corrected_sentence, explanation
```

Then add the new rule to the `check_all_rules()` method.

### Customizing Rule Logic
Individual rule methods can be modified to handle specific domain terminology or organizational style guidelines by updating the regex patterns and conversion logic.

## Testing

The module includes built-in test cases that demonstrate each rule's functionality. Run the default mode to see comprehensive examples of all rule applications.

## Limitations

- Requires spaCy English language model for NLP processing
- Rule detection is based on pattern matching and may not catch all edge cases
- Complex sentence structures may require manual review after automated correction
- Performance scales with text length and complexity of linguistic analysis required

## Technical Requirements

- Python 3.7+
- spaCy 3.0+ with English language model
- Sufficient memory for NLP model loading (approximately 50MB)
- Command-line interface support for interactive mode