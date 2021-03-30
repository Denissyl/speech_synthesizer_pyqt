def split_into_syllables(text):
    consonants = ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н',
                  'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
    vowels = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е']
    thud = ['к', 'п', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
    sonorous = ['м', 'н', 'р', 'л']

    if len(text) == 1:
        return [text]
    elif len(text) > 1:
        text = text.split()
        splited_words = []
        for word in text:
            word = word.lower()
            if not word == '@' or not all(c == word[0] for c in word[1:]):
                splited_word = ''
                syllable = ''
                i = 0
                while i < len(word):
                    current_letter = word[i]
                    syllable += current_letter
                    if current_letter in vowels:
                        if i + 1 < len(word):
                            letter1 = word[i + 1]
                            if letter1 in consonants:
                                if i + 1 >= len(word) - 1:
                                    syllable += letter1
                                    i += 1
                                else:
                                    letter2 = word[i + 2]
                                    if (letter1 == 'й' or letter1 == 'Й') and letter2 in consonants:
                                        syllable += letter1
                                        i += 1
                                    elif letter1 in sonorous and letter2 in thud:
                                        syllable += letter1
                                        i += 1
                                    elif letter1 in sonorous and letter2 in consonants and word[i + 3] in vowels\
                                            and letter1 != letter2:
                                        syllable += letter1
                                        i += 1
                                    elif letter2 == 'ь' or letter2 == 'ъ':
                                        i += 2
                                        syllable += letter1 + letter2
                                    elif i + 2 >= len(word) - 1 and letter2 in consonants:
                                        i += 2
                                        syllable += letter1 + letter2
                        splited_word += syllable
                        if i + 1 < len(word):
                            splited_word += '-'
                        syllable = ''
                    i += 1
                print(splited_word)
                splited_word = splited_word.split('-')
                splited_words.append(splited_word)
        return splited_words
