class auto():
    
    def __init__(self, sigma, state, delta, init, final):
        self.sigma = sigma
        self.final = final
        self.init = init
        self.state = state
        self.delta = delta
        
    def printAuto(self):
        print(
            "\n",
            "SIGMA:", self.sigma, "\n",
            "FINAL:", self.final, "\n",
            "INIT:", self.init, "\n",
            "STATE:", self.state, "\n",
            "DELTA:", self.delta,
            "\n"
        )
        
    def accepted(self, w):
        arrayW = list(w)
        
        stateAc = self.init
        for aw in arrayW:
            # print("\nINIT:", aw)
            for tr in self.delta[stateAc]:
                if(tr[0] == aw):
                    stateAc = tr[1]
        
        if(stateAc in self.final):
            return True
        return False