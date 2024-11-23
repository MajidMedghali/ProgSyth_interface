
import json
from flask import jsonify
import re
operators = ['+', '-']


# Transform expression then update inputs then evaluate then store in json file
def rec_fun(L, M):
    if not len(L)  and len(M) == 1:
        return '('+M[0]+')'
    if len(L) == 1 and len(M) == 2:
        return '(' + L[0] + ' '+ M[0] +' ' +M[1] + ')'
    
    return '('+ L[0] +' '+ M[0]+' ' +rec_fun(L[1:], M[1:]) + ')'    
        

def extract_and_remove_numbers(text):
 
  numbers = re.findall(r"\d+", text)
  cleaned_text = re.sub(r"\d+", "", text)
  return [numbers, cleaned_text]

# print(extract_and_remove_numbers("x+y+709+98"))       
# L = [1, 0]
def transform_expression(expression, inputs):
    
    if '(' in expression or ')' in expression:
        return "CAN'T TRANSFORM EXPRESSION"
    new_clon = expression[:]
    clon = new_clon.replace(' ', '')
    op_list = []
    var_list = []
    fin_list = []
    const_list = []
    const_list_type = []
    while(len(clon) > 0):
        element = clon[0]
        clon = clon[1:]
        if element in operators:
            op_list.append(element)
        elif element.isdigit():
            number = element
            dummy = clon[:]
            counter = 0
            num_points  = 0
            while len(dummy) > 0 and (dummy[0].isdigit() or dummy[0] == '.') and num_points < 2:
                if dummy[0] == '.':
                    num_points += 1
                number  = number+dummy[0]
                dummy = dummy[1:]
                counter += 1
              
            if num_points >= 2 :
                return "CAN'T TRANSFORM EXPRESSION"
            elif num_points == 1 :
                const_list.append(number)
                const_list_type.append('f')
            else:
                const_list.append(number)
                const_list_type.append('i')
            clon = clon[counter:]
            fin_list.append(number)
            
        else: 
            var_list.append(element)
            index = var_list.index(element)
            fin_list.append(f"var{index}")
  
    eval_list = fin_list[:]       
    if len(op_list) + 1 != len(fin_list):
        return "CAN'T TRANSFORM EXPRESSION"
    
    vector_var = get_var_vector(inputs)
    L =[]
    for element in fin_list:
        if element not in const_list:
            if len(vector_var) > 0:
                L.append(vector_var[0])
                vector_var = vector_var[1:]
        else:
            if len(const_list) > 0:
                if(const_list_type[0] == 'f'):
                    L.append(1)
                else :
                    L.append(0)
                const_list = const_list[1:]
                const_list_type = const_list_type[1:]
    
  
    new_dict = dict.fromkeys(fin_list, L)
    for key, value in zip(new_dict.keys(), L):
         new_dict.update({key: value})

    if 1 in new_dict.values():
        for i in range(len(fin_list)) :
            if not new_dict[fin_list[i]]:
                fin_list[i] = '(int2float '+ fin_list[i] +')'
    
    return [rec_fun(op_list, fin_list), eval_list, op_list, L]


def calculate_num_param(expression):
    if not len(expression):
        return "CAN'T TRANSFORM EXPRESSION"
    if '(' in expression or ')' in expression:
        return "CAN'T TRANSFORM EXPRESSION"
    new_clon = expression[:]
    clon = new_clon.replace(' ', '')
    op_list = []
    var_list = []
    fin_list = []
    const_list = []
    const_list_type = []
    while(len(clon) > 0):
        element = clon[0]
        clon = clon[1:]
        if element in operators:
            op_list.append(element)
        elif element.isdigit():
            number = element
            dummy = clon[:]
            counter = 0
            num_points  = 0
            while len(dummy) > 0 and (dummy[0].isdigit() or dummy[0] == '.') and num_points < 2:
                if dummy[0] == '.':
                    num_points += 1
                number  = number+dummy[0]
                dummy = dummy[1:]
                counter += 1
              
            if num_points >= 2 :
                return "CAN'T TRANSFORM EXPRESSION"
            elif num_points == 1 :
                const_list.append(number)
                const_list_type.append('f')
            else:
                const_list.append(number)
                const_list_type.append('i')
            clon = clon[counter:]
            fin_list.append(number)
            
        else: 
            var_list.append(element)
            index = var_list.index(element)
            fin_list.append(f"var{index}")
       
    if len(op_list) + 1 != len(fin_list):
        return "CAN'T TRANSFORM EXPRESSION"
    
    print(fin_list)
    print(op_list)
    
    return len(list(set(var_list)))

# print(calculate_num_param("x+y+y+9.9"))

def get_var_vector(inputs):
    vector = inputs[0]
    n = len(vector)
    vector = [0 for _ in range(n)]
   
    for input in inputs:
        for i in range(n):
            if vector[i] == 1:
                continue
            elif isinstance(input[i], float):
                vector[i] = 1
            else : vector[i] = 0

        
    return vector

def update_inputs(inputs):
    vector = get_var_vector(inputs)
    for j in range(len(vector)):
        if vector[j] == 1:
            for i in range(len(inputs)):
                inputs[i][j] = float(inputs[i][j])
    return inputs
    
inp = [[1,2, 4.98], [0,6.9, 0], [0, 8, 1], [2,4, 10]]

# print(get_var_vector(inp))         
def get_element(var, fi, input): 
    if var[0:3] == "var" :
        return input[int(var[3])]
    else:
        if not fi :
            return int(var)
        else:
            return float(var)
        


def evaluate_expression(M, N, L,input):
    value = 0 
    dummy = 1
    index_tracker = 0
    if len(M) == 1:
        return get_element(M[0], [], input)
    for i in range(len(N)):
        if dummy:
            if N[i] == '+':
                value = get_element(M[i], L[i], input) + get_element(M[i+1], L[i+1], input)
            elif N[i] == '-':
                value = get_element(M[i], L[i], input) - get_element(M[i+1], L[i+1], input)
            dummy = 0
     
        else:
            if N[i] == '+':
                value += get_element(M[i+1], L[i+1], input) 
            elif N[i] == '-':
                value -= get_element(M[i+1], L[i+1], input) 
        index_tracker+=1
        
    return value
  
    
# te = transform_expression("x + 7 + y + z + 9.8", [[1, 2, 3], [9, 1, 1 ]])
# print(evaluate_expression(te[1], te[2], te[3], [5,9,8]))
# filename = "test.json"
# STORE JSON NEEDS TO BE MODIFIED
def store_json(exp, f_or_i, inputs, filename):


  te = transform_expression(exp, f_or_i)  

  data = {}
  data["program"] = te[0]  
  examples = []
  for element in inputs:
    sample = {}
    sample["inputs"] = element
    sample["output"] = evaluate_expression(te[1], te[2], element)  
    examples.append(sample)
  data["examples"] = examples

  print(data)
#   with open(filename, 'w') as f:
#     json.dump(data, f, indent=4)

#   print(f"Data stored successfully in {filename}.")

def calculate_bis(expression):
    if expression.isdigit():
        print(int(expression))
        return int(expression)
    return "INVALID EXPRESSION"
    