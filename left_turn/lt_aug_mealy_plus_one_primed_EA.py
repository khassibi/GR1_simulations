class Strategy(object):
    """Mealy transducer.

    Internal states are integers, the current state
    is stored in the attribute "state".
    To take a transition, call method "move".

    The names of input variables are stored in the
    attribute "input_vars".

    Automatically generated by tulip.dumpsmach on 2023-09-09 06:39:10 UTC
    To learn more about TuLiP, visit http://tulip-control.org
    """
    def __init__(self):
        self.state = 35
        self.input_vars = ['vh', 'light']

    def move(self, vh, light):
        """Given inputs, take move and return outputs.

        @rtype: dict
        @return: dictionary with keys of the output variable names:
            ['a7', 'a8', 'a4', 'a9', 'loc']
        """
        output = dict()
        if self.state == 0:
            if (vh == 2) and (light == 'g2'):
                self.state = 1

                output["a7"] = False
                output["a8"] = True
                output["a4"] = False
                output["a9"] = False
                output["loc"] = 'c8'
            elif (vh == 3) and (light == 'g2'):
                self.state = 2

                output["a7"] = False
                output["a8"] = True
                output["a4"] = False
                output["a9"] = False
                output["loc"] = 'c8'
            else:
                self._error(vh, light)
        elif self.state == 1:
            if (vh == 2) and (light == 'g3'):
                self.state = 28

                output["a7"] = False
                output["a8"] = False
                output["a4"] = True
                output["a9"] = False
                output["loc"] = 'c4'
            elif (vh == 3) and (light == 'g3'):
                self.state = 4

                output["a7"] = False
                output["a8"] = False
                output["a4"] = True
                output["a9"] = False
                output["loc"] = 'c4'
            else:
                self._error(vh, light)
        elif self.state == 2:
            if (vh == 4) and (light == 'g3'):
                self.state = 3

                output["a7"] = False
                output["a8"] = True
                output["a4"] = False
                output["a9"] = False
                output["loc"] = 'c8'
            elif (vh == 3) and (light == 'g3'):
                self.state = 4

                output["a7"] = False
                output["a8"] = False
                output["a4"] = True
                output["a9"] = False
                output["loc"] = 'c4'
            else:
                self._error(vh, light)
        elif self.state == 3:
            if (vh == 4) and (light == 'y1'):
                self.state = 25

                output["a7"] = False
                output["a8"] = True
                output["a4"] = False
                output["a9"] = False
                output["loc"] = 'c8'
            elif (vh == 5) and (light == 'y1'):
                self.state = 26

                output["a7"] = False
                output["a8"] = False
                output["a4"] = True
                output["a9"] = False
                output["loc"] = 'c4'
            else:
                self._error(vh, light)
        elif self.state == 4:
            if (vh == 4) and (light == 'y1'):
                self.state = 5

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'y1'):
                self.state = 6

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 5:
            if (vh == 5) and (light == 'y2'):
                self.state = 17

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 6:
            if (vh == 3) and (light == 'y2'):
                self.state = 7

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 7:
            if (vh == 3) and (light == 'r'):
                self.state = 8

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 8:
            if (vh == 4) and (light == 'g1'):
                self.state = 9

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'g1'):
                self.state = 10

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'r'):
                self.state = 8

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 9:
            if (vh == 4) and (light == 'g2'):
                self.state = 11

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 5) and (light == 'g2'):
                self.state = 24

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 10:
            if (vh == 4) and (light == 'g2'):
                self.state = 11

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'g2'):
                self.state = 12

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 11:
            if (vh == 4) and (light == 'g3'):
                self.state = 13

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 5) and (light == 'g3'):
                self.state = 23

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 12:
            if (vh == 4) and (light == 'g3'):
                self.state = 13

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'g3'):
                self.state = 14

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 13:
            if (vh == 4) and (light == 'y1'):
                self.state = 5

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 5) and (light == 'y1'):
                self.state = 15

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 14:
            if (vh == 4) and (light == 'y1'):
                self.state = 5

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'y1'):
                self.state = 6

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 15:
            if (vh == 6) and (light == 'y2'):
                self.state = 16

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 5) and (light == 'y2'):
                self.state = 17

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 16:
            if (vh == 6) and (light == 'r'):
                self.state = 18

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 17:
            if (vh == 6) and (light == 'r'):
                self.state = 18

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 18:
            if (vh == 6) and (light == 'g1'):
                self.state = 19

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 6) and (light == 'r'):
                self.state = 18

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 19:
            if (vh == 6) and (light == 'g2'):
                self.state = 20

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 20:
            if (vh == 6) and (light == 'g3'):
                self.state = 21

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 21:
            if (vh == 6) and (light == 'y1'):
                self.state = 22

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 22:
            if (vh == 6) and (light == 'y2'):
                self.state = 16

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 23:
            if (vh == 6) and (light == 'y1'):
                self.state = 22

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 5) and (light == 'y1'):
                self.state = 15

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 24:
            if (vh == 6) and (light == 'g3'):
                self.state = 21

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 5) and (light == 'g3'):
                self.state = 23

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 25:
            if (vh == 5) and (light == 'y2'):
                self.state = 27

                output["a7"] = False
                output["a8"] = False
                output["a4"] = True
                output["a9"] = False
                output["loc"] = 'c4'
            else:
                self._error(vh, light)
        elif self.state == 26:
            if (vh == 6) and (light == 'y2'):
                self.state = 16

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 5) and (light == 'y2'):
                self.state = 17

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 27:
            if (vh == 6) and (light == 'r'):
                self.state = 18

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 28:
            if (vh == 2) and (light == 'y1'):
                self.state = 29

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'y1'):
                self.state = 6

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 29:
            if (vh == 2) and (light == 'y2'):
                self.state = 30

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'y2'):
                self.state = 7

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 30:
            if (vh == 2) and (light == 'r'):
                self.state = 31

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'r'):
                self.state = 8

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 31:
            if (vh == 2) and (light == 'g1'):
                self.state = 32

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'g1'):
                self.state = 10

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 2) and (light == 'r'):
                self.state = 31

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'r'):
                self.state = 8

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 32:
            if (vh == 2) and (light == 'g2'):
                self.state = 33

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'g2'):
                self.state = 12

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 33:
            if (vh == 2) and (light == 'g3'):
                self.state = 34

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'g3'):
                self.state = 14

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 34:
            if (vh == 2) and (light == 'y1'):
                self.state = 29

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            elif (vh == 3) and (light == 'y1'):
                self.state = 6

                output["a7"] = False
                output["a8"] = False
                output["a4"] = False
                output["a9"] = True
                output["loc"] = 'c9'
            else:
                self._error(vh, light)
        elif self.state == 35:
            if (vh == 2) and (light == 'g1'):
                self.state = 0

                output["a7"] = True
                output["a8"] = False
                output["a4"] = False
                output["a9"] = False
                output["loc"] = 'c7'
            else:
                self._error(vh, light)
        else:
            raise Exception("Unrecognized internal state: " + str(self.state))
        return output

    def _error(self, vh, light):
        raise ValueError("Unrecognized input: " + (
            "vh = {vh}; "
            "light = {light}; ").format(
                vh=vh,
                light=light))
