# Apache License
# Version 2.0, January 2004
# Author: Eugene Tkachenko

import os
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
from ai.ai_bot import AiBot
from google.colab import userdata



def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


class Gemini(AiBot):


    def __init__(self, token):
        GOOGLE_API_KEY=userdata.get(token)
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def ai_request_diffs(self, code, diffs):
        stream = model.start_chat(
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
    