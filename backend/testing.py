from flask import Flask,jsonify, request
from synth.task import Task
import pickle
import json
from synth.syntax.grammars.cfg import CFG
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from expression import calculate_bis
import ast
import sys
sys.path.append('../ProgSynth/examples/pbe/')
from dsl_loader import load_DSL
from synth.specification import PBE, Example
from synth.syntax.type_system import (
    INT,
    STRING,
    List,
    PolymorphicType,
    PrimitiveType,
)
from synth.syntax.type_helper import FunctionType
from dataset_loader import load_dataset
from synth.pbe.solvers import CutoffPBESolver
from dataset_loader import load_dataset
from dsl_loader import load_DSL

from synth.task import Task


from synth.syntax import CFG
from synth import Task, PBE
from synth.semantic import DSLEvaluator
from synth.syntax import bps_enumerate_prob_grammar, ProbDetGrammar

from synth.pbe.solvers import (
    NaivePBESolver,
    PBESolver,
    CutoffPBESolver,
    RestartPBESolver,
)
app = Flask(__name__)
CORS(app)



# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///progsynth.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)


# Define a model for the expressions
class Expression(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(255), nullable=False)

# Route to handle expression submission
@app.route('/Dsl', methods=['POST'])
def submit_expression():
    data = request.get_json()
    expression_text = data.get('expression')
    
    existing_expression = Expression.query.filter_by(id=1).first()

    # If an existing row is found, delete it
    if existing_expression:
        db.session.delete(existing_expression)
        db.session.commit()

    # Add the new expression
    new_expression = Expression(id=1, expression=expression_text)
    db.session.add(new_expression)
    db.session.commit()

    return jsonify({'message': 'Expression submitted successfully'}), 200

@app.route('/get_inputs', methods=['POST'])
def get_inputs():
    data = request.get_json()
    expression_text = data.get('expression')

    # Store the inputs in the second position in the database
  
    existing_expression = Expression.query.filter_by(id=2).first()

    # If an existing row is found, delete it
    if existing_expression:
        db.session.delete(existing_expression)
        db.session.commit()

    # Add the new expression
    new_expression = Expression(id=2, expression=json.dumps(expression_text))
    db.session.add(new_expression)
    db.session.commit()
    # Return a response indicating success
    return jsonify({'message': 'Inputs stored successfully'}), 200


@app.route('/eval', methods=['POST'])
def eval():
    data = request.get_json()
    expression_text = data.get('expression')

    # Store the inputs in the second position in the database
    
    existing_expression = Expression.query.filter_by(id=7).first()

    # If an existing row is found, delete it
    if existing_expression:
        db.session.delete(existing_expression)
        db.session.commit()

    # Add the new expression
    new_expression = Expression(id=7, expression=json.dumps(expression_text))
    db.session.add(new_expression)
    db.session.commit()

    # Return a response indicating success
    return jsonify({'message': 'Inputs stored successfully'}), 200


@app.route('/get_addons/<int:expression_id>', methods=['POST'])
def get_addons(expression_id):
    data = request.get_json()
    expression_text = data.get('expression')
    
    # Retrieve the third row from the database
   
    existing_expression = Expression.query.filter_by(id=expression_id).first()

    # If an existing row is found, delete it
    if existing_expression:
        db.session.delete(existing_expression)
        db.session.commit()

    # Add the new expression
    new_expression = Expression(id=expression_id, expression=expression_text)
    db.session.add(new_expression)
    db.session.commit()

    return jsonify({'message': 'Expression submitted successfully'}), 200





@app.route('/get_number_of_parameters', methods=['GET'])
def get_number_params():
    expression = Expression.query.first().expression
    num_param = calculate_bis(expression)
    return jsonify({"num_param":num_param})

# @app.route('/evaluate_expression', methods = ['GET'])
# def evaluate_expression():
#     expression = Expression.query.first().expression
#     expression_inputs  = Expression.query.filter_by(id=2)   
    # te = transform_expression(expression)
    # print(expression.expression)
    # print(expression_inputs.expression)
    # final = []
    # for input in expression_inputs:
    #     final.append(evaluate_expression(te[0], te[1], input))
    # return jsonify({"outputs":final})
        

@app.route('/get_expression/<int:expression_id>', methods=['GET'])
def get_expression(expression_id):
    expression = Expression.query.get(expression_id)
    if expression:
        return jsonify({'expression': expression.expression})
    else:
        return jsonify({'error': 'Expression not found'}), 404
    


# from synth.specification import PBEWithConstants
#from synth.example import Example






    
def reformat_solution(solution):
    # Supprimer les parenthèses
    solution = solution.replace("(", "").replace(")", "")

    # Séparer les variables et les opérateurs
    tokens = solution.split()

    # Remplacer les opérateurs par leurs équivalents textuels
    formatted_tokens = []
    for i, token in enumerate(tokens):
        if token in ["+", "-", "*", "/"]:
            if i == 0 or (i > 0 and not tokens[i-1].isdigit() and not tokens[i-1].startswith("var")):
                formatted_token = " plus " if token == "+" else " moins " if token == "-" else " fois " if token == "*" else " divisé par "
            else:
                formatted_token = token
        else:
            formatted_token = token
        formatted_tokens.append(formatted_token)

    # Réorganiser les variables dans un ordre approprié
    variables = [token for token in formatted_tokens if token.startswith("var")]
    variables.sort(key=lambda x: int(x[3:]))
    constants = [token for token in formatted_tokens if token.isdigit()]

    # Reconstruire l'expression
    formatted_variables = " + ".join(variables)
    formatted_constants = " + ".join(constants)

    if formatted_constants and formatted_variables:
        formatted_solution = formatted_variables + " + " + formatted_constants
    else:
        formatted_solution = formatted_variables + formatted_constants

    return formatted_solution


new_program = []
new_cfg = []

#-----------------------------------------------------
@app.route('/synth', methods = ['GET'] )
def synth_test():
    examples = Expression.query.filter_by(id=2).first().expression
    num_param = int(Expression.query.first().expression)
    dsl_name = 'calculator'


    dsl_module = load_DSL(dsl_name)
    dsl, evaluator = dsl_module.dsl, dsl_module.evaluator

    dataset_file = "../ProgSynth/examples/pbe/calculator/calculator.pickle"
    
    full_dataset = load_dataset(dsl_name, dataset_file)
    
    temp = ast.literal_eval(examples)
   

  
    examp = []
    all_inputs = []
    for example in temp:
        l = list(map(float, example))
        output = l.pop()
        inputs = l
        all_inputs.append(inputs[:])
        struct = Example(inputs = inputs, output = output)
        examp.append(struct)
        
    specification=PBE(examp)


   


    contraint = getattr(dsl_module, "constraints", [])
    type = getattr(dsl_module, "constant_types", set())
    types = [INT for i in range(num_param+1)]
    type_req = FunctionType(*types)


    global new_cfg
    new_cfg = CFG.depth_constraint(dsl, type_req, 7)
    cfg = CFG.depth_constraint(dsl, type_req, 7)
    pcfg = ProbDetGrammar.uniform(cfg)


    tasks = [
        Task(cfg.type_request, specification)
    ]



    timeout = 60*int(Expression.query.filter_by(id=3).first().expression)
 
    algo = Expression.query.filter_by(id=4).first().expression
    solver_front = Expression.query.filter_by(id=5).first().expression


    print(f"Timeout: {timeout}, Algo: {algo}, Solver: {solver_front}")

    dsl_name = "calculator"
    def synthesis(
    evaluator: DSLEvaluator,
    task: Task[PBE],
    pcfg: ProbDetGrammar,
    task_timeout: float = 60
):      
        if solver_front == "naive":
        	solver = NaivePBESolver(evaluator)
        elif solver_front == "cutoff":
        	solver = CutoffPBESolver(evaluator)
        elif solver_front == "restart":
        	solver = RestartPBESolver(evaluator)
        #elif solver_front == "PBESolver":
        #	solver = PBEsolver(evaluator)
        solution_generator = solver.solve(task, bps_enumerate_prob_grammar(pcfg), task_timeout)
        try:
            solution = next(solution_generator)
            solution_str = str(solution)
            for stats in solver.available_stats():
                print(f"\t{stats}: {solver.get_stats(stats)}") 
            return [solution_str, solution_generator]
        except StopIteration:
            # Failed generating a solution
            print("No solution found under timeout")
 

    full_solution = synthesis(evaluator, tasks[0], pcfg, timeout)
    if full_solution:
       solution = full_solution[0]
    else:
       solution = None
    # for program in full_solution[1]:
    #     evaluator.eval(program, *all_inputs)
    if solution:
        if not Expression.query.filter_by(id=6).first():
            data_object1 = Expression(id=6, expression=solution)
            db.session.add(data_object1)
        db.session.commit()
        
        print(solution)
        
        if '-' in solution:
            formatted_solution = solution
        else:
            formatted_solution = reformat_solution(solution)
        global new_program
        new_program = full_solution[1]

        return jsonify(formatted_solution)
    else:
    	return jsonify('No solution found under this timeout')
   
  


        
    
  
        
   



@app.route('/evaluate_solution', methods = ['GET'])
def evaluate_solution():
    eval_inputs = Expression.query.filter_by(id=7).first().expression
    
    temp = ast.literal_eval(eval_inputs)
    for element in temp:
        element.pop()
    examp = []
    print(temp)
    for example in temp:
        l = list(map(int, example))
        inputs = l
        struct = Example(inputs = inputs, output = 0)
        examp.append(struct)
        
    dsl_name = 'calculator'


    dsl_module = load_DSL(dsl_name)
    evaluator = dsl_module.evaluator
    print("examp",examp)
    task= Task(new_cfg.type_request, PBE(examp))
    evaluations = []
    for program in new_program:
        for example in task.specification.examples:
            print("example", example)
                # assert evaluator.eval(program, example.inputs) == example.output
            evaluations.append(evaluator.eval(program, example.inputs))
        break
        
        
    
    print(evaluations)
    return jsonify({'evaluations':evaluations})






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)
