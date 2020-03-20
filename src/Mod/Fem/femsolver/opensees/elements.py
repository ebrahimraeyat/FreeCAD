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

from math import pi
import FreeCAD


__all__ = [
    'Elements',
]


class Elements(object):

    def __init__(self):

        pass

    def write_elements(self):

        self.write_section('Elements')
        self.blank_line()

        for key, nodes in self.femelement_table.items():
            stype = 'SolidSection'

            # self.write_subsection(key)

            # property      = properties[key]
            # reinforcement = property.rebar
            # elset         = property.elset

            # section       = sections[property.section]
            # stype         = section.__name__
            # geometry      = section.geometry
            # material      = materials.get(property.material)

            # if material:
            #     m_index = material.index + 1

            # s_index = section.index + 1

            # selection = property.elements if property.elements else sets[elset].selection

            # if geometry is not None:

            #     t   = geometry.get('t', None)
            #     A   = geometry.get('A', None)
            #     J   = geometry.get('J', None)
            #     Ixx = geometry.get('Ixx', None)
            #     Iyy = geometry.get('Iyy', None)
            #     E   = material.E.get('E', None)
            #     G   = material.G.get('G', None)

            # for select in selection:

            #     element = elements[select]
            #     nodes   = [str(i + 1) for i in element.nodes]
            #     no      = len(nodes)
            #     n       = select + 1
            #     ex      = element.axes.get('ex', None)
            #     ey      = element.axes.get('ey', None)
            #     ez      = element.axes.get('ez', None)

            if stype == 'SolidSection':

                if len(nodes) == 4:
                    solid = 'FourNodeTetrahedron'
                elif len(nodes) == 20:
                    solid = '20NodeBrick'
                else:
                    FreeCAD.Console.PrintError("Writing of OpenSees {} Nodes element not supported.\n".format(len(nodes))
                                               )
                self.write_line('element {0} {1} {2} {3}'.format(solid, key, ' '.join([str(i) for i in nodes]), 1))

            # =====================================================================================================
            # =====================================================================================================
            # SHELL
            # =====================================================================================================
            # =====================================================================================================

            elif stype == 'ShellSection':

                if no == 3:
                    self.write_line('element tri31 {0} {1} {2} PlaneStress {3} 0 {4} 0 0'.format(
                                    n, ' '.join(nodes), t, m_index + 1000, material.p))
                    # self.write_line('section PlateFiber {0} {1} {2}'.format(n, m_index + 1000, t))
                    # self.write_line('element ShellDKGT {0} {1} {0}'.format(n, ' '.join(nodes)))
                    # self.write_line('element ShellNLDKGT {0} {1} {0}'.format(n, ' '.join(nodes)))
                    # aparently unknown to OpenSees
                else:
                    self.write_line('section PlateFiber {0} {1} {2}'.format(n, m_index + 1000, t))
                    self.write_line('element ShellNLDKGQ {0} {1} {0}'.format(n, ' '.join(nodes)))

            elif stype == 'TrussSection':

                e = 'element corotTruss'
                self.write_line('{0} {1} {2} {3} {4} {5}'.format(e, n, nodes[0], nodes[1], A, m_index))

            elif stype == 'SpringSection':

                kx = section.stiffness.get('axial', 0)
                ky = section.stiffness.get('lateral', 0)
                kr = section.stiffness.get('rotation', 0)

                if s_index not in written_springs:

                    if kx:

                        self.write_line('uniaxialMaterial Elastic 2{0:0>3} {1}'.format(s_index, kx))
                        self.blank_line()

                    # else:
                    #     i = ' '.join([str(k) for k in section.forces['axial']])
                    #     j = ' '.join([str(k) for k in section.displacements['axial']])
                    #     f.write('uniaxialMaterial ElasticMultiLinear {0}01 -strain {1} -stress {2}\n'.format(
                    #         s_index, j, i))
                    #     f.write('#\n')

                    written_springs.append(s_index)

                orientation = ' '.join([str(k) for k in ey])

                self.write_line('element twoNodeLink {0} {1} {2} -mat 2{3:0>3} -dir 1 -orient {4}'.format(n, nodes[0], nodes[1], s_index, orientation))

            # BEAM
            else:

                e = 'element elasticBeamColumn'
                self.write_line('geomTransf Corotational {0} {1}'.format(n, ' '.join([str(i) for i in ex])))
                self.write_line('{} {} {} {} {} {} {} {} {} {} {}'.format(e, n, nodes[0], nodes[1], A, E, G, J, Ixx, Iyy, n))

        self.blank_line()
        self.blank_line()


# def _write_membranes(f, software, selection, elements, geometry, material, materials, reinforcement):

#     for select in selection:

#         element = elements[select]
#         nodes   = element.nodes
#         n  = select + 1
#         t  = geometry['t']
#         ex = element.axes.get('ex', None)
#         ey = element.axes.get('ey', None)

#         if software == 'abaqus':

#             e1 = 'element_{0}'.format(select)
#             f.write('*ELEMENT, TYPE={0}, ELSET={1}\n'.format('M3D3' if len(nodes) == 3 else 'M3D4', e1))
#             f.write('{0}, {1}\n'.format(n, ','.join([str(i + 1) for i in nodes])))

#             if ex and ey:
#                 ori = 'ORI_element_{0}'.format(select)
#                 f.write('*ORIENTATION, NAME={0}\n'.format(ori))
#                 f.write(', '.join([str(j) for j in ex]) + ', ')
#                 f.write(', '.join([str(j) for j in ey]) + '\n')
#                 f.write('**\n')
#             else:
#                 ori = None

#             f.write('*MEMBRANE SECTION, ELSET={0}, MATERIAL={1}'.format(e1, material.name))
#             if ori:
#                 f.write(', ORIENTATION={0}\n'.format(ori))
#             else:
#                 f.write('\n'.format(t))
#             f.write('{0}\n'.format(t))

#         f.write('{0}\n'.format(comments[software]))
