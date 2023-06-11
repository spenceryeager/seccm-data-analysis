# this takes a folder of SECCM kinetics data and gets kinetics info from it
# big note here: currently, this program uses UME metal electrode approximations.
# take the results here with a grain of salt, butler-volmer kinetics are not formulated for semiconductors/polymers.

import pandas as pd
import numpy as np
from bard_mirkin_kinetics import get_kinetics


def main():
    print('hello')


if __name__ == "__main__":
    main()
    