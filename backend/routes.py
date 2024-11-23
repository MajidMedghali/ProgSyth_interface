from flask import Blueprint, request, jsonify
import argparse
import sys
sys.path.append('../ProgSynth/examples/pbe/')
from dsl_loader import load_DSL
from dsl_loader import add_dsl_choice_arg
from dataset_loader import add_dataset_choice_arg
from dataset_loader import load_dataset
from synth.pbe.solvers import CutoffPBESolver
from synth.syntax import hs_enumerate_prob_grammar, hs_enumerate_prob_u_grammar
from flask import Flask, jsonify
from dataset_loader import load_dataset
from dsl_loader import load_DSL
from synth.pbe.solvers import NaivePBESolver
from synth.task import Task
from synth.specification import PBEWithConstants
from synth.syntax.program import Program
from synth.syntax import CFG
from synth import Task, PBE
from synth.semantic import DSLEvaluator
from synth.syntax import bps_enumerate_prob_grammar, ProbDetGrammar
from synth.pbe.solvers import CutoffPBESolver

# from synth.specification import PBEWithConstants
#from synth.example import Example


routes = Blueprint('routes', __name__)

@routes.route('/get_dsl_name', methods=['POST'])
def get_dsl_name():
    data = request.get_json()
    dsl_name = data.get('dslName')

    if dsl_name:
        return jsonify({'dslName': dsl_name})
    else:
        return jsonify({'error': 'No DSL name provided'}), 400
        
        
from flask import Flask, request, jsonify


@routes.route('/get_dataset_file', methods=['POST'])
def get_dataset_file():
    data = request.get_json()
    dataset_file = data.get('datasetFile')

    if dataset_file:
        return jsonify({'datasetFile': dataset_file})
    else:
        return jsonify({'error': 'No dataset file provided'}), 400

@routes.route('/get_search_algo', methods=['POST'])

def get_search_algo():
    data = request.get_json()
    search_algo = data.get('searchAlgo')

    if search_algo:
        return jsonify({'searchAlgo': search_algo})
    else:
        return jsonify({'error': 'No search algorithm provided'}), 400

@routes.route('/get_solver', methods=['POST'])
def get_solver():
    data = request.get_json()
    solver = data.get('solver')

    if solver:
        return jsonify({'solver': solver})
    else:
        return jsonify({'error': 'No solver provided'}), 400


@routes.route('/synthesize', methods=['GET'])

def synthesize():
    # Définir les arguments ici
    dsl_name = 'calculator'
    dataset_file = '../ProgSynth/examples/pbe/calculator/calculator.pickle'
    task_timeout = 60.0
    constrained = False

    # Charger le DSL et le dataset
    dsl_module = load_DSL(dsl_name)
    dsl, evaluator = dsl_module.dsl, dsl_module.evaluator
    full_dataset = load_dataset(dsl_name, dataset_file)

    # Configurer le solveur
    solver: NaivePBESolver = NaivePBESolver(evaluator)

    # Effectuer la synthèse de programme
    solutions = []
    for task in full_dataset:
        if isinstance(task.specification, PBEWithConstants):
            task.specification.constants = {
                k: v for k, v in task.specification.constants.items()
                if k in dsl.constant_types
            }
        if constrained:
            enumerator = hs_enumerate_prob_u_grammar(dsl, task.type_request)
        else:
            enumerator = hs_enumerate_prob_grammar(dsl, task.type_request)
        solution: Program = next(solver.solve(task, enumerator, timeout=task_timeout))
        solutions.append(solution)

    return jsonify({'status': 'success', 'solutions': [str(s) for s in solutions]})


@routes.route('/run_synthesis', methods=['GET'])
def run_synthesis():
    try:
        # Définir les arguments manuellement
        dsl_name = "calculator"  # DSL pour la synthèse arithmétique (exemples: "arithmetic", "python")
        dataset_file = "../ProgSynth/examples/pbe/calculator/calculator.pickle"  # Fichier de jeu de données pour la synthèse arithmétique

        # Chargez le DSL et le jeu de données
        
        dsl_module = load_DSL(dsl_name)
        dataset = load_dataset(dsl_name,dataset_file)

        # Effectuez la synthèse de programmes (exemple: afficher les tâches du jeu de données)
        task_names = [task.metadata.get('name', 'Unnamed Task') for task in dataset.tasks]

        return jsonify({'message': 'Program synthesis completed successfully', 'task_names': task_names})
    except Exception as e:
        return jsonify({'error': str(e)})


@routes.route('/solve', methods=['POST'])
def solve():
    print('Received request:', request.headers)
    data = request.get_json(silent=True)

    if data is None:
        print('Request data is None, trying request.data:', request.data)
        data = json.loads(request.data)

    timeout = data.get('timeout')
    timeout_split = timeout.split()
    timeout = int(timeout_split[0]) * 60 
    algo = data.get('algo')
    solver = data.get('solver')

    print(f"Timeout: {timeout}, Algo: {algo}, Solver: {solver}")

    dsl_name = "calculator"
    # Renvoyer un résultat 
    results = run_synth(dsl_name, algo, solver, timeout)
    print(results)

    response_dict = {
        "result": results
    }

    return jsonify(response_dict)

@routes.route('/synthesis', methods=['GET'])
def synthesis(
    #evaluator: DSLEvaluator,
    #task: Task[PBE],
    #pcfg_file: str = None,
    task_timeout: float = 60
):  

    examples = [
            {
                "inputs": [2, 6],
                "output": 8
            },
            {
                "inputs": [-2, 2],
                "output": 0
            }]
    specification = PBEWithConstants(examples,constants = {"add": "+"})
    task = Task(type_request="int -> int", specification=specification)
    dsl_module = load_DSL("calculator")
    dsl, evaluator = dsl_module.dsl, dsl_module.evaluator
    #full_dataset = load_dataset("calculator", "../ProgSynth/examples/pbe/calculator/calculator.pickle")
    solver = CutoffPBESolver(evaluator)
    solution_generator = solver.solve(task,  ProbDetGrammar(hs_enumerate_prob_grammar), task_timeout)
    try:
        solution = next(solution_generator)
        print("Solution:", solution)
    except StopIteration:
        # Failed generating a solution
        print("No solution found under timeout")
    for stats in solver.available_stats():
        print(f"\t{stats}: {solver.get_stats(stats)}")
    
    
    
    
    



dsl_name = "calculator" 
dataset_file = "../ProgSynth/examples/pbe/calculator/calculator.pickle" 
dsl_module = load_DSL(dsl_name)
full_dataset = load_dataset(dsl_name,dataset_file)
evaluator = dsl_module.evaluator
solver = CutoffPBESolver(evaluator)
@routes.route('/solveee', methods=['GET'])
def solve_problem_function():
    results = []
    for task in full_dataset.tasks:
        try:
            enumerator = hs_enumerate_prob_grammar(task)
            solution = next(solver.solve(task,enumerator))
            results.append((task, solution))
        except StopIteration:
            results.append((task, None))
    
    
    formatted_results = []
    for task, solution in results:
        if solution:
            formatted_results.append({
                'task_name': task.name,
                'solution': solution.code
            })
        else:
            formatted_results.append({
                'task_name': task.name,
                'solution': 'No solution found'
            })

    return jsonify(formatted_results)

if __name__ == '__main__':
    app.run(debug=True)
