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


#!/usr/bin/env python

import ranengine
from ranengine.funcparse import parse_singlevar_function
from ranengine.residualcalc import *
from ranengine.csvparse import *
from numpy import linspace


try:
    import tkinter
    from tkinter import *
    from tkinter import ttk
    from tkinter.scrolledtext import *

except:
    sys.exit("Python 3 is required!")


import matplotlib
from matplotlib import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.filedialog import askopenfilename

matplotlib.use('TkAgg')


class MainGUI:

    def __init__(self):

        self.file_name = None
        
        self.pad = 10
        self.inpad = 5
        
        self.__root = Tk()
        self.__root.wm_title("MyEasyModel v0.0.1 ALPHA by Arseny Denisov, aka NullBytes0x00")
        self.__root.resizable(0, 0)
        
        self.__LabelFrame1 = ttk.LabelFrame(self.__root, text = "Settings", padding = (self.inpad, self.inpad))
        self.__LabelFrame1.grid(row = 0, column = 0, padx = self.pad, pady = self.pad, sticky = N + W)
        
        self.__Label1 = Label(self.__LabelFrame1, text = "Function")
        self.__Label1.grid(row = 0, column = 0, sticky = N + W)        
        
        self.__Entry1 = Entry(self.__LabelFrame1)
        self.__Entry1.grid(row = 1, column = 0, sticky = N + W)        

        self.__Label2 = Label(self.__LabelFrame1, text = "File not loaded", fg="red")
        self.__Label2.grid(row = 2, column = 0, sticky = N + W)  
        
        self.__LabelFrame2 = ttk.LabelFrame(self.__root, text = "Results", padding = (self.inpad, self.inpad))
        self.__LabelFrame2.grid(row = 1, column = 0, padx = self.pad, pady = self.pad, sticky = S + W)        
        self.__LabelFrame2.grid_columnconfigure(0, weight=1)

        self.__ScrolledText1 = ScrolledText(self.__LabelFrame2, height = 10, width = 20)      
        self.__ScrolledText1.config(state = DISABLED)
        self.__ScrolledText1.pack(fill=BOTH, expand=1)


        def copy_results():
                self.__root.clipboard_clear()
                self.__root.clipboard_append(self.__ScrolledText1.get(1.0, END))

        self.__Button0 = Button(self.__LabelFrame2, text = "Copy the result", command = copy_results)        
        self.__Button0.pack(expand=1)
        

        self.f = None
        self.a = None
        
        def reset_plot():
            self.f = Figure(figsize=(4, 3), dpi=100)
            self.f.set_facecolor('white')
            self.a = self.f.add_subplot(111, axisbg='0.98')           
        
        reset_plot()
        
        self.x_last_element = None
        self.x_first_element = None
        
        def load_csv(refresh):
            
            file_name = None
            
            if refresh is not True:
                file_name = askopenfilename()
            
            elif (self.file_name is not None) and (file_name != ""):
                file_name = self.file_name
			
            if (file_name is not None) and (file_name != ""):
            
                try:
					
                    reset_plot()
					
                    scatter_data = csvdata(file_name)
                    self.file_name = file_name

                    self.a.scatter(scatter_data[0][0], scatter_data[0][1])
                    x_axis = scatter_data[0][0]
                    self.x_last_element = x_axis[len(x_axis)-1]
                    self.x_first_element = x_axis[0]
					
                    self.a.set_xlabel(scatter_data[1])
                    self.a.set_ylabel(scatter_data[2])
                    self.f.tight_layout()

                    canvas = FigureCanvasTkAgg(self.f, master=self.__root)
                    canvas.get_tk_widget().grid(row = 0, column = 1, sticky = N+W, padx = self.pad, pady = self.pad, rowspan=2) 
                    canvas.show()
					
                    self.__Label2.configure(text = "File loaded", fg = "green")
					
                except:
                    raise

		
        self.__LabelFrame3 = ttk.LabelFrame(self.__root, text = "Visualization", padding = (self.inpad, self.inpad))
        self.__LabelFrame3.grid(row = 0, column = 1, sticky = N+W, padx = self.pad, pady = self.pad, rowspan=2) 		
		
        canvas = FigureCanvasTkAgg(self.f, master=self.__LabelFrame3)
        canvas.get_tk_widget().pack() 
        canvas.show()
		
        v = StringVar()
        self.__Label3 = Label(self.__LabelFrame3, textvariable = v, fg="red", font=("Calibri", "15"))
        self.__Label3.pack()
  		
        v.set("This model explains ..% of the variations in the data.")

		
        self.lines = None
        
        def plot_funct():
            
            try:

                expr_str = str(self.__Entry1.get())
                if expr_str and (self.file_name is not None):

        
                    if (self.lines is not None):
                        self.lines.pop(0).remove()
						
                    load_csv(True)
					
                    l = linspace(self.x_first_element, self.x_last_element)
                    expr = parse_singlevar_function(expr_str)
                    pl = self.a.plot(l, expr(l))
        
                    canvas = FigureCanvasTkAgg(self.f, master=self.__root)
                    canvas.get_tk_widget().grid(row = 0, column = 1, sticky = N+W, padx = self.pad, pady = self.pad, rowspan=2)
                    canvas.show()

                    self.__ScrolledText1.config(state = NORMAL)

                    rsq = singlevar_cod_calc(expr, csvdata(self.file_name))
                    self.__ScrolledText1.insert(INSERT, "Mean = " + str(singlevar_mean_calc(csvdata(self.file_name))) + "\n")
                    self.__ScrolledText1.insert(INSERT, "R Squared = " + str(rsq) + "\n")
                    self.__ScrolledText1.insert(INSERT, "RSS = " + str(singlevar_rss_calc(expr, csvdata(self.file_name))) + "\n")					
                    self.__ScrolledText1.insert(INSERT, "TSS = " + str(singlevar_tss_calc(expr, csvdata(self.file_name))) + "\n")
                    self.__ScrolledText1.insert(INSERT, "ESS = " + str(singlevar_ess_calc(expr, csvdata(self.file_name))) + "\n")
					
                    v.set("This model explains " + str(round(rsq*100, 2)) + "% of the data.")
					
                    if (rsq > 0.25) and (rsq < 0.5):
                        self.__Label3.config(fg = "yellow")
                    elif (rsq > 0.5) and (rsq < 0.75):
                        self.__Label3.config(fg = "yellow green")
                    elif (rsq > 0.75) and (rsq <= 100):
                        self.__Label3.config(fg = "green")
                    else:
                        self.__Label3.config(fg = "red")
					
                    self.__root.update()
					
                    self.__ScrolledText1.config(state = DISABLED)

                    self.lines = pl

            except:
                raise
        
        self.__Button1 = Button(self.__LabelFrame1, text = "Plot", command = plot_funct)        
        self.__Button1.grid(row = 1, column = 1, padx=(2, 0), sticky = N + W)        
        
        self.__Button2 = Button(self.__LabelFrame1, text = "Import a file", command = lambda: load_csv(False))        
        self.__Button2.grid(row = 3, column = 0, sticky = N + W)         
        

        mainloop()


if __name__ == "__main__":
    gclass = MainGUI()