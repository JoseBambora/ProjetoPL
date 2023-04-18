class Resultado:
    def __init__(self,ret,valorRet,pv):
        self.struct = (ret,valorRet,pv)
    def pp(self):
        return self.struct[1]