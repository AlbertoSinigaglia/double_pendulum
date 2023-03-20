import numpy as np

from double_pendulum.model.model_parameters import model_parameters
from double_pendulum.controller.partial_feedback_linearization.symbolic_pfl import (
    SymbolicPFLAndLQRController,
)
from sim_parameters import mpar, dt, t_final, t0, x0, goal, integrator, design, model, robot

name = "pflcol_lqr"
leaderboard_config = {"csv_path": "data/" + name + "/sim_swingup.csv",
                      "name": name,
                      "username": "fwiebe"}

pfl_method = "collocated"

torque_limit = [0.0, 5.0]

mpar.set_motor_inertia(0.0)
mpar.set_damping([0.0, 0.0])
mpar.set_cfric([0.0, 0.0])
mpar.set_torque_limit(torque_limit)

# controller parameters
# lqr parameters
Q = np.diag((0.97, 0.93, 0.39, 0.26))
R = np.diag((0.11, 0.11))
par = [1., 1., 1.]

controller = SymbolicPFLAndLQRController(
    model_pars=mpar, robot=robot, pfl_method=pfl_method
)
controller.lqr_controller.set_cost_parameters(
    p1p1_cost=Q[0, 0],
    p2p2_cost=Q[1, 1],
    v1v1_cost=Q[2, 2],
    v2v2_cost=Q[3, 3],
    p1v1_cost=0.0,
    p1v2_cost=0.0,
    p2v1_cost=0.0,
    p2v2_cost=0.0,
    u1u1_cost=R[0, 0],
    u2u2_cost=R[1, 1],
    u1u2_cost=0.0,
)

controller.set_goal(goal)
controller.set_cost_parameters_(par)
controller.init()
