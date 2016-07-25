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


def singlevar_rss_calc(func, dataset):

    s = 0
    for i in range(0, len(dataset[0][0])):
    
        s += (dataset[0][1][i] - func(dataset[0][0][i]))**2
        
    return s

def singlevar_mean_calc(dataset):

    s = 0
    for i in range(0, len(dataset[0][0])):
        s += (dataset[0][1][i])
		
    return s/(int(len(dataset[0][0])))
	
def singlevar_tss_calc(func, dataset):

    s = 0
    for i in range(0, len(dataset[0][0])):
    
        s += (dataset[0][1][i] - singlevar_mean_calc(dataset))**2
        
    return s
	
	
def singlevar_ess_calc(func, dataset):

    return singlevar_tss_calc(func, dataset)-singlevar_rss_calc(func, dataset)
	

def singlevar_cod_calc(func, dataset):

    return 1-(singlevar_rss_calc(func, dataset)/singlevar_tss_calc(func, dataset))