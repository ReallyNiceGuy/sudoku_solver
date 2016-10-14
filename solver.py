#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import copy
import re
import collections

class Solver(object):
  constraints = None
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
    if Solver.constraints is None:
      Solver.constraints = Solver.initializeConstraints()

  @staticmethod
  def initializeConstraints():
    c = dict()
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

        if not (x,y) in c:
          c[(x,y)] = []
        c[(x,y)].append(constraintsCol[x])
        c[(x,y)].append(constraintsRow[y])
        c[(x,y)].append(constraintsBlock[block])
    return c

  @staticmethod
  def validate(table):
    for x in range(0,9):
      for y in range(0,9):
        for v in Solver.constraints[(x,y)]:
          if not v(table):
            return False
    return True

  @staticmethod
  def isValid(table,x,y):
    for v in Solver.constraints[(x,y)]:
      if not v(table):
        return False
    return True

  @staticmethod
  def getNextCell(table,valids):
    minVal=10
    cell = []
    vals = []
    for key,values in valids.items():
      j,k = key
      t = 0
      if table[j][k] != ".":
        continue
      lvals = []
      for i in values:
        table[j][k]=i
        if Solver.isValid(table,j,k):
          t=t+1
          lvals.append(str(i))
          if t>=minVal:
            break
      table[j][k]="."
      if t<minVal:
        minVal=t
        vals=lvals
        cell=[(j,k)]
        if t==1:break
    return (cell,vals)

  @staticmethod
  def makeValidValues(table):
    v = dict()
    for j in range(0,9):
      for k in range(0,9):
        if table[j][k] != ".":
          continue
        v[(j,k)]=[]
        for i in range(1,10):
          table[j][k]=str(i)
          if Solver.isValid(table,j,k):
            v[(j,k)].append(str(i))
        table[j][k]="."
    return collections.OrderedDict(sorted(v.items(),key=lambda t: [len(t[1]),t[1]]))


  @staticmethod
  def solve(table):
    solution = []
    t = copy.deepcopy(table)
    valids = Solver.makeValidValues(t)
    Solver.__solve(t,valids,Solver.getNextCell(t,valids),solution)
    return (t,solution)

  @staticmethod
  def __solve(table,valids,order,solution):
    if len(order[0])==0:
      return True
    x, y = order[0][0]
    if table[x][y] != ".":
      return Solver.__solve(table,valids,Solver.getNextCell(table,valids),solution)
    for tryVal in order[1]:
      table[x][y] = tryVal
      solution.append((copy.deepcopy(table),(x,y)))
      ret = Solver.__solve(table,valids,Solver.getNextCell(table,valids),solution)
      if ret:
        return True

    table[x][y]="."
    if len(solution)>0: solution.pop()
    return False

  @staticmethod
  def dumpTable(table,start=None,j=None,k=None):
    if start is None:
      start=table
    print  ("┌─────┬─────┬─────┐")
    for x in range(len(table)):
      for y in range(len(table[x])):
        if y%3 == 0:
          print("│",end="")
        else:
          print(" ",end="")
        if table[x][y] != ".":
          if table[x][y] == start[x][y]:
            print(chr(ord(table[x][y])+0x1d7ec-ord("0")),end="")
          elif x==j and y==k:
            print(chr(ord(table[x][y])+0x277f-ord("0")),end="")
          else:
            print(table[x][y],end="")
        else:
          print("\u00b7",end="")
      
      print("│")
      if x<8:
        if x%3==2:
          print("├─────┼─────┼─────┤")
    print("└─────┴─────┴─────┘")

  @staticmethod
  def loadTable(fn):
    t=[]
    f=open(fn)
    for line in f:
      l=re.sub("[^0123456789.]","",line.strip('\n'))
      l=l.replace("0",".")
      if len(l) > 0:
        t.append(list(l))
    return t
 
if __name__ == "__main__":
  import sys
  t=Solver.loadTable(sys.argv[1])
  Solver.dumpTable(t)
  print()
  s=Solver()
  #print(s.validate(t))
  #exit(1)
  r,solution = Solver.solve(t)
  if len(solution)>0:
    step=1
    for x in solution:
      print("Step %s" % step)
      step=step+1
      Solver.dumpTable(x[0],t,x[1][0],x[1][1])
      print()
    Solver.dumpTable(r,t)
  else:
    print("There is no solution")
