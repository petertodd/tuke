# vim: tabstop=4 expandtab shiftwidth=4 fileencoding=utf8
# (c) 2008 Peter Todd <pete@petertodd.org>
#
# This program is made available under the GNU GPL version 3.0 or
# greater. See the accompanying file COPYING for details.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.

from __future__ import with_statement

from unittest import TestCase

from Tuke import Element,Id
import Tuke.context as context

import sys
import gc

bypass = None
class WrapperTest(TestCase):
    def test_Wrapped_obj_context_refcounts(self):
        """Wrapped maintains correct ref counts for obj and context"""
        def T(got,expected = True):
            self.assert_(expected == got,'got: %s  expected: %s' % (got,expected))

        a = Element(id=Id('a'))
        b = Element(id=Id('b'))

        # Check ref counting behavior
        ref_orig_a = sys.getrefcount(a)
        ref_orig_b = sys.getrefcount(a)
        w = context.Wrapped(b,a)
        T(sys.getrefcount(a) - ref_orig_a,1)
        T(sys.getrefcount(b) - ref_orig_b,1)

        del w
        T(sys.getrefcount(a) - ref_orig_a,0)
        T(sys.getrefcount(b) - ref_orig_b,0)

    def test_isinstance_Wrapped(self):
        """isinstance(Wrapped)"""
        def T(got,expected = True):
            self.assert_(expected == got,'got: %s  expected: %s' % (got,expected))

        a = Element(id=Id('a'))
        b = Element(id=Id('b'))

        w = context.Wrapped(b,a)

        T(isinstance(w,context.Wrapped))
        T(isinstance(w,Element))

    def test_Wrapped_getset_attr(self):
        """(get|set)attr on Wrapped object"""
        def T(got,expected = True):
            self.assert_(expected == got,'got: %s  expected: %s' % (got,expected))

        def R(ex,fn):
            self.assertRaises(ex,fn)

        a = Element(id=Id('a'))
        b = Element(id=Id('b'))

        w = context.Wrapped(b,a)

        R(AttributeError,lambda: w.VenezuelanBeaverCheese)
       
        n = "NorweiganJarlsburg"
        n_refc = sys.getrefcount(n)
        R(AttributeError,lambda: getattr(w,n))
        T(sys.getrefcount(n),n_refc)
       
        n = "Abuse"
        n_refc = sys.getrefcount(n)
        v = "vacuous, coffee-nosed, maloderous, pervert"
        v_refc = sys.getrefcount(n)
        setattr(w,n,"vacuous, coffee-nosed, maloderous, pervert")
        T(sys.getrefcount(n) - 1,n_refc)
        T(sys.getrefcount(v) - 1,v_refc)

        T(w.Abuse,v) 
        T(sys.getrefcount(n) - 1,n_refc)
        T(sys.getrefcount(v) - 1,v_refc)

    def test_Wrapped_data_in_out(self):
        """Wrapped data in/out wrapping"""
        def T(got,expected = True):
            self.assert_(expected == got,'got: %s  expected: %s' % (got,expected))

        # Tests both wrapping bound functions, and plain attributes at the same
        # time, in both directions at the same time. Two test vectors are
        # provided, the data in the outer context, and what it should be in the
        # inner context. The unwrapped data is then wrapped again whe nit's
        # passed back to the outer context, and checked that it matches.

        class skit(Element):
            def d(self,v):
                global bypass
                self.v = bypass
                bypass = v
                return self.v

        def T(got,expected = True):
            self.assert_(expected == got,'got: %s  expected: %s' % (repr(got),repr(expected)))

        def W(elem,
              data_in,
              unwrapped,
              equiv_in=None):
            global bypass
            if equiv_in is None:
                equiv_in = data_in

            bypass = data_in 
            r = elem.d(data_in)

            T(bypass,unwrapped)
            T(r,elem.v)
            T(r,data_in)


        a = Element(id=Id('spam'))
        b = skit(id=Id('ham'))

        w = context.Wrapped(b,a)

        W(w,0,0)
        W(w,Id('spam/ham'),Id('ham'))