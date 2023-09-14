class sys_ctrl(object):
    """Mealy transducer.

    Internal states are integers, the current state
    is stored in the attribute "state".
    To take a transition, call method "move".

    The names of input variables are stored in the
    attribute "input_vars".

    Automatically generated by tulip.dumpsmach on 2023-09-13 00:28:19 UTC
    To learn more about TuLiP, visit http://tulip-control.org
    """
    def __init__(self):
        self.state = 6
        self.input_vars = ['b']

    def move(self, b):
        """Given inputs, take move and return outputs.

        @rtype: dict
        @return: dictionary with keys of the output variable names:
            ['r']
        """
        output = dict()
        if self.state == 0:
            if (b == 1):
                self.state = 1

                output["r"] = 3
            elif (b == 3):
                self.state = 2

                output["r"] = 2
            else:
                self._error(b)
        elif self.state == 1:
            if (b == 2):
                self.state = 3

                output["r"] = 4
            else:
                self._error(b)
        elif self.state == 2:
            if (b == 2):
                self.state = 3

                output["r"] = 4
            else:
                self._error(b)
        elif self.state == 3:
            if (b == 1):
                self.state = 4

                output["r"] = 4
            elif (b == 3):
                self.state = 5

                output["r"] = 4
            else:
                self._error(b)
        elif self.state == 4:
            if (b == 2):
                self.state = 3

                output["r"] = 4
            else:
                self._error(b)
        elif self.state == 5:
            if (b == 2):
                self.state = 3

                output["r"] = 4
            else:
                self._error(b)
        elif self.state == 6:
            if (b == 2):
                self.state = 0

                output["r"] = 1
            else:
                self._error(b)
        else:
            raise Exception("Unrecognized internal state: " + str(self.state))
        return output

    def _error(self, b):
        raise ValueError("Unrecognized input: " + (
            "b = {b}; ").format(
                b=b))
