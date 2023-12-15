#pragma once

class Common():


    kPi = 3.1415926535

    def RadiansLim(orientation):
        if orientation < 0:
            orientation = -1 * (abs(orientation) % (2 * Common.kPi)) + (2 * Common.kPi)
        elif orientation >= 2 * Common.kPi:
            orientation = orientation % (2 * Common.kPi)
        return orientation


    def RadToDegrees(rad):
        return rad * (180./Common.kPi)

    def quadrant(orientation):

        orientation += (Common.kPi*0.125)

        if orientation < 0:
            orientation = -1 * (abs(orientation) % (2 * Common.kPi)) + (2 * Common.kPi)
        elif orientation >= 2 * Common.kPi:
            orientation = orientation % (2 * Common.kPi)

        quarter = (orientation // (2*Common.kPi*0.125))%8

        return int(quarter)





if __name__ == "__main__":

    print(Common.RadiansLim(-6.3))