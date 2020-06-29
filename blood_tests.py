# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 16:53:46 2020

@author: Aleksandre
"""

import random as rand
import math
import matplotlib.pyplot as plt


def find_infected(n,p):
    
    #n - power of 2
    #p - infection probability
    
    #initialize all samples as false
    samples = [False] * int(math.pow(2,n))
    
    #randomly set each sample to True with probability p
    for i in range(int(math.pow(2,n))):
        if rand.random() < p:
            samples[i] = True
    
    #test the samples
    test_res = binary_test(samples,0,int(math.pow(2,n)))
    results = []
    decipher(test_res,n,results)
    test_num = count_tests(test_res)
    
    #print("NUMBER OF TESTS: ",test_num)
    #print("RESULTS: " ,results)
    #print("ORIGINAL SAMPLES: ", samples)
    
    return [test_num,results,samples]

def group_test(arr):
    for i in range(len(arr)):
        if arr[i] == True:
            return True
    return False
# Returns index of x in arr if present, else -1 
def binary_test(arr, start, end):
    results = []
    #Initial test
    if group_test(arr) == False:
        results.append(False)
    else:
    #divide samples into two groups
        if end-start>1 and len(arr)>1:
            mid  = (start+end)//2
            #test each group
            group_1 = group_test(arr[start:mid])
            group_2 = group_test(arr[mid:end])
            #if a group test positive, recurse binary_test on that group
            if group_1:
                results.append(binary_test(arr, start, mid))
            else:
                results.append(False)
            if group_2:
                results.append(binary_test(arr, mid, end))
            else:
                results.append(False)
        else:
            results.append(arr[start:end])
        
    #return bool array
    return results

def decipher(arr,n,res):
    if len(arr) > 1:
        if arr[0] == False:
            for i in range(int(math.pow(2,n-1))):
                res.append(False)
        else:
            decipher(arr[0],n-1,res)
        if arr[1] == False:
            for i in range(int(math.pow(2,n-1))):
                res.append(False)
        else:
            decipher(arr[1],n-1,res)
    else:
        res.append(arr)
def count_tests(arr):
    i = 0
    if type(arr) == bool or len(arr) == 1:
        return i+1
    else:
        i = 1+count_tests(arr[0]) + count_tests(arr[1])
    return i


def find_avg_tests(n,p,x):
    total_tests = 0
    num_tests = []
    for i in range(x):
        tests = find_infected(n,p)[0]
        total_tests += tests
        num_tests.append(tests)
    return [total_tests/x,num_tests]


def find_avg_tests_over_p(n,p,x,y):
    prob = []
    num_tests = []
    for i in range(y):
        prob.append(i*p)
        num_tests.append(find_avg_tests(n,p*i,x)[0])
    return [prob,num_tests]


def plot_avg_tests_over_p(n,p,x,y):
    #p - base probability
    #y - number of iterations of probability
    
    avg_tests_over_p = find_avg_tests_over_p(n,p,x,y)
    plt.plot(avg_tests_over_p[0],avg_tests_over_p[1])
    plt.plot([int(math.pow(2,n)),int(math.pow(2,n))])
    plt.title("Average number of tests vs Probability of infection")
    plt.xlabel("Probability of Infection")
    plt.ylabel("Average number of tests required")
    plt.legend(["Tests","Number of Samples: " + str(int(math.pow(2,n)))])
    plt.savefig("avg_tests_over_p "+str(n),dpi=500)
    plt.show()
    
    return avg_tests_over_p


def find_variance_p(n,p,x):
    avg = find_avg_tests(n,p,x)
    total_sq_dist = 0
    for i in range(x):
        total_sq_dist+= math.pow((avg[1][i]-avg[0]),2)
    return total_sq_dist/(x-1)

def find_avg_sd_tests_over_n(n,p,x,y):
    num_samples = []
    sd = []
    for k in range(3,n+1):
        num_samples.append(math.pow(2,k))
    for j in range(3,n+1):
        sd_total = 0
        for i in range(y):
            sd_total+= math.sqrt(find_variance_p(j,p,x))
        sd.append(sd_total/y)
    return[num_samples,sd]

def plot_avg_sd_tests_over_n(n,p,x,y):
    avg = find_avg_sd_tests_over_n(n,p,x,y)
    plt.plot(avg[0],avg[1])
    plt.title("Avg Standard Deviation vs Number of Samples, p = "+str(p))
    plt.ylabel("Avg Standard Deviation")
    plt.xlabel("Number of Samples")
    plt.savefig("avg_sd_over_n "+str(n),dpi=500)
    plt.show()
    
    return avg

print(plot_avg_sd_tests_over_n(7,1/128,500,15))
print(plot_avg_tests_over_p(7,1/128,300,128))

