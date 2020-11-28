
# python has token module so i use tokens here.


# ..pattern..  -> in:pattern
def quick_form_convert_to_special_form(Token, Sign):
    LenSign = len(Sign)
    if Sign in Token:
        StarPrefix = Token.startswith(Sign)
        StarPostfix = Token.endswith(Sign)
        if StarPrefix and StarPostfix: Token = "in:" + Token[LenSign:-LenSign]
        if StarPrefix and not StarPostfix: Token = "start:" + Token[LenSign:]
        if not StarPrefix and StarPostfix: Token = "end:" + Token[:-LenSign]
    return Token