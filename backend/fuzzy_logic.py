import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. Define fuzzy variables
# Inputs
dirt_level = ctrl.Antecedent(np.arange(0, 101, 1), 'dirt_level')
load_size = ctrl.Antecedent(np.arange(0, 101, 1), 'load_size')

# Output
cycle_time = ctrl.Consequent(np.arange(0, 121, 1), 'cycle_time')

# 2. Define membership functions
# Dirt Level (0-100)
dirt_level['low'] = fuzz.trimf(dirt_level.universe, [0, 0, 50])
dirt_level['medium'] = fuzz.trimf(dirt_level.universe, [0, 50, 100])
dirt_level['high'] = fuzz.trimf(dirt_level.universe, [50, 100, 100])

# Load Size (0-100)
load_size['small'] = fuzz.trimf(load_size.universe, [0, 0, 50])
load_size['medium'] = fuzz.trimf(load_size.universe, [0, 50, 100])
load_size['large'] = fuzz.trimf(load_size.universe, [50, 100, 100])

# Cycle Time (0-120 mins)
cycle_time['short'] = fuzz.trimf(cycle_time.universe, [0, 0, 40])
cycle_time['medium'] = fuzz.trimf(cycle_time.universe, [20, 60, 100])
cycle_time['long'] = fuzz.trimf(cycle_time.universe, [80, 120, 120])

# 3. Define the rules
rule1 = ctrl.Rule(dirt_level['low'] & load_size['small'], cycle_time['short'])
rule2 = ctrl.Rule(dirt_level['low'] & load_size['medium'], cycle_time['medium'])
rule3 = ctrl.Rule(dirt_level['low'] & load_size['large'], cycle_time['medium'])

rule4 = ctrl.Rule(dirt_level['medium'] & load_size['small'], cycle_time['medium'])
rule5 = ctrl.Rule(dirt_level['medium'] & load_size['medium'], cycle_time['medium'])
rule6 = ctrl.Rule(dirt_level['medium'] & load_size['large'], cycle_time['long'])

rule7 = ctrl.Rule(dirt_level['high'] & load_size['small'], cycle_time['medium'])
rule8 = ctrl.Rule(dirt_level['high'] & load_size['medium'], cycle_time['long'])
rule9 = ctrl.Rule(dirt_level['high'] & load_size['large'], cycle_time['long'])

# 4. Create the control system and simulation
washing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
washing_simulator = ctrl.ControlSystemSimulation(washing_ctrl)

def compute_cycle_time(dirt: float, load: float) -> float:
    """
    Computes the washing machine cycle time using fuzzy logic.
    :param dirt: 0 to 100 (Dirt Level)
    :param load: 0 to 100 (Load Size)
    :return: Estimated cycle time in minutes
    """
    # Clip inputs to ranges just to be safe
    dirt = max(0, min(100, dirt))
    load = max(0, min(100, load))
    
    washing_simulator.input['dirt_level'] = dirt
    washing_simulator.input['load_size'] = load
    
    try:
        washing_simulator.compute()
        result = washing_simulator.output['cycle_time']
        return round(result, 2)
    except Exception as e:
        # Default fallback in case of edge values not fully caught
        return 60.0
