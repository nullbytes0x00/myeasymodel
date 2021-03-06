"""
MyEasyModel - Python-based non-linear regression analysis and curve fitting software
Copyright (C) 2016  Arseny Denisov


This file is part of MyEasyModel.

MyEasyModel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MyEasyModel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with MyEasyModel.  If not, see <http://www.gnu.org/licenses/>.

"""


import sympy
from sympy import *
from sympy.abc import x

def parse_singlevar_function(text):
	
    if not ("x" in text):
        
        print("Please specify a singlevariable function of variable \"x\".\n")
        return False

    try:

        lb = lambdify(x, eval(text), modules=['numpy'])
        return lb

    except:

        print("Invalid function format.\n")
        raise
        return False
