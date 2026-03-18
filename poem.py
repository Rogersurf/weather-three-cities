# poem.py

import sqlite3
from groq import Groq
import os

client = Groq(api_key=os.environ["GROQ_API_KEY"])

conn = sqlite3.connect("weather.db")
cur = conn.cursor()

rows = cur.execute("SELECT * FROM weather").fetchall()

text = "\n".join(str(r) for r in rows)

prompt = f"""
Weather data for tomorrow:

{text}

Write a short poem comparing the weather in the three cities.

Choose ONE of the following rhyme structures:

1) ABAB
Line 1 → rhyme A
Line 2 → rhyme B
Line 3 → rhyme A
Line 4 → rhyme B

Example:
The sun warms gently by the sea (A)
Cold winds arrive from northern air (B)
Soft waves reflect a golden key (A)
While clouds drift slowly everywhere (B)

2) ABBA
Line 1 → rhyme A
Line 2 → rhyme B
Line 3 → rhyme B
Line 4 → rhyme A

Example:
Bright sunlight dances on the shore (A)
Grey clouds gather in the sky (B)
Cool winds whisper passing by (B)
While warmth returns once more (A)

3) Brazilian-style rhymed stanza (quadra / cordel style)
4 lines with simple rhymes at the end.

Example:
No Rio o sol reluz
O vento sopra em Aalborg
Se quer fugir da chuva
Copenhague é boa sorte

Requirements:
- The poem must compare the weather in the three cities.
- Each line must end with rhyming words.
- Suggest where it would be nicest to be tomorrow.
- First write the poem in English.
- Then repeat the poem in Portuguese with rhymes.
"""

poem = response.choices[0].message.content

with open("docs/index.html","w") as f:
    f.write(f"""
    <html>
    <body>
    <h1>Weather Poem</h1>
    <pre>{poem}</pre>
    </body>
    </html>
    """)

print("Poem generated")
