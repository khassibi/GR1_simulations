import tulip as tlp

def set_specs(env_vars, sys_vars, env_init, sys_init, env_safe, sys_safe, 
              env_prog, sys_prog):
    '''
    Creates the GR(1) specifications and uses the correct settings for the specs
    '''
    # Function found in tulip-control/tulip/spec/form.py
    specs = tlp.spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                            env_safe, sys_safe, env_prog, sys_prog)
    specs.qinit = '\A \E'
    specs.moore = False # mealy controller
    specs.plus_one = False
    return specs