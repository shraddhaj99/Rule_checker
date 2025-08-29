# 📘 Rule Checker Module

A Rule Checker Module that processes a given piece of text and ensures it adheres to a set of predefined rules for procedural writing. The module identifies violations and (optionally) suggests corrections.

## 🚀 Features

Detects missing articles or demonstratives before nouns.

Ensures sentences are written in active voice.

Validates that each sentence contains only one instruction.

Enforces imperative (command) form in procedural writing.

Flags long sentences (more than 20 words).

CLI/Notebook interface for demonstration.

## 📜 Rules Implemented

Articles before nouns

❌ "Turn shaft assembly."

✅ "Turn the shaft assembly."

Active voice only

❌ "The safety procedures are supplied by the manufacturer."

✅ "The manufacturer supplies the safety procedures."

One instruction per sentence

❌ "Set the TEST switch and release the SHORT-CIRCUIT TEST switch."

✅
A. "Set the TEST switch."
B. "Release the SHORT-CIRCUIT TEST switch."

Imperative form

❌ "The test can be continued."

✅ "Continue the test."

Sentence length ≤ 20 words

Sentences longer than 20 words are flagged for readability
