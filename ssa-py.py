#!/usr/bin/env python3
"""SSA (Static Single Assignment) form converter for simple programs."""
import sys,re

class SSA:
    def __init__(self):self.counter={};self.env={};self.code=[]
    def fresh(self,name):
        self.counter[name]=self.counter.get(name,0)+1
        v=f"{name}_{self.counter[name]}";self.env[name]=v;return v
    def lookup(self,name):
        if name in self.env:return self.env[name]
        return self.fresh(name)
    def convert(self,lines):
        for line in lines:
            line=line.strip()
            if not line:continue
            m=re.match(r'(\w+)\s*=\s*(.+)',line)
            if m:
                lhs,rhs=m.group(1),m.group(2)
                # Replace vars in rhs
                def repl(m2):
                    w=m2.group(0)
                    if w.isdigit():return w
                    return self.lookup(w)
                rhs2=re.sub(r'[a-zA-Z_]\w*',repl,rhs)
                new_lhs=self.fresh(lhs)
                self.code.append(f"{new_lhs} = {rhs2}")
            else:
                def repl(m2):
                    w=m2.group(0)
                    if w in('print','return'):return w
                    return self.lookup(w)
                self.code.append(re.sub(r'[a-zA-Z_]\w*',repl,line))
        return self.code

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        s=SSA()
        result=s.convert(["x = 1","y = x + 2","x = x + y","z = x * y"])
        assert result==["x_1 = 1","y_1 = x_1 + 2","x_2 = x_1 + y_1","z_1 = x_2 * y_1"]
        # No variable reuse — each assignment creates new version
        s2=SSA()
        r2=s2.convert(["a = 5","a = a + 1","a = a + 1"])
        assert r2==["a_1 = 5","a_2 = a_1 + 1","a_3 = a_2 + 1"]
        print("All tests passed!")
    else:
        s=SSA()
        code=["x = 1","y = x + 2","x = x + y","print x"]
        print("Original → SSA:")
        for orig,ssa in zip(code,s.convert(code)):print(f"  {orig:20s} → {ssa}")
if __name__=="__main__":main()
