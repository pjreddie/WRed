from diffpy.Structure.SymmetryUtilities import ExpandAsymmetricUnit
positions = [[0.1, 0.2, 0.2]]

from diffpy.Structure.SpaceGroups import GetSpaceGroup
sg225 = GetSpaceGroup('Fm-3m')

eau = ExpandAsymmetricUnit(sg225, positions)

pos_expanded=eau.positions[0]