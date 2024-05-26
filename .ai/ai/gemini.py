# Apache License
# Version 2.0, January 2004
# Author: Eugene Tkachenko

import os
import pathlib
import textwrap

import google.generativeai as genai
from ai.ai_bot import AiBot




class Gemini(AiBot):


    def __init__(self, token):
        genai.configure(api_key=token)
        self.__model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def ai_request_diffs(self, code, diffs):
        stream = self.__model.start_chat(
            history=[
                {
                    "role": "user",
                    "content": AiBot.build_ask_text(code=code, diffs=diffs),
                }
            ],
            stream = True,
        )
        content = []
        for chunk in stream:
            if chunk.text:
                content.append(chunk.text)
        return " ".join(content)
    