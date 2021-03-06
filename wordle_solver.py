import PySimpleGUI as sg


# Messages
checkbox_message = """If checked, will assume that the character in the input box (can only be 1 character) must be in this slot.
If unchecked, will assume that the characters in the input box are required but can't be in this slot"""

def make_window(theme=None):
    if theme:
        sg.theme(theme)
    # -----  Layout & Window Create  -----
    layout = [  [sg.Text(text="Enter Bad Letters Here:", size=(30, 1))],
                [sg.Input(size=(30, 1), key='used')],
                [sg.Text(text="Enter Good Letters Here:", size=(30, 1))],
                [sg.Input(size=(30, 1), key="required")],
                [sg.Checkbox("Include", key='include0', tooltip=checkbox_message), sg.Input(size=(30, 1), key='slot0')],
                [sg.Checkbox("Include", key='include1', tooltip=checkbox_message), sg.Input(size=(30, 1), key='slot1')],
                [sg.Checkbox("Include", key='include2', tooltip=checkbox_message), sg.Input(size=(30, 1), key='slot2')],
                [sg.Checkbox("Include", key='include3', tooltip=checkbox_message), sg.Input(size=(30, 1), key='slot3')],
                [sg.Checkbox("Include", key='include4', tooltip=checkbox_message), sg.Input(size=(30, 1), key='slot4')],
                [sg.Multiline(default_text="No results yet!", size=(39, 4), key='results', disabled=True)],
                [sg.Button('Calculate'), sg.Exit(), sg.Button('Change Theme')]]

    return sg.Window('Wordle Solver', layout)

# All the stuff inside your window.


# Create the Window
window = make_window('Python')

# LOAD WORDS
with open("words.txt") as word_file:
    english_words = set(word.strip().lower() for word in word_file)


# FUNCTIONS
def is_english_word(word):
    return word.lower() in english_words


def selection(chars, choose, letters):
    """'chars' provides letters to exempt from selection unless choose == 1, in which case 'chars' should only have 1 character in it: the one desired for selection"""

    if choose == "1":
        return set(letters) - set(x for x in letters if x is not chars)
    else:
        return set(letters) - set([x for x in chars])


def get_possible_words(chars_a, chars_b, chars_c, chars_d, chars_e, possible_letters, required_letters):

    set_a = selection(chars_a[:-1], chars_a[-1], possible_letters)
    set_b = selection(chars_b[:-1], chars_b[-1], possible_letters)
    set_c = selection(chars_c[:-1], chars_c[-1], possible_letters)
    set_d = selection(chars_d[:-1], chars_d[-1], possible_letters)
    set_e = selection(chars_e[:-1], chars_e[-1], possible_letters)

    required = list(required_letters)

    words = ""

    for a in set_a:
        for b in set_b:
            for c in set_c:
                for d in set_d:
                    for e in set_e:

                        word = a + b + c + d + e

                        if is_english_word(word):

                            if sum([1 for i in required if i in word]) == len(required):

                                words += word + ", "
    
    return words[:-2]


# Event Loop to process "events" and get the "values" of the inputs
while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    
    elif event == "Calculate":

        all_letters = [i for i in "abcdefghijklmnopqrstuvwxyz"]

        chars_a = values["slot0"].strip() + str(int(values["include0"] == True))
        chars_b = values["slot1"].strip() + str(int(values["include1"] == True))
        chars_c = values["slot2"].strip() + str(int(values["include2"] == True))
        chars_d = values["slot3"].strip() + str(int(values["include3"] == True))
        chars_e = values["slot4"].strip() + str(int(values["include4"] == True))

        used = values["used"].strip()

        letters = [i for i in all_letters if i not in list(used)]

        required_letters = values["required"].strip()

        words = get_possible_words(chars_a, chars_b, chars_c, chars_d, chars_e, letters, required_letters)

        window['results'].update(words)

    elif event == "Change Theme":
        event, values = sg.Window('Choose Theme', [[sg.Combo(sg.theme_list(), readonly=True, k='themes'), sg.OK(), sg.Cancel()]]).read(close=True)

        if event == 'OK':
            # ---- Switch to your new theme! ---- IMPORTANT PART OF THE PROGRA<
            window.close()
            window = make_window(values['themes'])

window.close()


# ------------------- Main Program and Event Loop -------------------
def main():
    window = make_window()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        if event == 'Change Theme':      # Theme button clicked, so get new theme and restart window
            event, values = sg.Window('Choose Theme',
                                      [[sg.Combo(sg.theme_list(), readonly=True, k='-THEME LIST-'), sg.OK(), sg.Cancel()]]
                                      ).read(close=True)
            if event == 'OK':
                # ---- Switch to your new theme! ---- IMPORTANT PART OF THE PROGRA<
                window.close()
                window = make_window(values['-THEME LIST-'])

    window.close()