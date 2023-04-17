import logging
class Range:
    def __init__(self,lower_range:int,upper_range:int):
        if lower_range >= upper_range:
            self.range = [lower_range,pow(2,512)-1,0,upper_range]
        else:
            self.range = [lower_range,upper_range]
    def __len__(self):
        return len(self.range)

    def __contains__(self,id:int):
        try:
            if id >= self.range[0] and id <= self.range[1]:
                return True
            elif id >= self.range[2] and id <= self.range[3]:
                return True
            else:
                return False
        except:
            return False
    
    def serialize(self):
        return self.range
    
    def update(self,id:int):
        aux = [id+1,self.range[-1]]
        if aux[0] > aux[1]:
            self.range = [id+1,pow(2,512)-1,0,self.range[-1]]
        else:
            self.range = aux
        