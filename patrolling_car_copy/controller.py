class sys_ctrl(object):
    """Mealy transducer.

    Internal states are integers, the current state
    is stored in the attribute "state".
    To take a transition, call method "move".

    The names of input variables are stored in the
    attribute "input_vars".

    Automatically generated by tulip.dumpsmach on 2023-10-23 22:51:36 UTC
    To learn more about TuLiP, visit http://tulip-control.org
    """
    def __init__(self):
        self.state = 81
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
                output["fuel"] = 13
            elif (b == 3):
                self.state = 2

                output["move"] = False
                output["r"] = 'c40'
                output["fuel"] = 14
            else:
                self._error(b)
        elif self.state == 1:
            if (b == 0):
                self.state = 80

                output["move"] = True
                output["r"] = 'c31'
                output["fuel"] = 12
            elif (b == 2):
                self.state = 6

                output["move"] = True
                output["r"] = 'c31'
                output["fuel"] = 12
            else:
                self._error(b)
        elif self.state == 2:
            if (b == 4):
                self.state = 3

                output["move"] = False
                output["r"] = 'c40'
                output["fuel"] = 14
            elif (b == 2):
                self.state = 0

                output["move"] = False
                output["r"] = 'c40'
                output["fuel"] = 14
            else:
                self._error(b)
        elif self.state == 3:
            if (b == 3):
                self.state = 4

                output["move"] = True
                output["r"] = 'c41'
                output["fuel"] = 13
            else:
                self._error(b)
        elif self.state == 4:
            if (b == 4):
                self.state = 5

                output["move"] = True
                output["r"] = 'c31'
                output["fuel"] = 12
            elif (b == 2):
                self.state = 6

                output["move"] = True
                output["r"] = 'c31'
                output["fuel"] = 12
            else:
                self._error(b)
        elif self.state == 5:
            if (b == 3):
                self.state = 11

                output["move"] = True
                output["r"] = 'c32'
                output["fuel"] = 11
            else:
                self._error(b)
        elif self.state == 6:
            if (b == 1):
                self.state = 7

                output["move"] = True
                output["r"] = 'c32'
                output["fuel"] = 11
            elif (b == 3):
                self.state = 8

                output["move"] = False
                output["r"] = 'c31'
                output["fuel"] = 12
            else:
                self._error(b)
        elif self.state == 7:
            if (b == 0):
                self.state = 79

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 10
            elif (b == 2):
                self.state = 13

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 10
            else:
                self._error(b)
        elif self.state == 8:
            if (b == 4):
                self.state = 9

                output["move"] = False
                output["r"] = 'c31'
                output["fuel"] = 12
            elif (b == 2):
                self.state = 10

                output["move"] = False
                output["r"] = 'c31'
                output["fuel"] = 12
            else:
                self._error(b)
        elif self.state == 9:
            if (b == 3):
                self.state = 11

                output["move"] = True
                output["r"] = 'c32'
                output["fuel"] = 11
            else:
                self._error(b)
        elif self.state == 10:
            if (b == 1):
                self.state = 7

                output["move"] = True
                output["r"] = 'c32'
                output["fuel"] = 11
            elif (b == 3):
                self.state = 8

                output["move"] = False
                output["r"] = 'c31'
                output["fuel"] = 12
            else:
                self._error(b)
        elif self.state == 11:
            if (b == 4):
                self.state = 12

                output["move"] = True
                output["r"] = 'c31'
                output["fuel"] = 10
            elif (b == 2):
                self.state = 13

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 10
            else:
                self._error(b)
        elif self.state == 12:
            if (b == 3):
                self.state = 75

                output["move"] = True
                output["r"] = 'c32'
                output["fuel"] = 9
            else:
                self._error(b)
        elif self.state == 13:
            if (b == 1):
                self.state = 14

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 9
            elif (b == 3):
                self.state = 15

                output["move"] = False
                output["r"] = 'c22'
                output["fuel"] = 10
            else:
                self._error(b)
        elif self.state == 14:
            if (b == 0):
                self.state = 74

                output["move"] = True
                output["r"] = 'c13'
                output["fuel"] = 8
            elif (b == 2):
                self.state = 20

                output["move"] = True
                output["r"] = 'c24'
                output["fuel"] = 8
            else:
                self._error(b)
        elif self.state == 15:
            if (b == 4):
                self.state = 16

                output["move"] = False
                output["r"] = 'c22'
                output["fuel"] = 10
            elif (b == 2):
                self.state = 17

                output["move"] = False
                output["r"] = 'c22'
                output["fuel"] = 10
            else:
                self._error(b)
        elif self.state == 16:
            if (b == 3):
                self.state = 18

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 9
            else:
                self._error(b)
        elif self.state == 17:
            if (b == 1):
                self.state = 14

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 9
            elif (b == 3):
                self.state = 15

                output["move"] = False
                output["r"] = 'c22'
                output["fuel"] = 10
            else:
                self._error(b)
        elif self.state == 18:
            if (b == 4):
                self.state = 19

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 8
            elif (b == 2):
                self.state = 20

                output["move"] = True
                output["r"] = 'c24'
                output["fuel"] = 8
            else:
                self._error(b)
        elif self.state == 19:
            if (b == 3):
                self.state = 32

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 7
            else:
                self._error(b)
        elif self.state == 20:
            if (b == 1):
                self.state = 21

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 7
            elif (b == 3):
                self.state = 22

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 8
            else:
                self._error(b)
        elif self.state == 21:
            if (b == 0):
                self.state = 25

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 6
            elif (b == 2):
                self.state = 26

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 22:
            if (b == 4):
                self.state = 23

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 8
            elif (b == 2):
                self.state = 24

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 8
            else:
                self._error(b)
        elif self.state == 23:
            if (b == 3):
                self.state = 22

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 8
            else:
                self._error(b)
        elif self.state == 24:
            if (b == 1):
                self.state = 21

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 7
            elif (b == 3):
                self.state = 22

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 8
            else:
                self._error(b)
        elif self.state == 25:
            if (b == 1):
                self.state = 27

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 26:
            if (b == 1):
                self.state = 27

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 6
            elif (b == 3):
                self.state = 28

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 27:
            if (b == 0):
                self.state = 31

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 6
            elif (b == 2):
                self.state = 30

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 28:
            if (b == 4):
                self.state = 29

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 6
            elif (b == 2):
                self.state = 30

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 29:
            if (b == 3):
                self.state = 28

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 30:
            if (b == 1):
                self.state = 27

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 6
            elif (b == 3):
                self.state = 28

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 31:
            if (b == 1):
                self.state = 27

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 32:
            if (b == 4):
                self.state = 33

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 6
            elif (b == 2):
                self.state = 34

                output["move"] = True
                output["r"] = 'c24'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 33:
            if (b == 3):
                self.state = 46

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 5
            else:
                self._error(b)
        elif self.state == 34:
            if (b == 1):
                self.state = 35

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 5
            elif (b == 3):
                self.state = 36

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 35:
            if (b == 0):
                self.state = 39

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 4
            elif (b == 2):
                self.state = 40

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 36:
            if (b == 4):
                self.state = 37

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 6
            elif (b == 2):
                self.state = 38

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 37:
            if (b == 3):
                self.state = 36

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 38:
            if (b == 1):
                self.state = 35

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 5
            elif (b == 3):
                self.state = 36

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 39:
            if (b == 1):
                self.state = 41

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 40:
            if (b == 1):
                self.state = 41

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 4
            elif (b == 3):
                self.state = 42

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 41:
            if (b == 0):
                self.state = 45

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 4
            elif (b == 2):
                self.state = 44

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 42:
            if (b == 4):
                self.state = 43

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 4
            elif (b == 2):
                self.state = 44

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 43:
            if (b == 3):
                self.state = 42

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 44:
            if (b == 1):
                self.state = 41

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 4
            elif (b == 3):
                self.state = 42

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 45:
            if (b == 1):
                self.state = 41

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 46:
            if (b == 4):
                self.state = 47

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 4
            elif (b == 2):
                self.state = 48

                output["move"] = True
                output["r"] = 'c24'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 47:
            if (b == 3):
                self.state = 60

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 3
            else:
                self._error(b)
        elif self.state == 48:
            if (b == 1):
                self.state = 49

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 3
            elif (b == 3):
                self.state = 50

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 49:
            if (b == 0):
                self.state = 53

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 2
            elif (b == 2):
                self.state = 54

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 50:
            if (b == 4):
                self.state = 51

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 4
            elif (b == 2):
                self.state = 52

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 51:
            if (b == 3):
                self.state = 50

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 52:
            if (b == 1):
                self.state = 49

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 3
            elif (b == 3):
                self.state = 50

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 4
            else:
                self._error(b)
        elif self.state == 53:
            if (b == 1):
                self.state = 55

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 54:
            if (b == 1):
                self.state = 55

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 2
            elif (b == 3):
                self.state = 56

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 55:
            if (b == 0):
                self.state = 59

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 2
            elif (b == 2):
                self.state = 58

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 56:
            if (b == 4):
                self.state = 57

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 2
            elif (b == 2):
                self.state = 58

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 57:
            if (b == 3):
                self.state = 56

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 58:
            if (b == 1):
                self.state = 55

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 2
            elif (b == 3):
                self.state = 56

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 59:
            if (b == 1):
                self.state = 55

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 60:
            if (b == 4):
                self.state = 61

                output["move"] = True
                output["r"] = 'c24'
                output["fuel"] = 2
            elif (b == 2):
                self.state = 62

                output["move"] = True
                output["r"] = 'c24'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 61:
            if (b == 3):
                self.state = 64

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 62:
            if (b == 1):
                self.state = 63

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 1
            elif (b == 3):
                self.state = 64

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 63:
            if (b == 0):
                self.state = 67

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 0
            elif (b == 2):
                self.state = 68

                output["move"] = True
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 64:
            if (b == 4):
                self.state = 65

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 2
            elif (b == 2):
                self.state = 66

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 65:
            if (b == 3):
                self.state = 64

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 66:
            if (b == 1):
                self.state = 63

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 1
            elif (b == 3):
                self.state = 64

                output["move"] = False
                output["r"] = 'c24'
                output["fuel"] = 2
            else:
                self._error(b)
        elif self.state == 67:
            if (b == 1):
                self.state = 69

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 68:
            if (b == 1):
                self.state = 69

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            elif (b == 3):
                self.state = 70

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 69:
            if (b == 0):
                self.state = 73

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            elif (b == 2):
                self.state = 72

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 70:
            if (b == 4):
                self.state = 71

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            elif (b == 2):
                self.state = 72

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 71:
            if (b == 3):
                self.state = 70

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 72:
            if (b == 1):
                self.state = 69

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            elif (b == 3):
                self.state = 70

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 73:
            if (b == 1):
                self.state = 69

                output["move"] = False
                output["r"] = 'c04'
                output["fuel"] = 0
            else:
                self._error(b)
        elif self.state == 74:
            if (b == 1):
                self.state = 21

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 7
            else:
                self._error(b)
        elif self.state == 75:
            if (b == 4):
                self.state = 19

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 8
            elif (b == 2):
                self.state = 76

                output["move"] = True
                output["r"] = 'c22'
                output["fuel"] = 8
            else:
                self._error(b)
        elif self.state == 76:
            if (b == 1):
                self.state = 77

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 7
            elif (b == 3):
                self.state = 32

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 7
            else:
                self._error(b)
        elif self.state == 77:
            if (b == 0):
                self.state = 78

                output["move"] = True
                output["r"] = 'c13'
                output["fuel"] = 6
            elif (b == 2):
                self.state = 34

                output["move"] = True
                output["r"] = 'c24'
                output["fuel"] = 6
            else:
                self._error(b)
        elif self.state == 78:
            if (b == 1):
                self.state = 35

                output["move"] = True
                output["r"] = 'c14'
                output["fuel"] = 5
            else:
                self._error(b)
        elif self.state == 79:
            if (b == 1):
                self.state = 14

                output["move"] = True
                output["r"] = 'c23'
                output["fuel"] = 9
            else:
                self._error(b)
        elif self.state == 80:
            if (b == 1):
                self.state = 7

                output["move"] = True
                output["r"] = 'c32'
                output["fuel"] = 11
            else:
                self._error(b)
        elif self.state == 81:
            if (b == 2):
                self.state = 0

                output["move"] = False
                output["r"] = 'c40'
                output["fuel"] = 14
            else:
                self._error(b)
        else:
            raise Exception("Unrecognized internal state: " + str(self.state))
        return output

    def _error(self, b):
        raise ValueError("Unrecognized input: " + (
            "b = {b}; ").format(
                b=b))
