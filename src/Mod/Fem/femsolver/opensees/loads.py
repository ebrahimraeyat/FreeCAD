# ***************************************************************************
# *   Copyright (c) 2020 Raeyat Roknabadi Ebrahim <ebe79442114@gmail.com>   *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************


__all__ = [
    'Loads',
]


dofs = ['x', 'y', 'z', 'xx', 'yy', 'zz']


class Loads(object):

    def __init__(self):

        pass

    def write_loads(self):

        self.write_section('Loads')
        self.blank_line()
        print(self.force_objects)

        for femobj in self.force_objects:
            # femobj --> dict, FreeCAD document object is femobj["Object"]
            direction_vec = femobj["Object"].DirectionVector
            print(direction_vec)
            print(femobj)
            for ref_shape in femobj["NodeLoadTable"]:
                for n in sorted(ref_shape[1]):
                    node_load = ref_shape[1][n]
                    # if (direction_vec.x != 0.0):
                    v1 = direction_vec.x * node_load
                    #     constraints_data.append((n, str(n) + "  1  1  " + str(v1) + "\n"))
                    # if (direction_vec.y != 0.0):
                    v2 = direction_vec.y * node_load
                    #     constraints_data.append((n, str(n) + "  2  1  " + str(v2) + "\n"))
                    # if (direction_vec.z != 0.0):
                    v3 = direction_vec.z * node_load
                    # constraints_data.append((n, str(n) + "  3  1  " + str(v3) + "\n"))

                    self.write_subsection(k)

                    # load = loads[k]
                    ltype = "PointLoad"
                    # com = getattr(load, 'components', None)
                    # axes = getattr(load, 'axes', None)
                    # nodes = getattr(load, 'nodes', None)
                    # fact = factor.get(k, 1.0) if isinstance(factor, dict) else factor

                    # PointLoad
                    # ---------

                    if ltype == 'PointLoad':

                        self.write_line('load {0} {1} {2} {3}'.format(n, v1, v2, v3))

                    # Gravity
                    # -------

                    elif ltype == 'GravityLoad':

                        for nkey, node in self.structure.nodes.items():

                            W = - fact * node.mass * 9.81
                            self.write_line('load {0} {1} {2} {3}'.format(nkey + 1, gx * W, gy * W, gz * W))

                    # LineLoad
                    # --------

                    elif ltype == 'LineLoad':

                        if axes == 'global':

                            raise NotImplementedError

                        elif axes == 'local':

                            elements = ' '.join([str(i + 1) for i in sets[k].selection])
                            lx = -com['x'] * fact
                            ly = -com['y'] * fact
                            self.write_line('eleLoad -ele {0} -type -beamUniform {1} {2}'.format(elements, ly, lx))

                    self.blank_line()

                self.blank_line()
                self.blank_line()
