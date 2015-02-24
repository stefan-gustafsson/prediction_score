
# coding: utf-8

# In[125]:

"""
Program to calculate 5-year risk of mortality.

    Parameters
    ----------
    1. The name of the file that contains the results of the questionnaire. 
       Should be in the same folder of the program.
    
    Data Needed (All data should be in the same folder of the program)
    ----------
    1. CoefM.txt (coefficients for males)
    2. CoefF.txt (coefficients for females)
    3. wwMage.csv (weights for males)
    4. wwFage.csv (weights for females)
    5. MM095.csv (5-year survival probabilities from lifetables, males)
    6. FF095.csv (5-year survival probabilities from lifetables, females)

    Returns
    -------
    1. The predicted risk.

"""

import numpy as np
import math as mt
import sys
import os.path

def skip_d(d):
    '''
    This function replace the 'skip' value with the expected value 
    and delete the remaining 'skip' values. 
    Also delete the 'Sex' variable, which is not useful anymore.
    '''
    L1=[]
    L2=[]
    for x in d:
        if x[0] == 'Sex':
            continue
            
        elif x[0] in ['f.6141.0.l1','f.6141.0.l2','f.6141.0.l3','f.6141.0.l4','f.6141.0.l5','f.6141.0.l6','f.6141.0.l7','f.6141.0.l8'] and x[1]=='skip':
            if d[1,1] == "Male":
                x[1] = 'Live alone'
                x[0] = x[0]
            else:
                continue
    
        elif x[0] == 'f.1249.0.0' and x[1] == 'skip':
            x[1] = "I'm a smoker"
            x[0] = x[0]
    
        elif x[1] == 'skip':
            continue
        
        else:
            x[1] = x[1]
            x[0] = x[0]
        L1.append(x[1])
        L2.append(x[0])

    d=np.column_stack((L2,L1))
    return d

def add_interaction(interact_var,d):
    '''
    Function to create variables that interact with age
    and assign the right value
    '''
    for i in interact_var:
        newi = i.split (".", 2)[1] 
        newvar = 'f.age:'+newi
        newpar = d[d[:,0] == i,1]
        for k in newpar:
            newx = np.array((newvar,k))
            d = np.vstack((d,newx))
    return d

def deal_with_zeros(d):
    '''
    This function replace the '0' with the right values making the data structure 
    compatible with the functions
    '''
    L1=[]
    L2=[]
    for x in d:
        if x[1] == '0':
            continue

        elif x[0][len(x[0])-2:len(x[0])-1] == 'l':
            x[1] = x[1]
            x[0] = x[0][0:len(x[0])-3]

        else:
            x[1] = x[1]
            x[0] = x[0]
        L1.append(x[1])
        L2.append(x[0])

    d=np.column_stack((L2,L1))
    return d

def calculate_f709(d):
    '''
    This function calculate the right string interval for the variable f.709:
    number of people in the household
    '''
    if d[d[:,0] == ['f.709.0.0'],1] == '[1,2]' or d[d[:,0] == ['f.709.0.0'],1] == '(2,4]' or d[d[:,0] == ['f.709.0.0'],1] == '(4,100]':
        return d
    else:
        if np.int_(d[d[:,0] == ['f.709.0.0'],1]) < 3:
            d[d[:,0] == ['f.709.0.0'],1] = ['[1,2]']
        elif np.int_(d[d[:,0] == ['f.709.0.0'],1]) < 5:
            d[d[:,0] == ['f.709.0.0'],1] = ['(2,4]']
        else:
            d[d[:,0] == ['f.709.0.0'],1] = ['(4,100]']
        return d 

def calculate_f2734(d):
    '''
    This function calculate the right string interval for the variable f.2734:
    number of children
    '''
    if d[d[:,0] == ['f.2734.0.0'],1] == '[0,1]' or d[d[:,0] == ['f.2734.0.0'],1] == '(1,2]' or d[d[:,0] == ['f.2734.0.0'],1] == '(2,4]' or d[d[:,0] == ['f.2734.0.0'],1] == '(4,22]':
        return d
    else:
        if np.int_(d[d[:,0] == ['f.2734.0.0'],1]) < 2:
            d[d[:,0] == ['f.2734.0.0'],1] = ['[0,1]']
        elif np.int_(d[d[:,0] == ['f.2734.0.0'],1]) < 3:
            d[d[:,0] == ['f.2734.0.0'],1] = ['(1,2]']
        elif np.int_(d[d[:,0] == ['f.2734.0.0'],1]) < 5:
            d[d[:,0] == ['f.2734.0.0'],1] = ['(2,4]']
        else:
            d[d[:,0] == ['f.2734.0.0'],1] = ['(4,22]']
        return d 

'''
Following three functions are used to extract
the right values from the file containing coefficients
'''

def reform_array_par(name_var,coef):
    newarray=coef.view(np.recarray)
    return newarray.f1[newarray.f0 == name_var]

def reform_array_coef(name_var,coef):
    newarray=coef.view(np.recarray)
    return newarray.f2[newarray.f0 == name_var]

def reform_array_mean(name_var,coef):
    newarray=coef.view(np.recarray)
    return newarray.f3[newarray.f0 == name_var]

def calculate_lp(pars,means,coefs,name_var,d,age):
    '''
    Function to calculate the linear predictor for each variable
    '''
    name_par = d[d[:,0] == name_var,1]
    lp = 0
    for i in enumerate(pars):
        j = 0
        for k in name_par:
            if i[1] == k:
                j = j+1
        if j == 0:
            tind = i[0]
            t = (0-means[tind])*coefs[tind] 
        else:
            if name_var[0:5] == 'f.age': #If age interaction then use formula (age-mean) * coef
                tind = i[0]
                t = (age-means[tind])*coefs[tind]  
            else:
                tind = i[0]
                t = (1-means[tind])*coefs[tind]  
        lp += t
    return lp

def age_lp(age,coef):
    
    '''
    Function to calculate the linear predictor for age
    '''
    return (np.int_(age)-coef[0,][3])*coef[0,][2]



class Predscore_final(object):
    
    def __init__ (self, d, age, sex, directory):
        self.d = d
        self.age=age
        self.sex=sex
        self.directory=directory 
        
    def sex_load(self):
        '''
        Initial data process, output a clean dataset that is used to calculate the linear predictors
        '''
        if  self.sex == 'Male':
            self.coef = np.loadtxt(fname=self.directory +'/coefM.txt', delimiter='\t',dtype={'names': ('f0', 'f1', 'f2','f3'),'formats': ('S40', 'S100', '<f8','<f8')}, usecols=(0,1,2,3))
            self.basehaz=0.0127703  
            self.wwage = np.loadtxt(fname=self.directory + '/wwMage.csv', delimiter=',', dtype='<f8')
            self.S095 = np.loadtxt(fname=self.directory + '/MM095.csv', delimiter=',', dtype='<f8')
            # Determine which variable are interacting with age
            interact_var = ['f.709.0.0','f.6141.0','f.924.0.0','f.2443.0.0','f.2453.0.0','f.6150.0','f.6146.0']
            # These functions set the data in the right format
            self.d=skip_d(self.d)
            self.d=calculate_f709(self.d)   
            self.d=deal_with_zeros(self.d)
            self.d=add_interaction(interact_var,self.d)
        else:    
            self.coef = np.loadtxt(fname=self.directory +'/coefF.txt', delimiter='\t',dtype={'names': ('f0', 'f1', 'f2','f3'),'formats': ('S40', 'S100', '<f8','<f8')}, usecols=(0,1,2,3))
            self.basehaz=0.007218876
            self.wwage = np.loadtxt(fname=self.directory + '/wwFage.csv', delimiter=',', dtype='<f8')
            self.S095 = np.loadtxt(fname=self.directory + '/FF095.csv', delimiter=',', dtype='<f8')
            # Determine which variable are interacting with age
            interact_var = ['f.2453.0.0','f.6146.0']
            # These functions set the data in the right format
            self.d=skip_d(self.d)
            self.d=calculate_f2734(self.d)
            self.d=deal_with_zeros(self.d)
            self.d=add_interaction(interact_var,self.d)
        return self.d     
       
    def calculate_risk(self):
        '''
        Calculate the individual risk and
        report the largest and smallest linear predictor beside age and age*var interaction
        '''
        lp_risk=0
        maxrf = 0
        minrf = 0
        maxrfidx = []
        minrfidx = []
        for i in np.unique(self.d[:,0]):
            if i =='age':
                lp = age_lp(self.age,self.coef)
            else:
                coefs=reform_array_coef(i, self.coef)
                means=reform_array_mean(i, self.coef)
                pars=reform_array_par(i, self.coef)
                lp=calculate_lp(pars,means,coefs,i,self.d,self.age)
            if lp > maxrf and i != 'age' and i[0:5] != 'f.age' : # beside age and age interaction variables
                maxrf = lp
                maxrfidx = i
            if lp < minrf and i != 'age' and i[0:5] != 'f.age' : # beside age and age interaction variables
                minrf = lp
                minrfidx = i    
            lp_risk += lp     
        w = self.wwage[self.wwage[:,0] == self.age ,1] # Obtain the right weights
        MMt = mt.exp(-self.basehaz * w) # Weight the baseline hazard
        self.predscore = 1-(MMt**mt.exp(lp_risk)) #
        return (self.predscore,maxrfidx,minrfidx)
    
    
    def assertion_data(self):
        assert len(self.d) > 1, 'ERROR'
        assert self.d[0,0] == 'age' , 'ERROR'
        assert np.array_equal(np.unique(self.d[:,0]),np.unique(self.coef['f0'])), 'ERROR'
        
    def bioage(self):
        '''
        Find closest value to values in array:
        Used to find the biological age
        '''
        idx = (np.abs(self.S095[:,1]-(1-self.predscore))).argmin()
        return self.S095[idx,0] 
 
def show ():
    ''' 
    Function that reads the data and the required files;
    run the functions to obtain the predicted score and performs checks
    '''
    
    directory = os.getcwd()
    #directory = '/Users/AndreaGanna/Documents/Work/Phd_KI/UKbio_mortality/Pgm/test_python'
    assert os.path.isdir(directory), 'ERROR'
    
    fname = directory + '/' + sys.argv[1]
    #fname = directory + '/answer-female'
    assert os.path.isfile(fname), 'File does not exist'
    
    d = np.loadtxt(fname=fname, delimiter='\t',dtype='S100') # Read external file containing questionnaire results
    age=np.int_(d[d[:,0] == ['age'],1][0])
    assert issubclass(type(age), np.integer) and (age > 39 and age < 71), 'Wrong format for age or age out of age-limits'
    
    sex=np.str_(d[d[:,0] == ['Sex'],1][0])
    assert sex == 'Male' or sex == 'Female', 'ERROR'
  
    fun_to_run = Predscore_final(d,age,sex,directory)
    
    fun_to_run.sex_load()
    fun_to_run.assertion_data()
    
    predscore=fun_to_run.calculate_risk()[0] 
    assert predscore < 1 and predscore > 0, 'ERROR'
    
    maxlp=fun_to_run.calculate_risk()[1] 
    minlp=fun_to_run.calculate_risk()[2]
    
    bioage=fun_to_run.bioage()
    assert bioage > 14 and bioage < 96, 'ERROR'
    
    risk = np.int_(predscore*100)
    invrisk = 100- risk
    if risk < 1:
        riskout = "less than 1"
        invriskout = "more than 99"
    else:
        riskout=risk
        invriskout=invrisk
    print str(age) + ';' + sex + ';' + str(np.int_(bioage)) + ';' + str(predscore) + ';' + maxlp + ';' + minlp+ ';' + str(riskout) + ';' + str(invriskout)

show()    


# In[ ]:



