#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import copy

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
  def solve(table):
    t = copy.deepcopy(table)
    Solver.__solve(t)
    return t

  @staticmethod
  def __solve(table,cell=0):
    if cell>80:
      return True
    x = cell//9
    y = cell%9
    if table[x][y] != ".":
      return Solver.__solve(table,cell+1)
    for tryVal in range(1,10):
      table[x][y] = str(tryVal)
      if Solver.isValid(table,x,y):
#        Solver.dumpTable(table)
#        print()
        ret = Solver.__solve(table,cell+1)
        if ret:
          return True

    table[x][y]="."
    return False

  @staticmethod
  def dumpTable(table):
    print  ("┏━┯━┯━┳━┯━┯━┳━┯━┯━┓")
    for x in range(len(table)):
      for y in range(len(table[x])):
        if y%3 == 0:
          print("┃",end="")
        else:
          print("│",end="")
        if table[x][y] != ".":
          print(table[x][y],end="")
        else:
          print(" ",end="")
      
      print("┃")
      if x<8:
        if x%3==2:
          print("┣━┿━┿━╋━┿━┿━╋━┿━┿━┫")
        else:
          print("┠─┼─┼─╂─┼─┼─╂─┼─┼─┨")
    print("┗━┷━┷━┻━┷━┷━┻━┷━┷━┛")

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
  r = s.solve(t)
  Solver.dumpTable(r)

