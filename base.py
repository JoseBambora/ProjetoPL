from liststructs import ListStatic
from liststructs import ListVar

class Base:
    def __init__(self, variaveis):
        self.struct = variaveis

    def toPythonBase(self):
        args = []
        for arg in self.struct:
            if isinstance(arg, list):
                args.append("".join(arg))
            elif isinstance(arg, ListVar) or isinstance(arg, ListStatic):
                # print(arg.toPythonArgs())
                # print(arg.toPythonIf())
                args.append(arg.getName())
            else:
                args.append(arg)
        return ', '.join(args)

