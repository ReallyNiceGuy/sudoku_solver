#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import collections

class Solver(object):
  @staticmethod
  def makeConstraint(x0,y0,x1,y1):
    def validate(table):
      found = dict()
      for x in range(x0,x1):
        for y in range(y0,y1):
          if table[x][y] == ".":
            continue
          if table[x][y] in found:
            return False
          found[table[x][y]]=True
      return True
    return validate

  @staticmethod
  def getBlock(x,y):
    j=x//3
    k=y//3
    return (j,k)

  def __init__(self):
    self.initializeConstraints()

  def initializeConstraints(self):
    self.constraints = dict()
    constraintsRow = dict()
    constraintsCol = dict()
    constraintsBlock = dict()
    for x in range(0,9):
      if not x in constraintsCol:
        constraintsCol[x]=Solver.makeConstraint(x,0,x+1,9)
      for y in range(0,9):
        if not y in constraintsRow:
          constraintsRow[y]=Solver.makeConstraint(0,y,9,y+1)
        block = Solver.getBlock(x,y)
        if not block in constraintsBlock:
          j,k=block
          constraintsBlock[block]=Solver.makeConstraint(j*3,k*3,j*3+3,k*3+3)

        if not (x,y) in self.constraints:
          self.constraints[(x,y)] = []
        self.constraints[(x,y)].append(constraintsCol[x])
        self.constraints[(x,y)].append(constraintsRow[y])
        self.constraints[(x,y)].append(constraintsBlock[block])

  def validate(self,table):
    for x in range(0,9):
      for y in range(0,9):
        for v in self.constraints[(x,y)]:
          if not v(table):
            return False
    return True

  def isValid(self,table,x,y):
    for v in self.constraints[(x,y)]:
      if not v(table):
        return False
    return True

  def solve(self,table,cell=0):
    if cell>80:
      return True
    x = cell//9
    y = cell%9
    if table[x][y] != ".":
      return self.solve(table,cell+1)
    for tryVal in range(1,10):
      table[x][y] = str(tryVal)
      if self.isValid(table,x,y):
#        Solver.dumpTable(table)
#        print()
        ret = self.solve(table,cell+1)
        if ret:
          return True

    table[x][y]="."
    return False

  @staticmethod
  def dumpTable(table):
    for x in t:
      print("|",end="")
      for y in x:
        print(y+"|",end="")
      print("\n|-+-+-+-+-+-+-+-+-|")

  @staticmethod
  def loadTable(fn):
    t=[]
    f=open(fn)
    for line in f:
      t.append(list(line.strip('\n')))
    return t
 
if __name__ == "__main__":
  import sys
  t=Solver.loadTable(sys.argv[1])
  Solver.dumpTable(t)
  print()
  s=Solver()
  #print(s.validate(t))
  #exit(1)
  s.solve(t)
  Solver.dumpTable(t)

