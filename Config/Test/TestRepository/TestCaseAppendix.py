#!/usr/bin/env python3
"""Angela RML Interpreter - RML Condition Handling
Created by the project angela team
    http://sourceforge.net/projects/projectangela/
    http://www.projectangela.org"""
    
__license__ = "MIT"
__version__ = "$Revision: 1.0.0 $"
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

class ConditionTrueOrFalse(object):

    def __init__(self, dtParams = None, rtParams = None):
        self.dtParams = dtParams
        self.rtParams = rtParams   
        
    def execute(self, params):
        #All this script does is check the passed parameter argument map (as if the condition has a 
        # simple argument - see ConditionSet.execute() in condition.py) for an entry called "TestValue".
        # If it is present and True, then return True.  Otherwise (no argument map, argument map present, 
        # but no TestValue entry or TestValue is anything other than a unicode string saying TRUE), then 
        # return False.
        returnValue = False
        try:
            if type({}) == type(params[1]): 
                argumentMap = params[1]
                try:
                    passedParam = argumentMap[u"TestValue"]
                    if passedParam.upper() == u"TRUE":
                        returnValue = True
                except:
                    pass
        except:
            pass
        return returnValue
    
    
