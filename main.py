"""
Author: Gerod Dunn (gerod.dunn.ie3@gmail.com)
Date of original code: March 15, 2021
Date of rework code: Feb 17,2024
Description: The code was writen to demonstrate the diffraction of electrons through crystal structures and observe how the kinetic energy of an electron is
             dependent on the wavelength of the electron as well as run the appropriate calculations to draw conclusions.
"""

import pandas as pd                     # importing pandas for data frames, done as pd so as to not need to write as much
import numpy as np                      # redefining numpy features as np so as to not need to write as much
import matplotlib.pyplot as plt         # redifined for less verbos graphing
from scipy import stats                 # getting science statistics library
import statistics                       # mainly for linear regression
import csv                              # library for importing csv files

df=pd.read_csv('Teletron.csv')          # opening and reading Teletron.csv file
df2=pd.read_csv('Welch.csv')            # opening and reading Welch.cdv file


"""
function name: first_graph
function parameters: 3 lists are inputed (outer, inner, and volts) for the Teletron
function use: The function displays a graph of 2 sets of data with linear regression lines for each graph.
function return: The return type can be considerd void as there is no return statement.

function description: The function takes in 3 lists, places the outer distances and inner distances against volts on the same graph. The function then sets the
                      slope, y-intercept, r value, confidence value, and the standard deviation for the linear regression for the outter and inner lists distances
                      against the volts. The function then has two nested functions for both the outter and inner distances that return y values for y values for
                      the lines of best fit. The function then creates 2 models for the inner and outer functions and plots them. The function creates error bars
                      for the x values and displays the overlayed graphs.
                      
techniques/notes about function: The main technique that was used is nested functions and the map of the functions creates continuous line for the display that
                                 can be compared to the experemental data,rather than a series of discrete points.
"""
def first_graph(outer_diameter,inner_diameter,volts):
    plt.scatter(volts,outer_diameter,color='k')  # creates a scatter plot where outer diameter for teletron is graphed against volts
    plt.scatter(volts,inner_diameter,color='k')  # creates a scatter plot where inner diameter for teletron is graphed against volts
    slopeo, intercepto, ro, po, std_erro = stats.linregress(volts, outer_diameter) # linear regression of outer diameter against volts
    slopei, intercepti, ri, pi, std_erri = stats.linregress(volts, inner_diameter) # linear regression of inner diameter against volts

    """
    function name: myfunco
    function parameters: number x (can only be a number)
    function use: To create outputs based on the expiremental inputs and the linear regression of the slope and intercept of the outer measurments
    function description: The function takes in a value of x and multiplies it by the slope and adds the intercept to return a predicted y-value
    """
    def myfunco(x):
      return slopeo * x + intercepto

    """
    function name: myfunci
    function parameters: number x (can only be a number)
    function use: To create outputs based on the expiremental inputs and the linear regression of the slope and intercept of the inner measurments
    function description: The function takes in a value of x and multiplies it by the slope and adds the intercept to return a predicted y-value
    """
    def myfunci(x):
        return slopei*x+intercepti

    mymodelo=list(map(myfunco,volts)) # creates continious line of best fit for outer measurements
    mymodeli=list(map(myfunci,volts)) # creates continious line of best fit for inner measurements

    plt.plot(volts,mymodelo,color='b',label='outer best fitline: y=21.304x-.027') # plots line of best fit for outer measurements
    plt.plot(volts,mymodeli,color='r',label='inner best fitline: y=11.66x-.003')  # plots line of best fit for inner measurements

    plt.title("Electron Diffraction: Inner and Outer Rings\nsize of diffraction ring with respect to electron energy",loc='center') #graph title
    plt.xlabel("Volts^-1/2 (V^-1/2)")  # x-axis label
    plt.ylabel("Diameter/length (cm)") # y-axis label
    plt.errorbar(volts, mymodelo, xerr=.001, yerr=.05, errorevery=1, markeredgewidth=1,color='b') # creates error bars for outer diameter
    plt.errorbar(volts, mymodeli, xerr=.001, yerr=.05, errorevery=1, markeredgewidth=1,color='r') # creates error bars for inner diameter 
    plt.legend() # legend for graph
    plt.show()   # show graph

    
"""
function name: second_graph
function parameters: outer_diameter,inner_diameter,volts
function use: display a graph of fhkl diameter vs the inverse root of volts/energy passing through the crystal plane.
function description: The function takes in 3 variables. The function creates a empty list. The function alters the values in the outer diameter list, based on
                      instructions received in class on how to alter. The altered values are then added to the list. The list is converted into a numpy array.
                      A slope, an intercept, standard deviation, confidence value, and r value are calculated using the stats.linregress method against volts and the
                      list.
function return: float of a slope
important techniques or notes about function: the function uses nested functions to model the outputs of an input
"""
def second_graph(outer_diameter,inner_diameter,volts):
    final_y=[]                                       # list for returning values at the end for analysis
    for i in range(len(outer_diameter)):
        final_y.append((.5*3**.5)*outer_diameter[i]) # the fkhl for inner is root 3 over 2

    finally_y=np.array(final_y) # turning list into an array

    slopef, interceptf, rf, pf, std_errf = stats.linregress(volts, finally_y) # statistical analysis of the functions

    """
    function name: myfuncf
    function parameters: x as a float
    function use: to return the expected outputs based on an input
    function description: returns outputs based on an input for a model that has been defined
    important techniques or notes about function: function nesting
    """
    def myfuncf(x):
      return slopef * x + interceptf
    mymodelf=list(map(myfuncf,volts)) # creates continious line for a function of the best fit line for volts against inputs

    plt.plot(volts,mymodelf,'r--',label='y=18.45x-.0197') # plot of volts vs the model
    plt.scatter(volts,final_y,color='b')                  # scatter plot on line to show the original data and be able to compare obtained data vs expected data
    plt.errorbar(volts, final_y, xerr=0.001, yerr=np.abs(interceptf), errorevery=1, markeredgewidth=1,fmt='o')# error bars, correcting if error is negative
    plt.title("Electron Diffraction:\nNormalized for Separation Length and Crystal Plane")                    # plot title
    plt.xlabel("Volts-1/2 (V-1/2)")         # x-axis label
    plt.ylabel("fhkl*Diameter/Length (cm)") # y-axis label
    plt.legend()  # legend for second graph
    plt.show()    # show graph
    return slopef # return the slope for further calculation in the lab

"""
function name: main
function parameters: none
function use: main area of statistical calculations, displays data analysis results
function description: The function creates data frames from the files that were read in at the top of the file. The function then converts the data to the desired units, such as meters to centimeters. The function then combines data
                      of similar use, such as inner measurements from the Teletron and inner measuements of the welch, into a list which is then converted into a numpy array. The function then takes square roots the voltage and
                      inverts the voltage. These 'new' voltages will be passed to other functions in the program as x-values. The function will then run analysis based on the 'smearing' or systematic error that was done, ie the
                      minimum threshold of the measurements that were taken, as well as the results of the graphs.
important techniques or notes about function: The function uses data frames and statistical analysis with flow control
"""
def main():

    # data frames for Teletron
    v_tele=df["Voltage (V)"].values
    Do_tele=df["Douter (m)"].values
    Di_tele=df["Dinner (m)"].values

    teletron_voltage=np.array(v_tele)
    teletron_Douter=np.array(Do_tele)
    teletron_Dinner=np.array(Di_tele)

    # data frames for Welch
    v_welch=df2["Voltage (V)"].values
    Do_welch=df2["Douter (m)"].values
    Di_welch=df2["Dinner (m)"].values

    welch_voltage=np.array(v_welch)
    welch_Douter=np.array(Do_welch)
    welch_Dinner=np.array(Di_welch)

    # some information that was given to us outside the lab
        # the fkhl for outer is 1/2
        # the fkhl for inner is root 3 over 2

    # convert all D from m to cm
    list_outter=[] # list to hold all outer values
    for i in range(len(welch_Douter)):
        list_outter.append((100/18.16)*welch_Douter[i])   # list for all outer Welch diameter measurements
    for i in range(len(teletron_Douter)):
        list_outter.append((100/13.5)*teletron_Douter[i]) # list for all outer Teletron diameter measurements
    
    # convert all D from m to cm
    list_inner=[] # list to hold all inner values
    for i in range(len(welch_Dinner)):
        list_inner.append((100/18.16)*welch_Dinner[i])
    for i in range(len(teletron_Dinner)):
        list_inner.append((100/13.5)*teletron_Dinner[i])

    volts=[] # list for volts
    for i in range(len(welch_voltage)):
        volts.append(welch_voltage[i]**(-.5))    # add inverted square root of voltage from Welch
    for i in range(len(teletron_voltage)):
        volts.append(teletron_voltage[i]**(-.5)) # add inverted square root of voltage from Teletron

    outer_y=np.array(list_outter) # make outer list into an array
    inner_y=np.array(list_inner)  # make inner list into an array
    voltages=np.array(volts)      # make volts list into an array

    first_graph(outer_y,inner_y,voltages)         # display first graph
    slopef=second_graph(outer_y,inner_y,voltages) # display second graph and return the slope

    h=6.582119569e-16 # Plank constant in eVs terms
    m=9.10938356E-31  # mass of an electron in kg
    c=1.60217662E-19  # charge of an electron in coulombs
    f=.5*3**.5        # norm of miller indicies

    a=(((4*h**2))/(((f*2*m*c)**.5)*1*slopef**2)) # lattice planner constant
    print("The plannar constant is:",a)          # display planner constant

    teletron_a_list_outer=[] # planner constant for the outer diameter for the teletron list per measurement
    teletron_a_list_inner=[] # planner constant for the inner diameter for the teletron list per measurement
    welch_a_list_inner=[] # planner constant for the inner diameter for the welch list per measurement
    welch_a_list_outer=[] # planner constant for the outer diameter for the welch list per measurement

    for i in range(len(teletron_Douter)):
        teletron_a_list_outer.append((2*13.5*h)/(teletron_Douter[i]*2*f*(m*c)**.5)) # planner constant for the outer diameter for the teletron list per measurement
    for i in range(len(teletron_Dinner)):
        teletron_a_list_inner.append((2*13.5*h)/(teletron_Dinner[i]*.5*(m*c)**.5))  # planner constant for the inner diameter for the teletron list per measurement
    for i in range(len(welch_Dinner)):
        welch_a_list_inner.append((2*18.6*h)/(welch_Dinner[i]*.5*(m*c)**.5))  # planner constant for the inner diameter for the welch list per measurement
    for i in range(len(welch_Douter)):
        welch_a_list_outer.append((2*18.6*h)/(welch_Douter[i]*2*f*(m*c)**.5)) # planner constant for the outer diameter for the welch list per measurement

    # all planner constants per measurement
    a_list=[]
    for i in range(len(teletron_a_list_outer)):
        a_list.append(teletron_a_list_outer[i])
    for i in range(len(teletron_Dinner)):
        a_list.append(teletron_a_list_inner[i])
    for i in range(len(welch_a_list_outer)):
        a_list.append(welch_a_list_outer[i])
    for i in range(len(welch_a_list_inner)):
        a_list.append(welch_a_list_inner[i])
        
    print("teleout",teletron_a_list_outer) # displays the planner constant list for the outer diameter measuements of the teletron
    print("teleout mean",statistics.mean(teletron_a_list_outer)) # displays the mean of the planner constant list for the outer diameter measuements of the teletron
    print("teleout std",statistics.stdev(teletron_a_list_outer)) # displays the standard deviation of the planner constant list for the outer diameter measuements of the teletron
    print("std",statistics.stdev(a_list)) # standard deviation of standard deviation, not needed but I thought it would be fun to do at the time I originally wrote this code
    print("mean",statistics.mean(a_list)) # mean of mean, not needed but I thought it would be fun to do at the time I originally wrote this code

    # te=-1*(a-statistics.mean(a_list))/a # not sure what this is, but I'm keeping it in incase I need it later or figure out what I did and why later

    dD=.01 # lowest threshold of concentric circle's diameter
    dL=.1  # lowest threshold for distance from viewing screen to L
    dV=100 # lowest threshold for measurements for volts

    teletron_outer_uncertainty=[]
    teletron_Dinner_uncertainty=[]
    welch_Douter_uncertainty=[]
    welch_Dinner_uncertainty=[]
    
    # teletron outer and inner uncertainty
    for i in range(len(teletron_Douter)):
        teletron_outer_uncertainty.append((dL*voltages[i]/teletron_Douter[i])**2+((-13.5*voltages[i]/((teletron_Douter[i]**2)))*dD)**2+(((13.5*voltages[i]**(3/2))/teletron_Douter[i])*dV)**2)
    for i in range(len(teletron_Dinner)): 
        teletron_Dinner_uncertainty.append((dL*voltages[i]/teletron_Dinner[i])**2+((-13.5*voltages[i]/((teletron_Dinner[i]**2)))*dD)**2+(((13.5*voltages[i]**(3/2))/teletron_Dinner[i])*dV)**2)

    # welch outer and inner uncertainty
    for i in range(len(welch_Douter)):
        welch_Douter_uncertainty.append((dL*voltages[i]/welch_Douter[i])**2+((-18.16*voltages[i]/((welch_Douter[i]**2)))*dD)**2+(((18.16*voltages[i]**(3/2))/welch_Douter[i])*dV)**2)
    for i in range(len(welch_Dinner)):
        welch_Dinner_uncertainty.append((dL*voltages[i]/welch_Dinner[i])**2+((-18.16*voltages[i]/((welch_Dinner[i]**2)))*dD)**2+(((18.16*voltages[i]**(3/2))/welch_Dinner[i])*dV)**2)

    print("The systematic error is", statistics.stdev(teletron_outer_uncertainty)/statistics.mean(teletron_outer_uncertainty)) # displays systematic error

if __name__=="__main__":
    main()






