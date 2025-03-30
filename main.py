import sys
import argparse


class Regex:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.groups = {}
        self.alternatives = self.split_alternatives(pattern)  

    def tokenize(self, pattern: str):
        tokens = []
        i = 0
        length = len(pattern)

        while i < length:
            char = pattern[i]

            if char == '^':
                tokens.append({"type": "START", "value": char, "position": i})

            elif char == '$':
                tokens.append({"type": "END", "value": char, "position": i})

            elif char in '*+?':
                tokens.append({"type": "QUANTIFIER", "value": char, "position": i})

            elif char == '\\' and i + 1 < length:
                escape_seq = pattern[i: i + 2]
                tokens.append({"type": "ESCAPE", "value": escape_seq, "position": i})
                i += 1  

            elif char == '[':
                set_end = pattern.find("]", i)
                if set_end == -1:
                    raise ValueError("Unmatched '[' in regex pattern")
                tokens.append({"type": "CHAR_SET", "value": pattern[i:set_end + 1], "position": i})
                i = set_end  

            elif char == "(":
                tokens.append({"type": "GROUP_START", "value": char, "position": i})

            elif char == ")":
                tokens.append({"type": "GROUP_END", "value": char, "position": i})

            elif char == ".":
                tokens.append({"type": "WILDCARD", "value": char, "position": i})

            else:
                tokens.append({"type": "LITERAL", "value": char, "position": i})

            i += 1  

        return tokens

    def match_token(self, token, char):
        if token['type'] == 'LITERAL':
            return token['value'] == char

        elif token['type'] == 'WILDCARD':
            return True  

        elif token['type'] == 'CHAR_SET':
            charset = token['value'][1:-1]  
            return char in charset

        elif token['type'] == 'ESCAPE':
            escaped_char = token['value'][1]
            if escaped_char == 'd':
                return char.isdigit()
            elif escaped_char == 'w':
                return char.isalnum() or char == '_'
            elif escaped_char == 's':
                return char.isspace()
            return escaped_char == char

        return False

    def helper_star(self, token, string, idx_string):
        count = 0
        while idx_string + count < len(string) and self.match_token(token, string[idx_string + count]):
            count += 1
        return count  

    def helper_plus(self, token, string, idx_string):
        count = self.helper_star(token, string, idx_string)
        return count if count > 0 else -1  

    def helper_question(self, token, string, idx_string):
        return 1 if idx_string < len(string) and self.match_token(token, string[idx_string]) else 0


    def match_sequence(self, tokens, string, idx_string=0, idx_token=0 , group_stack=[]):
        if idx_token >= len(tokens):
            return idx_string == len(string)  

        token = tokens[idx_token]

        if token['type'] == 'END':  
            return idx_string == len(string)
        
        if token['type'] == 'GROUP_START':
            group_stack.append(idx_string)
            return self.match_sequence(tokens, string, idx_string, idx_token+1 , group_stack)
        
        if token['type'] == 'GROUP_END':
            start_index = group_stack.pop()
            self.groups[len(self.groups)+1] = string[start_index : idx_string]
            return self.match_sequence(tokens, string, idx_string, idx_token + 1, group_stack)  


        if idx_token + 1 < len(tokens) and tokens[idx_token + 1]['type'] == 'QUANTIFIER':
            quantifier = tokens[idx_token + 1]['value']

            if quantifier == '*':  
                count = self.helper_star(token, string, idx_string)

            elif quantifier == '+':  
                count = self.helper_plus(token, string, idx_string)
                if count == -1:
                    return False

            elif quantifier == '?':  
                count = self.helper_question(token, string, idx_string)

            return self.match_sequence(tokens, string, idx_string + count, idx_token + 2)

        if idx_string >= len(string):
            return False  

        if not self.match_token(token, string[idx_string]):
            return False

        return self.match_sequence(tokens, string, idx_string + 1, idx_token + 1)  
    
    def split_alternatives(self, pattern: str):
        parts = pattern.split('|')  
        return [self.tokenize(part) for part in parts]  
    
    def match(self, string: str) -> bool:
        for tokens in self.alternatives:
            self.groups.clear()
            if self.match_sequence(tokens, string):
                return True  
        return False  

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Regex Matcher CLI")

    parser.add_argument("pattern", type=str, help="Regex pattern to match")
    parser.add_argument("strings", type=str, nargs="+", help="Test strings to check against the pattern")
    
    args = parser.parse_args()
    
    regex = Regex(args.pattern)
    print(f"Pattern: {args.pattern}")
    
    for string in args.strings:
        result = regex.match(string)
        if regex.groups:
            print("Captured Groups:", regex.groups)
        print(f"'{string}' -> {'MATCH' if result else 'NO MATCH'}")