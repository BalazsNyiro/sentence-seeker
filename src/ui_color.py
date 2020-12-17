# https://www.geeksforgeeks.org/formatted-text-linux-terminal-using-python/
# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
Colors = {
    'Black': '30', 'Bright Black': '90',
    'Red': '31', 'Bright Red': '91',
    'Green': '32', 'Bright Green': '92',
    'Yellow': '33', 'Bright Yellow': '93',
    'Blue': '34', 'Bright Blue': '94',
    'Cyan': '36', 'Bright Magenta': '95',
    'White': '37', 'Bright Cyan': '96',
    'Default': '39', 'Bright White': '97',

    'Plain': '0',  # xfce4-term    gnome-term
    'Bold': '1',  # +                +
    'Italic': '3',  # -                +
    'Underline': '4',
    'Blink': '5',

    # swap foreground and bg colour
    'Reverse': '7',

    'CursorHide': '?25l',
    'CursorShow': '?25h'
}


def color_reset():
    return color("Plain") + color("Default")


__color_name_last_used = ["Default"]
__style_last_used = ["Plain"]


def color(ColorName, CnameBackground=""):
    ColorBackground = ""
    global __color_name_last_used, __style_last_used

    # print('\033[38;5;188;48;5;22mAlma')
    try:  # ha 256 szinu tablazatbol dolgozunk, ColorName egy szam:
        ColorFg = "38;5;" + str(
            int(ColorName))  # ha ez sikerul, akkor csak szamot kaptunk - amit visszaalakitunk stringge
        if CnameBackground:
            ColorBackground = ";48;5;" + str(int(CnameBackground))
        ControlChars = ColorFg + ColorBackground + "m"
        # print(ControlChars)
        return AnsiControlInit + ControlChars  # 38: foreground

    except:  # ha ColorName szoveges, tehat a fenti tablazatbol kell kivalasztani vmit
        if CnameBackground:
            if CnameBackground not in Colors:
                print("Color name error, not in table: ", CnameBackground)
            CodeBg = Colors[CnameBackground]
            if len(CodeBg) == 2:
                CodeBg = str(int(CodeBg) + 10)
            ColorBackground = ";" + CodeBg

        if "Prev" in ColorName:  # ColorPrev, StylePrev
            # the current color is in -1, so Previous id == -2
            if "ColorPrev" == ColorName:
                ColorName = __color_name_last_used[-2]
                colorCode = Colors[ColorName]
                __color_name_last_used.append(ColorName)
            if "StylePrev" == ColorName:
                ColorName = __style_last_used[-2]
                colorCode = Colors[ColorName]
                __style_last_used.append(ColorName)
        else:

            if ColorName not in Colors:
                print("Color name error, not in table: ", ColorName)

            colorCode = Colors[ColorName]

            Styles = ['Plain',
                      'Bold',
                      'Italic',
                      'Underline',
                      'Blink',
                      'Reverse',
                      'CursorHide',
                      'CursorShow', ]

            MaxElem = 20  # limit of memory usage
            if ColorName in Styles:
                __style_last_used.append(ColorName)
                __style_last_used = __style_last_used[-MaxElem:]

            else:
                __color_name_last_used.append(ColorName)
                __color_name_last_used = __color_name_last_used[-MaxElem:]

        # it doesn't work: return '\\e[' + colorCode + 'm'
        ColorControl = colorCode + ColorBackground + 'm'
        # print("ColorControl: " + ColorControl)

        ColorString = AnsiControlInit + ColorControl
        return ColorString


AnsiControlInit = '\033['  # echo -e "\x1b[93;41m"  # example  \x1b is \033 in python
