import logging
from tulip import spec
from tulip import synth
from tulip.transys import machines
from tulip import dumpsmach
import pickle
import simulations
import traceback

logging.basicConfig(level=logging.WARNING)

class ForAll(simulations.Simulation):
    def make_specs(self):
        env_vars = {}
        sys_vars = {}
        env_vars['b'] = (0,1)
        sys_vars['r'] = (0,1)

        env_init = {}
        sys_init = {}

        env_safe = {
                    "b=0 || b = 1"
                }


        sys_safe = {
                        "r=0 || r = 1"
                    }

        env_prog = {"b=0 || b = 1"}
        sys_prog = {"r=0 || r = 1"}

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

        return specs.pretty()


if __name__ == '__main__':
    path = 'forall/'
    sims = []
    asrts = open(path + "asrts_bothtrue.txt", "w")
    f = open(path + "runs_bothtrue.txt", "w")
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
