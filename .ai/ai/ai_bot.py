# Apache License
# Version 2.0, January 2004
# Author: Eugene Tkachenko

from abc import ABC, abstractmethod
from ai.line_comment import LineComment
from log import Log

class AiBot(ABC):
    
    __no_response = "No critical issues found"
    __problems="errors, issues, potential crashes or unhandled exceptions"
    __gemini_ask_long="""
Act as a senior software engineer who is responsible for doing PR reviews, Review the below code with given git diffs and briefly describe {problems} etc?. Be strict about these areas if applicable: "{standards}" . While giving response, do not add intro words, response format should be: "lineNumber : cause effect"
If there are no issues just say "{no_response}".

DIFFS:

{diffs}

Full code from the file:

{code}
"""

    @abstractmethod
    def ai_request_diffs(self, code, diffs) -> str:
        pass

    @staticmethod
    def build_ask_text(code, diffs, standards) -> str:
        Log.print_green("Standards", standards)
        return AiBot.__gemini_ask_long.format(
            problems = AiBot.__problems,
            no_response = AiBot.__no_response,
            diffs = diffs,
            code = code,
            standards=standards,
        )

    @staticmethod
    def is_no_issues_text(source: str) -> bool:
        target = AiBot.__no_response.replace(" ", "")
        source_no_spaces = source.replace(" ", "")
        return source_no_spaces.startswith(target)
    
    @staticmethod
    def split_ai_response(input) -> list[LineComment]:
        if input is None or not input.strip():
            return []
        
        lines = input.strip().split("\n")
        models = []

        for full_text in lines:
            full_text = full_text.strip()
            if len(full_text) == 0:
                continue

            # Use regex to find the number at the beginning, followed by a colon
            match = re.match(r'(\d+(?:\s\d+)*):', full_text)
            if match:
                # Extract the line number
                number_str = match.group(1).replace(" ", "")
                number = int(number_str)
                
                # Extract the text after the line number and colon
                text = full_text[match.end():].strip()
            else:
                # If no match is found, default to line 0
                number = 0
                text = full_text

            models.append(LineComment(line=number, text=text))
        
        return models
    