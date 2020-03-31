import configparser


class UnquotedConfigParser(configparser.ConfigParser):
    """Custom ConfigParser instance that strips quoted strings

    As several configuration options begin with leading /'s, support their extraction when wrapped in quotes.
    """

    def __init__(self):
        configparser.ConfigParser.__init__(self)

    def get(self, section, option, *, raw=False, vars=None, fallback=object()):
        result = configparser.ConfigParser.get(self=self, section=section, option=option, raw=raw, vars=vars,
                                               fallback=fallback)
        return result.replace('"', '')
