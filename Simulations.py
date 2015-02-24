
# coding: utf-8

# In[311]:

import numpy as np

def generate_array(coef):
    '''
    Generate the array for the combination process using the coefficient file
    '''
    myarray = []
    for i in np.unique(coef[:,0]):
        a = coef[:,1][coef[:,0] == i]
        myarray.append(a)
    return myarray 
        
def cartesian(arrays,out=None):
    """
    Generate a cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """
    arrays = [np.asarray(x) for x in arrays]
  
    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype='S60')

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    print 'Countdown: Processing array number ' + str(len(arrays))
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]       
    return out

def checkingsF(out,listnames):
    '''
    Function that performs checking for females.
    It excludes array which contains combination that cannot be output of the questionnaire
    '''
    outclean=[]
    for n,i in enumerate(out):
        if (n % 100000) == 0:
            print 'Current iteration =' + str(n) + ' out of ' + str(len(out)) 
        if i[listnames == 'f.6146.0.l1'] == 'None of the above' and (i[listnames == 'f.6146.0.l2'] != '0' or i[listnames == 'f.6146.0.l3'] != '0' or i[listnames == 'f.6146.0.l4'] != '0'):
            continue
        elif i[listnames == 'f.6146.0.l1'] == '0' and i[listnames == 'f.6146.0.l2'] == '0' and i[listnames == 'f.6146.0.l3'] == '0' and i[listnames == 'f.6146.0.l4'] == '0':
            continue
        elif i[listnames == 'f.6145.0.l1'] == 'None of the above' and (i[listnames == 'f.6145.0.l2'] != '0' or i[listnames == 'f.6145.0.l3'] != '0' or i[listnames == 'f.6145.0.l4'] != '0'  or i[listnames == 'f.6145.0.l5'] != '0' or i[listnames == 'f.6145.0.l6'] != '0' or i[listnames == 'f.6145.0.l7'] != '0'):
            continue
        elif i[listnames == 'f.6145.0.l1'] == '0' and i[listnames == 'f.6145.0.l2'] == '0' and i[listnames == 'f.6145.0.l3'] == '0' and i[listnames == 'f.6145.0.l4'] == '0'  and i[listnames == 'f.6145.0.l5'] == '0' and i[listnames == 'f.6145.0.l6'] == '0' and i[listnames == 'f.6145.0.l7'] == '0':
            continue
        elif i[listnames == 'f.1239.0.0'] == 'Yes, on most or all days' and i[listnames == 'f.1249.0.0'] != "I'm a smoker":
            continue
        elif i[listnames == 'f.1249.0.0'] == "I'm a smoker" and i[listnames == 'f.1239.0.0'] != 'Yes, on most or all days':
            continue
        else:
            outclean.append(i)
    return outclean


def checkingsM(out,listnames):
    '''
    Function that performs checking for males.
    It excludes array which contains combination that cannot be output of the questionnaire
    '''
    outclean=[]
    for n,i in enumerate(out):
        if (n % 100000) == 0:
            print 'Current iteration =' + str(n) + ' out of ' + str(len(out)) 
        
        # f.6146
        if i[listnames == 'f.6146.0.l1'] == 'None of the above' and (i[listnames == 'f.6146.0.l2'] != '0' or i[listnames == 'f.6146.0.l3'] != '0' or i[listnames == 'f.6146.0.l4'] != '0'):
            continue
        elif i[listnames == 'f.6146.0.l1'] == '0' and i[listnames == 'f.6146.0.l2'] == '0' and i[listnames == 'f.6146.0.l3'] == '0' and i[listnames == 'f.6146.0.l4'] == '0':
            continue
        
        # f.6145
        elif i[listnames == 'f.6145.0.l1'] == 'None of the above' and (i[listnames == 'f.6145.0.l2'] != '0' or i[listnames == 'f.6145.0.l3'] != '0' or i[listnames == 'f.6145.0.l4'] != '0'  or i[listnames == 'f.6145.0.l5'] != '0' or i[listnames == 'f.6145.0.l6'] != '0' or i[listnames == 'f.6145.0.l7'] != '0'):
            continue
        elif i[listnames == 'f.6145.0.l1'] == '0' and i[listnames == 'f.6145.0.l2'] == '0' and i[listnames == 'f.6145.0.l3'] == '0' and i[listnames == 'f.6145.0.l4'] == '0'  and i[listnames == 'f.6145.0.l5'] == '0' and i[listnames == 'f.6145.0.l6'] == '0' and i[listnames == 'f.6145.0.l7'] == '0':
            continue
        
        # f.1239 and f.1249
        elif i[listnames == 'f.1239.0.0'] == 'Yes, on most or all days' and i[listnames == 'f.1249.0.0'] != "I'm a smoker":
            continue
        elif i[listnames == 'f.1249.0.0'] == "I'm a smoker" and i[listnames == 'f.1239.0.0'] != 'Yes, on most or all days':
            continue
        
        # f.6150
        elif i[listnames == 'f.6150.0.l1'] == 'None of the above' and (i[listnames == 'f.6150.0.l2'] != '0' or i[listnames == 'f.6150.0.l3'] != '0' or i[listnames == 'f.6150.0.l4'] != '0'):
            continue  
        elif i[listnames == 'f.6150.0.l1'] == '0' and i[listnames == 'f.6150.0.l2'] == '0' and i[listnames == 'f.6150.0.l3'] == '0' and i[listnames == 'f.6150.0.l4'] == '0':
            continue

            
        # f.6141 check that one at least one is 'live alone' all should be 'live alone'
        elif i[listnames == 'f.6141.0.l1'] == 'Live alone' and (i[listnames == 'f.6141.0.l2'] != 'Live alone' or i[listnames == 'f.6141.0.l3'] != 'Live alone' or i[listnames == 'f.6141.0.l4'] != 'Live alone' or i[listnames == 'f.6141.0.l5'] != 'Live alone' or i[listnames == 'f.6141.0.l6'] != 'Live alone' or i[listnames == 'f.6141.0.l7'] != 'Live alone' or i[listnames == 'f.6141.0.l8'] != 'Live alone'):
            continue
        elif i[listnames == 'f.6141.0.l2'] == 'Live alone' and (i[listnames == 'f.6141.0.l1'] != 'Live alone' or i[listnames == 'f.6141.0.l3'] != 'Live alone' or i[listnames == 'f.6141.0.l4'] != 'Live alone' or i[listnames == 'f.6141.0.l5'] != 'Live alone' or i[listnames == 'f.6141.0.l6'] != 'Live alone' or i[listnames == 'f.6141.0.l7'] != 'Live alone' or i[listnames == 'f.6141.0.l8'] != 'Live alone'):
            continue
        elif i[listnames == 'f.6141.0.l3'] == 'Live alone' and (i[listnames == 'f.6141.0.l2'] != 'Live alone' or i[listnames == 'f.6141.0.l1'] != 'Live alone' or i[listnames == 'f.6141.0.l4'] != 'Live alone' or i[listnames == 'f.6141.0.l5'] != 'Live alone' or i[listnames == 'f.6141.0.l6'] != 'Live alone' or i[listnames == 'f.6141.0.l7'] != 'Live alone' or i[listnames == 'f.6141.0.l8'] != 'Live alone'):
            continue
        elif i[listnames == 'f.6141.0.l4'] == 'Live alone' and (i[listnames == 'f.6141.0.l2'] != 'Live alone' or i[listnames == 'f.6141.0.l3'] != 'Live alone' or i[listnames == 'f.6141.0.l1'] != 'Live alone' or i[listnames == 'f.6141.0.l5'] != 'Live alone' or i[listnames == 'f.6141.0.l6'] != 'Live alone' or i[listnames == 'f.6141.0.l7'] != 'Live alone' or i[listnames == 'f.6141.0.l8'] != 'Live alone'):
            continue
        elif i[listnames == 'f.6141.0.l5'] == 'Live alone' and (i[listnames == 'f.6141.0.l2'] != 'Live alone' or i[listnames == 'f.6141.0.l3'] != 'Live alone' or i[listnames == 'f.6141.0.l4'] != 'Live alone' or i[listnames == 'f.6141.0.l1'] != 'Live alone' or i[listnames == 'f.6141.0.l6'] != 'Live alone' or i[listnames == 'f.6141.0.l7'] != 'Live alone' or i[listnames == 'f.6141.0.l8'] != 'Live alone'):
            continue
        elif i[listnames == 'f.6141.0.l6'] == 'Live alone' and (i[listnames == 'f.6141.0.l2'] != 'Live alone' or i[listnames == 'f.6141.0.l3'] != 'Live alone' or i[listnames == 'f.6141.0.l4'] != 'Live alone' or i[listnames == 'f.6141.0.l5'] != 'Live alone' or i[listnames == 'f.6141.0.l1'] != 'Live alone' or i[listnames == 'f.6141.0.l7'] != 'Live alone' or i[listnames == 'f.6141.0.l8'] != 'Live alone'):
            continue
        elif i[listnames == 'f.6141.0.l7'] == 'Live alone' and (i[listnames == 'f.6141.0.l2'] != 'Live alone' or i[listnames == 'f.6141.0.l3'] != 'Live alone' or i[listnames == 'f.6141.0.l4'] != 'Live alone' or i[listnames == 'f.6141.0.l5'] != 'Live alone' or i[listnames == 'f.6141.0.l6'] != 'Live alone' or i[listnames == 'f.6141.0.l1'] != 'Live alone' or i[listnames == 'f.6141.0.l8'] != 'Live alone'):
            continue
        elif i[listnames == 'f.6141.0.l8'] == 'Live alone' and (i[listnames == 'f.6141.0.l2'] != 'Live alone' or i[listnames == 'f.6141.0.l3'] != 'Live alone' or i[listnames == 'f.6141.0.l4'] != 'Live alone' or i[listnames == 'f.6141.0.l5'] != 'Live alone' or i[listnames == 'f.6141.0.l6'] != 'Live alone' or i[listnames == 'f.6141.0.l7'] != 'Live alone' or i[listnames == 'f.6141.0.l1'] != 'Live alone'):
            continue
        
        
        # f.6141 check that when all are 'live alone' then f.709 ==[1,2]
        elif i[listnames == 'f.6141.0.l1'] == 'Live alone' and i[listnames == 'f.6141.0.l2'] == 'Live alone' and i[listnames == 'f.6141.0.l3'] == 'Live alone' and i[listnames == 'f.6141.0.l4'] == 'Live alone' and i[listnames == 'f.6141.0.l5'] == 'Live alone' and i[listnames == 'f.6141.0.l6'] == 'Live alone' and i[listnames == 'f.6141.0.l7'] == 'Live alone' and i[listnames == 'f.6141.0.l8'] == 'Live alone' and i[listnames == 'f.709.0.0'] != '[1,2]':
            continue
        
        # when all f.6141 == 0 then wrong they should be live alone
        elif i[listnames == 'f.6141.0.l1'] == '0' and i[listnames == 'f.6141.0.l2'] == '0' and i[listnames == 'f.6141.0.l3'] == '0' and i[listnames == 'f.6141.0.l4'] == '0' and i[listnames == 'f.6141.0.l5'] == '0' and i[listnames == 'f.6141.0.l6'] == '0' and i[listnames == 'f.6141.0.l7'] == '0' and i[listnames == 'f.6141.0.l8'] == '0' :
            continue
        
        else:
            outclean.append(i)
    return outclean
            

def write_files(coef,outclean,directory,listnames):
    '''
    Write files:
    Each file starts with an increasing integer number.
    You can specify the directory where you want your file to be saved
    '''
    for k in range(0,len(outclean)):
    #for k in range(0,100):
        if (k % 100) == 0:
            print 'Writing first =' + str(k) + ' files out of ' + str(len(outclean)) 
        outtemp=outclean[k]
        with open(directory + str(k)+'file.txt', 'w') as the_file:
            for j in range(0,len(outtemp)):
                outline = listnames[j] + '\t' + outtemp[j] + "\n"
                the_file.writelines(outline)


# In[312]:


## Run this script for women
coef = np.genfromtxt(fname='coefF_for_simulation_reduced.txt', delimiter='\t',dtype='S60', usecols=(0,1))
listnames = np.unique(coef[:,0])
myarray = generate_array(coef)
out = cartesian(myarray)
outclean = checkingsF(out,listnames)
write_files(coef,outclean,directory='/Users/AndreaGanna/test/',listnames=listnames)


# In[307]:

## Run this script for men
coef = np.genfromtxt(fname='coefM_for_simulation_reduced.txt', delimiter='\t',dtype='S60', usecols=(0,1))
listnames = np.unique(coef[:,0])
myarray = generate_array(coef)
out = cartesian(myarray)
outclean = checkingsM(out,listnames)
write_files(coef,outclean,directory='/Users/AndreaGanna/test/',listnames=listnames)





