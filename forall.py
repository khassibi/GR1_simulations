import logging
from tulip import spec
from tulip import synth
from tulip.transys import machines
from tulip import dumpsmach
import pickle
import simulations
import traceback
from tulip.interfaces import omega as omega_int
from omega.games import gr1

logging.basicConfig(level=logging.WARNING)

class ForAll(simulations.Simulation):
    def make_specs(self):
        env_vars = {}
        sys_vars = {}
        env_vars['b'] = (0,1)
        sys_vars['r'] = (0,1)

        env_init = {'b=1'}
        sys_init = {}

        env_safe = {'b=0'}
        sys_safe = {"r = 0"}

        env_prog = {'b=0'}
        sys_prog = {"r=0"}

        # Create a GR(1) specification
        specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init, env_safe, sys_safe, env_prog, sys_prog)
        # Print specifications:
        # print(specs.pretty())
        #
        # Controller synthesis
        #
        # The controller decides based on current variable values only,
        # without knowing yet the next values that environment variables take.
        # A controller with this information flow is known as Moore.
        specs.moore = self.moore

        specs.plus_one = self.plus_one

        # Ask the synthesizer to find initial values for system variables
        # that, for each initial values that environment variables can
        # take and satisfy `env_init`, the initial state satisfies
        # `env_init /\ sys_init`.

        specs.qinit = self.qinit  # i.e., "there exist sys_vars: forall env_vars"

        self.specs = specs

        aut = omega_int._grspec_to_automaton(specs)
        winning_set, _, __ = gr1.solve_streett_game(aut)
        check_bdd = aut.let({'r':1, 'b':0}, winning_set)
        print(check_bdd == aut.true)
        # 'r':0, 'b':0 in winning set
        # 'r':0, 'b':1 in winning set
        # 'r':1, 'b':1 is NOT in winning set
        # 'r':1, 'b':0 is NOT in winning set
        # write a short description of what we learned today: figuring out plus_one and qinit
        # plus one: thing has to be true one time step later. never set plus_one to be anything but true because then you'll lose causality
        # qinit: AN INTERESTING CASE: go through these cases for b0r0 on the whiteboard
        # the sys_init = {} or true comes into play here
        # hypothesis to why it is not realizable? it removes states that violate safety set, so when it computes the winning set, it gets it wrong
        # it should not matter because you should not give it an initial condition that the environment instantly violates and what should the system do
        # let's show examples, where each of the 
        # \E \A and \A \E: get it back to the initial conditions
        # see when \E \A and \A \E have the same controllers. they may have different initial conditions
        # need an example where: the system initial condition depends on what the environment condition does
        # the initial conditions can be a formula
        # does env_init only depend on env variables?

        return specs.pretty()


if __name__ == '__main__':
    path = 'forall/'
    sims = []
    name = 'test_run'
    asrts = open(path + "asrts_" + name + ".txt", "w")
    f = open(path + "runs_" + name + ".txt", "w")
    f.write("The simulations of runner blocker that have a realizable controller\n")
    i = 0
    for plus_one in [True, False]:
        for moore in [True, False]:
            for qinit in ['\E \A', '\A \E', '\A \A', '\E \E']:
                run = ForAll(plus_one, moore, qinit)
                run.give_name('rb')
                specs = run.make_specs()
                if i == 0:
                    asrts.write(specs)
                    f.write(specs)
                i += 1
                asrts.write('\n------\n')
                asrts.write(run.name)
                try:
                    run.make_strat(path)
                except Exception as e:
                    # asrts.write(f"\nError: {type(e).__name__}")
                    asrts.write('\n' + str(traceback.format_exc(-1)))

                sims.append(run)
                if run.realizable:
                    f.write('\n------\n')
                    f.write(run.name)
    f.close()
