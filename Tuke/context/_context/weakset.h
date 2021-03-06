// ### BOILERPLATE ###
// Tuke - Electrical Design Automation toolset
// Copyright (C) 2008 Peter Todd <pete@petertodd.org>
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
// ### BOILERPLATE ###

#ifndef WEAKSET_H
#define WEAKSET_H

extern PyTypeObject WeakSetType;

typedef struct {
    PyObject_HEAD
    PyObject *in_weakreflist;

    // The underlying PySetObject
    PyObject *set;

    // A premade weakref pointing to ourselves.
    PyObject *selfref;
} WeakSet;

PyObject *WeakSet_New(void);

int WeakSet_Add(PyObject *self,PyObject *key);
int WeakSet_Contains(PyObject *self,PyObject *key);

PyObject *initweakset(void);

// Local Variables:
// mode: C
// fill-column: 76
// c-file-style: "gnu"
// indent-tabs-mode: nil
// End:
// vim: et:sw=4:sts=4:ts=4:cino=>4s,{s,\:s,+s,t0,g0,^-4,e-4,n-4,p4s,(0,=s:
#endif
