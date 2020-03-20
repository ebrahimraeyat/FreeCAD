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
    'BCs',
]

dofs    = ['x',  'y',  'z',  'xx', 'yy', 'zz']


class BCs(object):

    def __init__(self):

        pass


    def write_boundary_conditions(self):

        self.write_section('Boundary conditions')
        self.blank_line()

        sets          = self.structure.sets
        steps         = self.structure.steps
        displacements = self.structure.displacements

        try:

            step = steps[self.structure.steps_order[0]]

            if isinstance(step.displacements, str):
                step.displacements = [step.displacements]

            for key in step.displacements:

                nodes      = displacements[key].nodes
                components = displacements[key].components
                nset       = nodes if isinstance(nodes, str) else None
                selection  = sets[nset].selection if isinstance(nodes, str) else nodes

                self.write_subsection(key)

                # ----------------------------------------------------------------------------
                # OpenSees
                # ----------------------------------------------------------------------------

                if self.software == 'opensees':

                    entry = ['1' if components[dof] is not None else '0' for dof in dofs[:self.ndof]]

                    for node in sorted(selection, key=int):
                        self.write_line('fix {0} {1}'.format(node + 1, ' '.join(entry)))

                # ----------------------------------------------------------------------------
                # Abaqus
                # ----------------------------------------------------------------------------

                elif self.software == 'abaqus':

                    self.write_line('*BOUNDARY')
                    self.blank_line()

                    for c, dof in enumerate(dofs, 1):
                        if components[dof] is not None:
                            if nset:
                                self.write_line('{0}, {1}, {1}, {2}'.format(nset, c, components[dof]))
                            else:
                                for node in sorted(selection, key=int):
                                    self.write_line('{0}, {1}, {1}, {2}'.format(node + 1, c, components[dof]))

                # ----------------------------------------------------------------------------
                # Ansys
                # ----------------------------------------------------------------------------

                elif self.software == 'ansys':

                    pass

                self.blank_line()

        except:

            print('***** Error writing boundary conditions, check Step exists in structure.steps_order[0] *****')

        self.blank_line()
        self.blank_line()
