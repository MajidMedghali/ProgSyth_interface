import argparse
import sys
sys.path.append('../ProgSynth/examples/pbe/')
from dsl_loader import load_DSL
from dataset_loader import load_dataset
from synth.pbe.solvers import CutoffPBESolver
from synth.syntax import hs_enumerate_prob_grammar, hs_enumerate_prob_u_grammar
import inspect
# Définissez les arguments ici
dsl_name = 'calculator'
dataset_file = '../ProgSynth/examples/pbe/calculator/calculator.pickle'
search_algo = 'heap_search'
solver_name = 'CutoffPBESolver'
timeout = 600

# Créez un objet argparse.Namespace avec les arguments
args = argparse.Namespace(
    dsl=dsl_name,
    dataset=dataset_file,
    search=search_algo,
    solver=solver_name,
    timeout=timeout
)

# Chargez le DSL et le jeu de données
dsl_module = load_DSL(args.dsl)
dsl, evaluator = dsl_module.dsl, dsl_module.evaluator
full_dataset = load_dataset(args.dsl, args.dataset)

# Récupérez la fonction de recherche et le solveur correspondants
det_search, u_search = (hs_enumerate_prob_grammar, hs_enumerate_prob_u_grammar)
solver = CutoffPBESolver(evaluator=evaluator)
signature = inspect.signature(det_search)
for param in signature.parameters.values():
    print(f"Nom: {param.name}, Défaut: {param.default}, Annotation: {param.annotation}")

# Exécutez la recherche de solutions pour chaque tâche du jeu de données
for task in full_dataset.tasks:
    print(task.type_request)
   # enumerator = det_search(task.type_request)
    
    #sol_generator = solver.solve(task, enumerator, timeout=args.timeout)
    #try:
    #    solution = next(sol_generator)
    #    print(f"Solution found for task {task.name}: {solution}")
    #except StopIteration:
    #    print(f"No solution found for task {task.name}")
