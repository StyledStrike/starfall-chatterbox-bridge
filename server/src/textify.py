import re

# Replace things that are separated by a space.
WORD_REPLACEMENTS = {
    "wtf": "what the fuck",
    "lmao": "la mao",
    "etc": "etcetera",
    "nvm": "nevermind",
    "brb": "be right back",
    "ig": "I guess",
    "im": "I am",
    "i'm": "I am",
    "js": "Javascript",
    "sf": "Starfall",
    "e2": "Expression Two",
    "pac": "pack",
    "km": "kilometer",
    "m": "meter",
    "m/s": "meters per second",
    "km/s": "kilometers per second",
    "km/h": "kilometers per hour",
    "mph": "miles per hour",
    "ft": "feet",
    "gmod": "Garry's Mod",
    "atm": "at the moment",
    "ngl": "not gonna lie",
    "diarrhea": "die a ree uhh",
    "tbh": "to be honest",
    "mfw": "my face when",
    "tfw": "that feeling when",
    "knee ghers": "nuuh",
    "snicker": "isneech er",
    "sybau": "shut yo bitch ass up",
    "cs2": "Counter-Strike Two",
    "f2p": "free-to-play",
    "idk": "I don't know",
    "ikr": "I know, right?",
    "wdym": "what do you mean",
    "pmo": "pisses me off",
    "idc": "I don't care",
    "fr": "for real",
    "rip": "rest in peace",
    "rn": "right now",
    "pls": "please",
    "afaik": "as far as I know",
    "mf": "motherfucker",
    "ur": "you are",
    "fw": "fuck with",
    "cya": "see ya",
    "btw": "by the way",
    "np": "no problem",
    "wb": "welcome back",
    "thx": "thanks"
}

# Replace these exactly as they show up in the text.
VERBATIM_REPLACEMENTS = {
    ";)": "wink",
    ":3": "meow",
    "( ͡° ͜ʖ ͡°)": "lenny face",
    "( °     ͜ʖ   °)": "wide lenny face",
    "( ° ͜ʖ °)": "lenny face",
    "( ͡º ‿ʖ ͡º)": "smug lenny face",
    "( ͝סּ ͜ʖ͡סּ)_/¯": "salty lenny face",
    "( ͡o ͜ʖ ͡o)_/¯": "salty lenny face",
    "( ಠ ͜ʖಠ)_/¯": "salty lenny face",
    "( °     ͜ʖ    °)": "wide lenny face",
    "(͡ ͡° ͜ つ ͡͡°)": "nosey lenny face",
    "¯\\_(ツ)_/¯": "shrug",
    "( ͠° ͟ʖ ͡°)": "annoyed lenny face",
    "(╯°□°）╯︵ ┻━┻": "table flip",
    "(づ •◡• )づ": "cute lenny face",
    "( ° ω °)": "kitty lenny face",
    "(ง'̀-'́)ง": "fighter lenny face",
    #"˙ ͜ʟ˙": "desfigured lenny face",
}

# Only spell these symbols when they are surrounded by spaces.
DONT_SPELL_SYMBOLS = {
    33: True, # Exclamation mark
    34: True, # Quote
    39: True, # Single quote
    40: True, # Open parenthesis
    41: True, # Close parenthesis
    42: True, # Asterisk
    44: True, # Comma
    45: True, # Hyphen
    46: True, # Period
    58: True, # Colon
    59: True, # Semicolon
    63: True  # Question mark
}

SYMBOLS = {
    33: "Exclamation mark",
    34: "Quote",
    35: "Hashtag",
    36: "Dollar",
    37: "Per cent",
    38: "Ampersand",
    39: "Single quote",
    40: "Open parenthesis",
    41: "Close parenthesis",
    42: "Asterisk",
    43: "Plus",
    44: "Comma",
    45: "Hyphen",
    46: "Period",
    47: "Slash",
    58: "Colon",
    59: "Semicolon",
    60: "Less than",
    61: "Equals",
    62: "Greater than",
    63: "Question mark",
    64: "At",
    91: "Opening bracket",
    92: "Backslash",
    93: "Closing bracket",
    94: "Self", #Caret
    95: "Underscore",
    96: "Grave accent",
    123: "Opening brace",
    124: "Vertical bar",
    125: "Closing brace",
    126: "tilde",
    8364: "Euro sign",
    8218: "Single low-nine quotation mark",
    402: "Latin small letter f with hook",
    8222: "Double low-nine quotation mark",
    8230: "Horizontal ellipsis",
    8224: "Dagger",
    8225: "Double dagger",
    710: "Modifier letter circumflex accent",
    8240: "Per mille sign",
    352: "Latin capital letter S with caron",
    8249: "Single left-pointing angle quotation",
    338: "Latin capital ligature OE",
    381: "Latin capital letter Z with caron",
    8216: "Left single quotation mark",
    8217: "Right single quotation mark",
    8220: "Left double quotation mark",
    8221: "Right double quotation mark",
    8226: "Bullet",
    8211: "En dash",
    8212: "Em dash",
    732: "Small tilde",
    8482: "Trade mark",
    353: "Latin small letter S with caron",
    8250: "Single right-pointing angle quotation mark",
    339: "Latin small ligature oe",
    382: "Latin small letter z with caron",
    376: "Latin capital letter Y with diaeresis",
    161: "Inverted exclamation mark",
    162: "Cent",
    163: "Pound",
    164: "Currency sign",
    165: "Yen",
    166: "Pipe, Broken vertical bar",
    167: "Section sign",
    168: "Spacing diaeresis - umlaut",
    169: "Copyright",
    170: "Feminine ordinal indicator",
    171: "Left double angle quotes",
    172: "Not sign",
    174: "Registered trade mark sign",
    175: "Spacing macron - overline",
    176: "Degree",
    177: "Plus-or-minus",
    178: "Superscript two - squared",
    179: "Superscript three - cubed",
    180: "Acute accent - spacing acute",
    181: "Micro sign",
    182: "Pilcrow sign - paragraph sign",
    183: "Middle dot - Georgian comma",
    184: "Spacing cedilla",
    185: "Superscript one",
    186: "Masculine ordinal indicator",
    187: "Right double angle quotes",
    188: "Fraction one quarter",
    189: "Fraction one half",
    190: "Fraction three quarters",
    191: "Inverted question mark",
    192: "Latin capital letter A with grave",
    193: "Latin capital letter A with acute",
    194: "Latin capital letter A with circumflex",
    195: "Latin capital letter A with tilde",
    196: "Latin capital letter A with diaeresis",
    197: "Latin capital letter A with ring above",
    198: "Latin capital letter AE",
    199: "Latin capital letter C with cedilla",
    200: "Latin capital letter E with grave",
    201: "Latin capital letter E with acute",
    202: "Latin capital letter E with circumflex",
    203: "Latin capital letter E with diaeresis",
    204: "Latin capital letter I with grave",
    205: "Latin capital letter I with acute",
    206: "Latin capital letter I with circumflex",
    207: "Latin capital letter I with diaeresis",
    208: "Latin capital letter ETH",
    209: "Latin capital letter N with tilde",
    210: "Latin capital letter O with grave",
    211: "Latin capital letter O with acute",
    212: "Latin capital letter O with circumflex",
    213: "Latin capital letter O with tilde",
    214: "Latin capital letter O with diaeresis",
    215: "Multiplied",
    216: "Latin capital letter O with slash",
    217: "Latin capital letter U with grave",
    218: "Latin capital letter U with acute",
    219: "Latin capital letter U with circumflex",
    220: "Latin capital letter U with diaeresis",
    221: "Latin capital letter Y with acute",
    222: "Latin capital letter THORN",
    223: "Latin small letter sharp s - ess-zed",
    224: "Latin small letter a with grave",
    225: "Latin small letter a with acute",
    226: "Latin small letter a with circumflex",
    227: "Latin small letter a with tilde",
    228: "Latin small letter a with diaeresis",
    229: "Latin small letter a with ring above",
    230: "Latin small letter ae",
    231: "Latin small letter c with cedilla",
    232: "Latin small letter e with grave",
    233: "Latin small letter e with acute",
    234: "Latin small letter e with circumflex",
    235: "Latin small letter e with diaeresis",
    236: "Latin small letter i with grave",
    237: "Latin small letter i with acute",
    238: "Latin small letter i with circumflex",
    239: "Latin small letter i with diaeresis",
    240: "Latin small letter eth",
    241: "Latin small letter n with tilde",
    242: "Latin small letter o with grave",
    243: "Latin small letter o with acute",
    244: "Latin small letter o with circumflex",
    245: "Latin small letter o with tilde",
    246: "Latin small letter o with diaeresis",
    247: "Divided",
    248: "Latin small letter o with slash",
    249: "Latin small letter u with grave",
    250: "Latin small letter u with acute",
    251: "Latin small letter u with circumflex",
    252: "Latin small letter u with diaeresis",
    253: "Latin small letter y with acute",
    254: "Latin small letter thorn",
    255: "Latin small letter y with diaeresis",
}

# Array of units as words
UNITS = [
    "",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]

# Array of tens as words
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

# Array of scales as words
SCALES = [
    "",
    "thousand",
    "million",
    "billion",
    "trillion",
    "quadrillion",
    "quintillion",
    "sextillion",
    "septillion",
    "octillion",
    "nonillion",
    "decillion",
    "undecillion",
    "duodecillion",
    "tredecillion",
    "quatttuor-decillion",
    "quindecillion",
    "sexdecillion",
    "septen-decillion",
    "octodecillion",
    "novemdecillion",
    "vigintillion",
    "unvigintillion",
]

def numberToEnglish(number: str):
    """
    Convert an integer to its words representation.

    Slightly modified from the original by StyledStrike to work with
    Python, have better pauses between scales, and handle absolutely huge humbers.

    @author McShaman (http://stackoverflow.com/users/788657/mcshaman)
    @source http://stackoverflow.com/questions/14766951/convert-digits-into-words-with-javascript
    """

    if number == "0":
        return "zero"
    
    # Split number into 3 digit chunks from right to left
    chunks = []
    start = len(number)
    end = 0

    while start > 0:
        end = start
        start = max(0, start - 3)
        chunks.append(number[start:end])

    words = []

    # Check if we have enough scale words to be able to stringify the number
    chunksLen = len(chunks)

    if chunksLen > len(SCALES):
        # If it is too big, lets spell numbers separately instead
        num = 0

        for i in range(len(number)):
            num = int(number[i])
            
            if num == 0:
                words.append("zero")
            else:
                words.append(UNITS[num])
        
        return " ".join(words)

    def getStr(l: list, i: int):
        return l[i] if i < len(l) and l[i] != "" else None

    def appendFrom(l: list, i: int):
        if i < len(l) and l[i] != "":
            words.append(l[i])

    for i in range(chunksLen):
        chunk = chunks[i]

        # Split chunk into a reversed array of individual integers
        ints = list(chunk)
        ints.reverse()

        for j in range(len(ints)):
            ints[j] = int(ints[j])

        intsLen = len(ints)

        def getInt(index: int):
            return ints[index] if index < intsLen else None

        # If tens integer is 1, i.e. 10, then add 10 to units integer
        if getInt(1) == 1:
            ints[0] += 10

        # Add scale word if chunk is not zero
        if i > 0:
            appendFrom(SCALES, i)

        # Add unit word
        appendFrom(UNITS, ints[0])

        # Add tens word
        t = getInt(1)

        if t is not None:
            appendFrom(TENS, t)

        # Add hundreds word if array item exists
        h = getInt(2)

        if h is not None and h > 0 and h < len(UNITS):
            # Add "and" string after units or tens integer
            # if we have tens/units available.
            if (t is not None and ints[0] > 0):
                words.append("and")

            words.append(UNITS[h] + " hundred")

    words.reverse()

    return " ".join(words)

def replaceNumberFunc(matchobj):
    return numberToEnglish(matchobj.group(1))

def getSymbolWordFrom(text: str, pos: int):
    if pos < 0 or pos >= len(text):
        return None

    return SYMBOLS.get(ord(text[pos]), None)

def getChar(text: str, pos: int):
    if pos < 0 or pos >= len(text):
        return " "

    return text[pos]

def textify(text: str, symbolsToWords = False, numbersToWords = False):
    # Word replacements
    words = text.split()

    for i in range(len(words)):
        words[i] = WORD_REPLACEMENTS.get(words[i], words[i])

    text = " ".join(words)

    # Verbatim replacements
    for index in VERBATIM_REPLACEMENTS:
        text = text.replace(index, VERBATIM_REPLACEMENTS[index])

    # Replace symbols with words
    if symbolsToWords:
        parts = []
        textLen = len(text)

        for i in range(textLen):
            char = text[i]
            symbol = getSymbolWordFrom(text, i)

            if symbol is None:
                parts.append(char)
            else:
                prevChar = getChar(text, i - 1)
                nextChar = getChar(text, i + 1)
                dontSpell = DONT_SPELL_SYMBOLS.get(ord(char), False)

                if dontSpell and not (prevChar == " " and nextChar == " "):
                    parts.append(char)
                else:
                    if prevChar != " ":
                        symbol = " " + symbol

                    if nextChar != " ":
                        symbol = symbol + " "

                    parts.append(symbol)

        text = "".join(parts)

    # Replace numbers with words
    if numbersToWords:
        text = re.sub('([0-9]+)', replaceNumberFunc, text)

    return text
