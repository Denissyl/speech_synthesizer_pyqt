import sqlite3


def get_syllables_and_letters():
    letters_syllables = {}
    con = sqlite3.connect('sounds.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM sounds")
        rows = cur.fetchall()

        for row in rows:
            letters_syllables[row[0]] = row[1]
            upping = row[0].upper()
            letters_syllables[upping] = row[1]
    return letters_syllables
