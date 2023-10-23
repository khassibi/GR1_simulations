class sys_ctrl(object):
    """Mealy transducer.

    Internal states are integers, the current state
    is stored in the attribute "state".
    To take a transition, call method "move".

    The names of input variables are stored in the
    attribute "input_vars".

    Automatically generated by tulip.dumpsmach on 2023-10-23 22:54:16 UTC
    To learn more about TuLiP, visit http://tulip-control.org
    """
    def __init__(self):
        self.state = 24
        self.input_vars = ['b']

    def move(self, b):
        """Given inputs, take move and return outputs.

        @rtype: dict
        @return: dictionary with keys of the output variable names:
            ['r', 'fuel', 'move']
        """
        output = dict()
        if self.state == 0:
            if (b == 1):
                self.state = 1

                output["move"] = True
                output["r"] = 'c41'
                output["fuel"] = 7
            else:
                self._error(b)
        elif self.state == 1:
            if (b == 0):
                self.state = 2

                output["move"] = True
                output["r"] = 'c31'
                output["fuel"] = 6
            elif (b == 2):
                self.state = 3

                output["move"] = True
                output["r"] = 'c31'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 2:
            if (b == 1):
                self.state = 4

                output["move"] = True
                output["r"] = 'c32'
                output["fuel"] = 5
            else:
                self._error(b)
        elif self.state == 3:
            if (b == 1):
                self.state = 4

                output["move"] = True
                output["r"] = 'c32'
                output["fuel"] = 5
            elif (b == 3):
                self.state = 5

                output["move"] = True
                output["r"] = 'c32'
                output["fuel"] = 5
            else:
                self._error(b)
        elif self.state == 4:
            if (b == 0):
                self.state = 23

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 4
            elif (b == 2):
                self.state = 7

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 5:
            if (b == 4):
                self.state = 6

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 4
            elif (b == 2):
                self.state = 7

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 6:
            if (b == 3):
                self.state = 9

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 3
            else:
                self._error(b)
        elif self.state == 7:
            if (b == 1):
                self.state = 8

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 3
            elif (b == 3):
                self.state = 9

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 3
            else:
                self._error(b)
        elif self.state == 8:
            if (b == 0):
                self.state = 22

                output["move"] = True
                output["r"] = 'c13'
                output["fuel"] = 2
            elif (b == 2):
                self.state = 11

                output["move"] = True
                output["r"] = 'c13'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 9:
            if (b == 4):
                self.state = 10

                output["move"] = True
                output["r"] = 'c13'
                output["fuel"] = 2
            elif (b == 2):
                self.state = 11

                output["move"] = True
                output["r"] = 'c13'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 10:
            if (b == 3):
                self.state = 13

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 1
            else:
                self._error(b)
        elif self.state == 11:
            if (b == 1):
                self.state = 12

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 1
            elif (b == 3):
                self.state = 13

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 1
            else:
                self._error(b)
        elif self.state == 12:
            if (b == 0):
                self.state = 21

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 0
            elif (b == 2):
                self.state = 15

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 13:
            if (b == 4):
                self.state = 14

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 0
            elif (b == 2):
                self.state = 15

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 14:
            if (b == 3):
                self.state = 17

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 15:
            if (b == 1):
                self.state = 16

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            elif (b == 3):
                self.state = 17

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 16:
            if (b == 0):
                self.state = 20

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            elif (b == 2):
                self.state = 19

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 17:
            if (b == 4):
                self.state = 18

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            elif (b == 2):
                self.state = 19

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 18:
            if (b == 3):
                self.state = 17

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 19:
            if (b == 1):
                self.state = 16

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            elif (b == 3):
                self.state = 17

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 20:
            if (b == 1):
                self.state = 16

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 21:
            if (b == 1):
                self.state = 16

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 22:
            if (b == 1):
                self.state = 12

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 1
            else:
                self._error(b)
        elif self.state == 23:
            if (b == 1):
                self.state = 8

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 3
            else:
                self._error(b)
        elif self.state == 24:
            if (b == 0):
                self.state = 0

                output["move"] = False
                output["r"] = 'c40'
                output["fuel"] = 8
            else:
                self._error(b)
        else:
            raise Exception("Unrecognized internal state: " + str(self.state))
        return output

    def _error(self, b):
        raise ValueError("Unrecognized input: " + (
            "b = {b}; ").format(
                b=b))
