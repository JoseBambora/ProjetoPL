class Base:
    def __init__(self, variaveis):
        self.struct = variaveis

    def toPythonBase(self):
        args = []
        for arg in self.struct:
            if isinstance(arg, list):
                args.append("".join(arg))
            else:
                args.append(arg)
        return ', '.join(args)

