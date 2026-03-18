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
Write a short poem comparing tomorrow's weather in these locations.

{ text }

Write in English and Portuguese.
Suggest where it is nicest to be tomorrow.
"""

response = client.chat.completions.create(
model="llama-3.1-8b-instant",
messages=[{"role": "user", "content": prompt}]
)

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
