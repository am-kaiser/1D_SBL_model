"""
Script to run randomized version of model by van de Wiel et al.

Van de Wiel, B. J. H., and Coauthors, 2017: Regime transitions in near-surface temperature inversions:
A conceptual model. Journal of the Atmospheric Sciences, 74, 1057–1073, https://doi.org/10.1175/JAS-D-16-0180.1.
"""
import os
import time
import json
import ast
import dataclasses

from DomeC import process_dome_c_data
from one_D_model.utils import plot_output as plot, parse_command_line_input
from one_D_model.model import run_SDE_model as run_1D_SDE_model
from one_D_model.model import parameters, solve_ODE, make_bifurcation_analysis, solve_SDEs, solve_SDE_stoch_stab_function, compare_stability_functions


def save_parameters_in_file(params):
    # Define name of parameter file
    file_name = str(params.sol_directory_path) + 'parameters.json'
    # Transform parameter class to json
    params_json = params.to_json()
    # Save json to file + remove unnecessary characters
    with open(file_name, 'w') as file:
        json.dump(ast.literal_eval(params_json), file)


# Read command line input
function, stab_function, Qi, Lambda, z0, u, make_plot = parse_command_line_input.read_command_line_input()
# -----------------------------------------------------------------------------------------
# Load Parameters
param = parameters.Parameters()
# -----------------------------------------------------------------------------------------
# Make directory for output
param.sol_directory_path = 'output' + '/' + time.strftime("%Y%m%d_%H%M_%S") + '/'
if not os.path.exists(param.sol_directory_path):
    os.makedirs(param.sol_directory_path)
    os.makedirs(param.sol_directory_path + 'temporary/')
# -----------------------------------------------------------------------------------------
# Save parameters
save_parameters_in_file(param)
# -----------------------------------------------------------------------------------------
if make_plot:
    # Process Dome C data and plot it
    # process_dome_c_data.main(param)
    # # -------------------------------------------------------------------------------------
    # # Solve deterministic ODE
    # ODE_sol = solve_ODE.solve_deterministic_ODE(param)
    # # Plot solution of deterministic model
    # plot.make_2D_plot(param, ODE_sol.t.flatten(), ODE_sol.y.flatten(), 'ODE_sol.png')
    # Plot stability functions
    compare_stability_functions.make_comparison(param)
    # -------------------------------------------------------------------------------------
    # Make bifurcation plots
    # copy dataclass to prevent overwriting original
    # param_copy = dataclasses.replace(param)
    # param_copy.sol_directory_path = param.sol_directory_path
    # param_copy.stab_func_type = 'short_tail'
    # make_bifurcation_analysis.make_bifurcation_analysis(param_copy)
    # param_copy.stab_func_type = 'long_tail'
    # make_bifurcation_analysis.make_bifurcation_analysis(param_copy)
    # Plot potential
    #plot.plot_potentials(param)
# -----------------------------------------------------------------------------------------
# Run 1D model (with randomizations)
if function:
    run_1D_SDE_model.solve_randomized_model(param)

if Qi:
    function_name = solve_SDEs.solve_SDE_with_stoch_Qi
    sol_file_name = 'SDE_Qi_sol'
    run_1D_SDE_model.solve_model_with_randomized_parameter(param, function_name, sol_file_name)

if Lambda:
    function_name = solve_SDEs.solve_SDE_with_stoch_lambda
    sol_file_name = 'SDE_lambda_sol'
    run_1D_SDE_model.solve_model_with_randomized_parameter(param, function_name, sol_file_name)

if u:
    function_name = solve_SDEs.solve_SDE_with_stoch_u
    sol_file_name = 'SDE_u_sol'
    run_1D_SDE_model.solve_model_with_randomized_parameter(param, function_name, sol_file_name)

if stab_function:
    function_name = solve_SDE_stoch_stab_function.solve_SDE_with_stoch_stab_function
    sol_file_name = 'SDE_stab_func_sol'
    run_1D_SDE_model.solve_model_with_randomized_parameter(param, function_name, sol_file_name)

if z0:
    sol_file_name = 'SDE_z0_sol'
    run_1D_SDE_model.solve_model_with_randomized_parameter_z0(param, sol_file_name)
