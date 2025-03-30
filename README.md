# 🔍 Custom Regex Engine in Python  

A **lightweight, custom-built regex engine** in Python that parses and matches regular expressions **without relying on Python's built-in `re` module**. This project aims to **understand and implement regex functionalities from scratch**! 🚀  

## 📌 Features Implemented  
✅ **Tokenization System** – Converts regex patterns into structured tokens.  
✅ **Matching System** – Recursive pattern evaluation for complex matching.  
✅ **Quantifiers Support** – `*`, `+`, `?` implemented.  
✅ **Alternation (`|`)** – Supports either-or matching.  
✅ **Character Sets (`[]`)** – Handles ranges like `[a-z]`.  
✅ **Escape Sequences (`\d`, `\w`, `\s`)** – Supports special characters.  
✅ **Grouping (`()`)** – Captures & stores substrings.  
✅ **Command-Line Interface (CLI)** – Regex matching directly via terminal.  

## 🚀 Getting Started  

### **Prerequisites**  
Ensure you have Python installed (Python 3.7+ recommended).  

### **Installation**  
Clone the repository:  
```sh
git clone https://github.com/yourusername/custom-regex-engine.git
cd custom-regex-engine
```

### **Usage**  
Run the CLI to match a string against a regex pattern:  
```sh
python regex_engine.py "a|b+" "a" "b" "bb" "c"
```
Output:  
```
Pattern: a|b+
'a' -> MATCH
'b' -> MATCH
'bb' -> MATCH
'c' -> NO MATCH
```

## 🔍 Scope for Improvement  
🔹 **Backreferences (`\1`, `\2`)** – Reusing captured groups.  
🔹 **Lookaheads & Lookbehinds** – Advanced pattern matching.  
🔹 **Greedy & Lazy Matching** – Implementing `.*?` for lazy quantifiers.  
🔹 **File Search Integration** – Scanning entire text files for matches.  

## 🤝 Contributing  
Contributions are welcome! Feel free to open issues, fork the repo, and submit pull requests.  

