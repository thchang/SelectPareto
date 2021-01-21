'''This Python code is an automatically generated wrapper
for Fortran code made by 'fmodpy'. The original documentation
for the Fortran source code follows.

! TITLE:
!   Fast sort (and select)
!
!
! PURPOSE:
!  This file contains the following modules and subroutines for quickly
!  sorting (either partially or fully) arrays in Fortran.
!
!   SWAP
!    SWAP_I64
!    SWAP_R64
!
!   FAST_SELECT
!    ARGSELECT_R64
!    ARGSELECT_I64
!
!   FAST_SORT
!    ARGSORT_R64
!    ARGPARTITION_R64
!    INSERTION_ARGSORT_R64
!
! Respectively, the purposes of the three modules are:
!
!   SWAP - Swap the value of two variables through a temporary.
!
!   FAST_SELECT - Do a fast "select" operation on an array of numbers,
!     resulting in the value at index K being as if the entire array
!     were sorted. All values before K will be less or equal, but not
!     sorted. All values after K will be greater or equal, but not
!     sorted. This operation is O(N).
!
!   FAST_SORT - Do a fast "sort" operation that uses methods
!     appropriate for the size of the array that will maximize speed.
!
!
! AUTHOR:
!   Thomas C.H. Lux (thomas.ch.lux@gmail.com)
!
!
! NOTES:
!   The algorithm for SELECT was inspired by the Floyd-Rivest method
!   of performing selection. The algorithm for SORT was inspired by
!   Data Structures and Algorithms Analysis by Dr. Clifford A. Shaffer
!   (Virginia Polytechnic Institute and State University).
'''

import os
import ctypes
import numpy

# --------------------------------------------------------------------
#               CONFIGURATION
# 
_verbose = True
_fort_compiler = "gfortran"
_shared_object_name = "fast_sort.so"
_this_directory = os.path.dirname(os.path.abspath(__file__))
_path_to_lib = os.path.join(_this_directory, _shared_object_name)
_compile_options = ['-fPIC', '-shared', '-O3']
_ordered_dependencies = ['fast_sort.f90', 'fast_sort_c_wrapper.f90']
# 
# --------------------------------------------------------------------
#               AUTO-COMPILING
#
# Try to import the existing object. If that fails, recompile and then try.
try:
    clib = ctypes.CDLL(_path_to_lib)
except:
    # Remove the shared object if it exists, because it is faulty.
    if os.path.exists(_shared_object_name):
        os.remove(_shared_object_name)
    # Compile a new shared object.
    _command = " ".join([_fort_compiler] + _compile_options + ["-o", _shared_object_name] + _ordered_dependencies)
    if _verbose:
        print("Running system command with arguments")
        print("  ", _command)
    # Run the compilation command.
    import subprocess
    subprocess.run(_command, shell=True, cwd=_this_directory)
    # Import the shared object file as a C library with ctypes.
    clib = ctypes.CDLL(_path_to_lib)
# --------------------------------------------------------------------


def argselect_r64(values, indices, k, divisor=None, max_size=None):
    '''! ------------------------------------------------------------------
!                       FastSelect method
!
! Given VALUES list of numbers, rearrange the elements of VALUES
! such that the element at index K has rank K (holds its same
! location as if all of VALUES were sorted). Symmetrically rearrange
! array INDICES to keep track of prior indices.
!
! This algorithm uses the same conceptual approach as Floyd-Rivest,
! but instead of standard-deviation based selection of bounds for
! recursion, a rank-based method is used to pick the subset of
! values that is searched. This simplifies the code and improves
! interpretability, while achieving the same tunable performance.
!
! Arguments:
!
!   VALUES   --  A 1D array of real numbers.
!   INDICES  --  A 1D array of original indices for elements of VALUES.
!   K        --  A positive integer for the rank index about which
!                VALUES should be rearranged.
! Optional:
!
!   DIVISOR  --  A positive integer >= 2 that represents the
!                division factor used for large VALUES arrays.
!   MAX_SIZE --  An integer >= DIVISOR that represents the largest
!                sized VALUES for which the worst-case pivot value
!                selection is tolerable. A worst-case pivot causes
!                O( SIZE(VALUES)^2 ) runtime. This value should be
!                determined heuristically based on compute hardware.
!
! Output:
!
!   The elements of the array VALUES are rearranged such that the
!   element at position VALUES(K) is in the same location it would
!   be if all of VALUES were in sorted order. Also known as,
!   VALUES(K) has rank K.
!
! Arguments'''

    # Setting up "values"
    if ((not issubclass(type(values), numpy.ndarray)) or
        (not numpy.asarray(values).flags.f_contiguous) or
        (not (values.dtype == numpy.dtype(ctypes.c_double)))):
        import warnings
        warnings.warn("The provided argument 'values' was not an f_contiguous NumPy array of type 'ctypes.c_double' (or equivalent). Automatically converting (probably creating a full copy).")
        values = numpy.asarray(values, dtype=ctypes.c_double, order='F')
    values_dim_1 = ctypes.c_int(values.shape[0])

    # Setting up "indices"
    if ((not issubclass(type(indices), numpy.ndarray)) or
        (not numpy.asarray(indices).flags.f_contiguous) or
        (not (indices.dtype == numpy.dtype(ctypes.c_long)))):
        import warnings
        warnings.warn("The provided argument 'indices' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
        indices = numpy.asarray(indices, dtype=ctypes.c_long, order='F')
    indices_dim_1 = ctypes.c_int(indices.shape[0])

    # Setting up "k"
    if (type(k) is not ctypes.c_long): k = ctypes.c_long(k)

    # Setting up "divisor"
    divisor_present = ctypes.c_bool(True)
    if (divisor is None):
        divisor_present = ctypes.c_bool(False)
        divisor = ctypes.c_long()
    if (type(divisor) is not ctypes.c_long): divisor = ctypes.c_long(divisor)

    # Setting up "max_size"
    max_size_present = ctypes.c_bool(True)
    if (max_size is None):
        max_size_present = ctypes.c_bool(False)
        max_size = ctypes.c_long()
    if (type(max_size) is not ctypes.c_long): max_size = ctypes.c_long(max_size)

    # Call C-accessible Fortran wrapper.
    clib.c_argselect_r64(ctypes.byref(values_dim_1), ctypes.c_void_p(values.ctypes.data), ctypes.byref(indices_dim_1), ctypes.c_void_p(indices.ctypes.data), ctypes.byref(k), ctypes.byref(divisor_present), ctypes.byref(divisor), ctypes.byref(max_size_present), ctypes.byref(max_size))

    # Return final results, 'INTENT(OUT)' arguments only.
    return values, indices

    
def argselect_i64(values, indices, k, divisor=None, max_size=None):
    '''! Arguments'''

    # Setting up "values"
    if ((not issubclass(type(values), numpy.ndarray)) or
        (not numpy.asarray(values).flags.f_contiguous) or
        (not (values.dtype == numpy.dtype(ctypes.c_long)))):
        import warnings
        warnings.warn("The provided argument 'values' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
        values = numpy.asarray(values, dtype=ctypes.c_long, order='F')
    values_dim_1 = ctypes.c_int(values.shape[0])

    # Setting up "indices"
    if ((not issubclass(type(indices), numpy.ndarray)) or
        (not numpy.asarray(indices).flags.f_contiguous) or
        (not (indices.dtype == numpy.dtype(ctypes.c_long)))):
        import warnings
        warnings.warn("The provided argument 'indices' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
        indices = numpy.asarray(indices, dtype=ctypes.c_long, order='F')
    indices_dim_1 = ctypes.c_int(indices.shape[0])

    # Setting up "k"
    if (type(k) is not ctypes.c_long): k = ctypes.c_long(k)

    # Setting up "divisor"
    divisor_present = ctypes.c_bool(True)
    if (divisor is None):
        divisor_present = ctypes.c_bool(False)
        divisor = ctypes.c_long()
    if (type(divisor) is not ctypes.c_long): divisor = ctypes.c_long(divisor)

    # Setting up "max_size"
    max_size_present = ctypes.c_bool(True)
    if (max_size is None):
        max_size_present = ctypes.c_bool(False)
        max_size = ctypes.c_long()
    if (type(max_size) is not ctypes.c_long): max_size = ctypes.c_long(max_size)

    # Call C-accessible Fortran wrapper.
    clib.c_argselect_i64(ctypes.byref(values_dim_1), ctypes.c_void_p(values.ctypes.data), ctypes.byref(indices_dim_1), ctypes.c_void_p(indices.ctypes.data), ctypes.byref(k), ctypes.byref(divisor_present), ctypes.byref(divisor), ctypes.byref(max_size_present), ctypes.byref(max_size))

    # Return final results, 'INTENT(OUT)' arguments only.
    return values, indices


def argsort_r64(values, indices, min_size=None):
    '''! ------------------------------------------------------------------
!                         FastSort
!
! This routine uses a combination of QuickSort (with modestly
! intelligent pivot selection) and Insertion Sort (for small arrays)
! to achieve very fast average case sort times for both random and
! partially sorted data. The pivot is selected for QuickSort as the
! median of the first, middle, and last values in the array.
!
! Arguments:
!
!   VALUES   --  A 1D array of real numbers.
!   INDICES  --  A 1D array of original indices for elements of VALUES.
!
! Optional:
!
!   MIN_SIZE --  An positive integer that represents the largest
!                sized VALUES for which a partition about a pivot
!                is used to reduce the size of a an unsorted array.
!                Any size less than this will result in the use of
!                INSERTION_ARGSORT instead of ARGPARTITION.
!
! Output:
!
!   The elements of the array VALUES are sorted and all elements of
!   INDICES are sorted symmetrically (given INDICES = 1, ...,
!   SIZE(VALUES) beforehand, final INDICES will show original index
!   of each element of VALUES before the sort operation).
!'''

    # Setting up "values"
    if ((not issubclass(type(values), numpy.ndarray)) or
        (not numpy.asarray(values).flags.f_contiguous) or
        (not (values.dtype == numpy.dtype(ctypes.c_double)))):
        import warnings
        warnings.warn("The provided argument 'values' was not an f_contiguous NumPy array of type 'ctypes.c_double' (or equivalent). Automatically converting (probably creating a full copy).")
        values = numpy.asarray(values, dtype=ctypes.c_double, order='F')
    values_dim_1 = ctypes.c_int(values.shape[0])

    # Setting up "indices"
    if ((not issubclass(type(indices), numpy.ndarray)) or
        (not numpy.asarray(indices).flags.f_contiguous) or
        (not (indices.dtype == numpy.dtype(ctypes.c_long)))):
        import warnings
        warnings.warn("The provided argument 'indices' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
        indices = numpy.asarray(indices, dtype=ctypes.c_long, order='F')
    indices_dim_1 = ctypes.c_int(indices.shape[0])

    # Setting up "min_size"
    min_size_present = ctypes.c_bool(True)
    if (min_size is None):
        min_size_present = ctypes.c_bool(False)
        min_size = ctypes.c_long()
    if (type(min_size) is not ctypes.c_long): min_size = ctypes.c_long(min_size)

    # Call C-accessible Fortran wrapper.
    clib.c_argsort_r64(ctypes.byref(values_dim_1), ctypes.c_void_p(values.ctypes.data), ctypes.byref(indices_dim_1), ctypes.c_void_p(indices.ctypes.data), ctypes.byref(min_size_present), ctypes.byref(min_size))

    # Return final results, 'INTENT(OUT)' arguments only.
    return values, indices


def insertion_argsort_r64(values, indices):
    '''! Insertion sort (best for small lists).'''

    # Setting up "values"
    if ((not issubclass(type(values), numpy.ndarray)) or
        (not numpy.asarray(values).flags.f_contiguous) or
        (not (values.dtype == numpy.dtype(ctypes.c_double)))):
        import warnings
        warnings.warn("The provided argument 'values' was not an f_contiguous NumPy array of type 'ctypes.c_double' (or equivalent). Automatically converting (probably creating a full copy).")
        values = numpy.asarray(values, dtype=ctypes.c_double, order='F')
    values_dim_1 = ctypes.c_int(values.shape[0])

    # Setting up "indices"
    if ((not issubclass(type(indices), numpy.ndarray)) or
        (not numpy.asarray(indices).flags.f_contiguous) or
        (not (indices.dtype == numpy.dtype(ctypes.c_long)))):
        import warnings
        warnings.warn("The provided argument 'indices' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
        indices = numpy.asarray(indices, dtype=ctypes.c_long, order='F')
    indices_dim_1 = ctypes.c_int(indices.shape[0])

    # Call C-accessible Fortran wrapper.
    clib.c_insertion_argsort_r64(ctypes.byref(values_dim_1), ctypes.c_void_p(values.ctypes.data), ctypes.byref(indices_dim_1), ctypes.c_void_p(indices.ctypes.data))

    # Return final results, 'INTENT(OUT)' arguments only.
    return values, indices

    
def argpartition_r64(values, indices):
    '''! This function efficiently partitions values based on the median
! of the first, middle, and last elements of the VALUES array. This
! function returns the index of the pivot.'''
        
    # Setting up "values"
    if ((not issubclass(type(values), numpy.ndarray)) or
        (not numpy.asarray(values).flags.f_contiguous) or
        (not (values.dtype == numpy.dtype(ctypes.c_double)))):
        import warnings
        warnings.warn("The provided argument 'values' was not an f_contiguous NumPy array of type 'ctypes.c_double' (or equivalent). Automatically converting (probably creating a full copy).")
        values = numpy.asarray(values, dtype=ctypes.c_double, order='F')
    values_dim_1 = ctypes.c_int(values.shape[0])

    # Setting up "indices"
    if ((not issubclass(type(indices), numpy.ndarray)) or
        (not numpy.asarray(indices).flags.f_contiguous) or
        (not (indices.dtype == numpy.dtype(ctypes.c_long)))):
        import warnings
        warnings.warn("The provided argument 'indices' was not an f_contiguous NumPy array of type 'ctypes.c_long' (or equivalent). Automatically converting (probably creating a full copy).")
        indices = numpy.asarray(indices, dtype=ctypes.c_long, order='F')
    indices_dim_1 = ctypes.c_int(indices.shape[0])

    # Setting up "left"
    left = ctypes.c_long()

    # Call C-accessible Fortran wrapper.
    clib.c_argpartition_r64(ctypes.byref(values_dim_1), ctypes.c_void_p(values.ctypes.data), ctypes.byref(indices_dim_1), ctypes.c_void_p(indices.ctypes.data), ctypes.byref(left))

    # Return final results, 'INTENT(OUT)' arguments only.
    return values, indices, left.value
