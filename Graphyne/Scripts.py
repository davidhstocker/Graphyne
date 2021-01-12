#!/usr/bin/env python2
"""Angela RML Interpreter - RML Condition Handling
Created by the project angela team
    http://sourceforge.net/projects/projectangela/
    http://www.projectangela.org"""
    
__license__ = "GPL"
__version__ = "$Revision: 0.1 $"
__author__ = 'David Stocker'


# ***** BEGIN GPL LICENSE BLOCK *****
#
# Module copyright (C) David Stocker 
#
# This module is part of the Angela RML Engine.

# Angela is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Angela is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Angela.  If not, see <http://www.gnu.org/licenses/>.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------

import Graphyne.Scripting


class ConditionTrue(Graphyne.Scripting.StateEventScript):

    def execute(self, entityID, params):
        #always return True
        return True
    
    
    
class ConditionFalse(Graphyne.Scripting.StateEventScript):  
        
    def execute(self, entityID, params):
        #always return False
        return False