"""INSEE-PCS is a set of tools to easily use the PCS system of INSEE.

PCS ("Professions et catégories socioprofessionnelles") is
a classification system created by INSEE ("Institut National
de la Statistique et des Études Économiques") to do statistics
with the jobs of the population in four levels.

This package allows you to get their descriptions and levels, and to
store the PCS of someone in a Django project with four dedicated fields.

Usage:
>>> import insee_pcs
>>> pcs = insee_pcs.get_PCS(4, "382b")
>>> print(pcs, pcs.level, pcs.description)
<PCS '382b' (level 4)> 4 "Architectes salariés"

The code of this module is under the AGPLv3.
The database it uses is copyright free, according to
the INSEE website : https://www.insee.fr/fr/information/2381863
"""

import sys as _sys
import os as _os
_sys.path.append(_os.path.dirname(_os.path.abspath(__file__)))

from main import PCS, get_PCS

__version__ = "0.1.0"
__appname__ = "insee-pcs"
__author__ = "rezemika <reze.mika@gmail.com>"
__licence__ = "AGPLv3"
