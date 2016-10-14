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
          if table[x][y] == "0":
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

  @staticmethod
  def getConstraints():
    if Solver.constraints is None:
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
      Solver.constraints = c
    return Solver.constraints

  @staticmethod
  def isValidTable(table):
    for x in range(0,9):
      for y in range(0,9):
        for v in Solver.getConstraints()[(x,y)]:
          if not v(table):
            return False
    return True

  @staticmethod
  def isComplete(table):
    for x in range(0,9):
      for y in range(0,9):
        if table[x][y] == "0":
          return False
    return True
 
  @staticmethod
  def isValid(table,x,y):
    for v in Solver.getConstraints()[(x,y)]:
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
      if table[j][k] != "0":
        continue
      lvals = []
      for i in values:
        table[j][k]=i
        if Solver.isValid(table,j,k):
          t=t+1
          lvals.append(str(i))
          if t>=minVal:
            break
      table[j][k]="0"
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
        if table[j][k] != "0":
          continue
        v[(j,k)]=[]
        for i in range(1,10):
          table[j][k]=str(i)
          if Solver.isValid(table,j,k):
            v[(j,k)].append(str(i))
        table[j][k]="0"
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
    if table[x][y] != "0":
      return Solver.__solve(table,valids,Solver.getNextCell(table,valids),solution)
    for tryVal in order[1]:
      table[x][y] = tryVal
      solution.append((copy.deepcopy(table),(x,y)))
      ret = Solver.__solve(table,valids,Solver.getNextCell(table,valids),solution)
      if ret:
        return True

    table[x][y]="0"
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
        if table[x][y] != "0":
          if table[x][y] == start[x][y]:
            print(chr(ord(table[x][y])+ord("\N{MATHEMATICAL SANS-SERIF BOLD DIGIT ONE}")-ord("\N{DIGIT ONE}")),end="")
          elif x==j and y==k:
            print(chr(ord(table[x][y])+ord("\N{CIRCLED DIGIT ONE}")-ord("\N{DIGIT ONE}")),end="")
          else:
            print(table[x][y],end="")
        else:
          print("\N{MIDDLE DOT}",end="")
      
      print("│")
      if x<8:
        if x%3==2:
          print("├─────┼─────┼─────┤")
    print("└─────┴─────┴─────┘")

  @staticmethod
  def loadTable(f):
    t=[]
    for line in f:
      l=re.sub("[^.\\d\N{MIDDLE DOT}]","",line.strip('\n'))
      l=re.sub("[.\N{MIDDLE DOT}]","0",l)
      if len(l) > 0:
        t.append([ str(int(x)) for x in l ])
    return t
 
if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description="Solve sudoku")
  parser.add_argument("-s", "--steps",action='store_true',help="show solution steps")
  parser.add_argument("game",type=argparse.FileType('r'),nargs=1)
  options=parser.parse_args()

  t=Solver.loadTable(options.game[0])
  options.game[0].close()
  Solver.dumpTable(t)
  print()
  if Solver.isComplete(t):
    if Solver.isValidTable(t):
      print("Already solved")
    else:
      print("Invalid game")
  else:
    if Solver.isValidTable(t):
      #print(s.validate(t))
      #exit(1)
      r,solution = Solver.solve(t)
      if len(solution)>0:
        if (options.steps):
          step=1
          for x in solution:
            print("Step %s" % step)
            step=step+1
            Solver.dumpTable(x[0],t,x[1][0],x[1][1])
            print()
        Solver.dumpTable(r,t)
      else:
        print("There is no solution")
    else:
      print("Invalid game")
