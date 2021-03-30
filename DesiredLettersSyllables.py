def desired_letters_and_syllables(splited_words, letters_syllables):
    desired_letters_syllables = []
    print(splited_words)
    for l in splited_words:
        for j in l:
            if j not in letters_syllables:
                for i in j:
                    desired_letters_syllables.append(letters_syllables[i])
            else:
                desired_letters_syllables.append(letters_syllables[j])
    return desired_letters_syllables
