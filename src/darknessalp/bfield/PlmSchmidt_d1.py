import numpy as np
import math

# Global variables to mimic Fortran's SAVE attribute and threadprivate behavior (for single-threaded context)
# These will persist across calls to PlmSchmidt_d1 if lmax does not increase.
_lmax_old_schmidt_d1 = 0
_sqr_schmidt_d1 = None
_f1_schmidt_d1 = None
_f2_schmidt_d1 = None

def PlmSchmidt_d1(lmax, z, p_out, dp1_out, csphase=1, cnorm=0, exitstatus_out_list=None):
    """
    Computes all Schmidt semi-normalized associated Legendre functions and their first derivatives.
    This is a Python transcription of the Fortran subroutine PlmSchmidt_d1 from SHTOOLS.

    Parameters:
    lmax : int
        The maximum spherical harmonic degree to compute.
    z : float
        cos(colatitude) or sin(latitude). Argument of the Legendre functions.
    p_out : numpy.ndarray
        A 1D NumPy array, pre-allocated, to store the associated Legendre functions.
        Size must be at least (lmax+1)*(lmax+2)/2.
        Output is stored by l*(l+1)/2 + m.
    dp1_out : numpy.ndarray
        A 1D NumPy array, pre-allocated, to store the first derivatives.
        Size must be at least (lmax+1)*(lmax+2)/2.
        Output is stored by l*(l+1)/2 + m.
    csphase : int, optional
        Condon-Shortley phase convention.
        1 (default): Do not include the phase factor of (-1)^m.
        -1: Apply the phase factor of (-1)^m.
    cnorm : int, optional
        Normalization convention.
        0 (default): Use real normalization (integral of P_lm^2 is 2*(2-delta_0m)/(2l+1)).
        1: Use complex normalization (integral of P_lm^2 is 2/(2l+1)).
    exitstatus_out_list : list, optional
        If provided as a list (e.g., [0]), exitstatus[0] will be set:
        0 = No errors;
        1 = Improper dimensions of input array;
        2 = Improper bounds for input variable;
        3 = Error allocating memory (less relevant in Python, but kept for consistency).

    Returns:
    None (results are stored in p_out and dp1_out).
    """
    global _lmax_old_schmidt_d1, _sqr_schmidt_d1, _f1_schmidt_d1, _f2_schmidt_d1

    # --- Helper function for Fortran's sqr(i) = sqrt(float(i)) ---
    # _sqr_schmidt_d1 stores sqrt(1), sqrt(2), ...
    # So, _sqr_schmidt_d1[fortran_idx - 1] gives sqrt(fortran_idx)
    def get_sqr(fortran_index):
        if not (1 <= fortran_index < len(_sqr_schmidt_d1) + 1):
             # This case should ideally not be hit if lmax and array sizes are correct
             raise IndexError(f"Fortran index {fortran_index} is out of bounds for _sqr_schmidt_d1 (size {len(_sqr_schmidt_d1)})")
        return _sqr_schmidt_d1[fortran_index - 1]

    # --- Initial error status ---
    if exitstatus_out_list is not None:
        exitstatus_out_list[0] = 0

    # --- Handle lmax = -1 for deallocation ---
    if lmax == -1:
        _sqr_schmidt_d1 = None
        _f1_schmidt_d1 = None
        _f2_schmidt_d1 = None
        _lmax_old_schmidt_d1 = 0
        return

    # --- Calculate required dimension ---
    sdim = (lmax + 1) * (lmax + 2) // 2

    # --- Validate input array dimensions ---
    if p_out.size < sdim:
        if exitstatus_out_list is not None:
            exitstatus_out_list[0] = 1
            return
        else:
            raise ValueError(f"p_out must be dimensioned at least {sdim}. Got {p_out.size}")
    if dp1_out.size < sdim:
        if exitstatus_out_list is not None:
            exitstatus_out_list[0] = 1
            return
        else:
            raise ValueError(f"dp1_out must be dimensioned at least {sdim}. Got {dp1_out.size}")

    # --- Validate lmax ---
    if lmax < 0:
        if exitstatus_out_list is not None:
            exitstatus_out_list[0] = 2
            return
        else:
            raise ValueError(f"LMAX must be greater than or equal to 0. Input value is {lmax}")

    # --- Validate z ---
    if abs(z) > 1.0:
        if exitstatus_out_list is not None:
            exitstatus_out_list[0] = 2
            return
        else:
            raise ValueError(f"ABS(Z) must be less than or equal to 1. Input value is {z}")
    
    if abs(z) == 1.0: # Derivative calculation involves 1/(1-z^2)
        # The Fortran code has this check specifically for derivatives.
        # For P_lm themselves, z=+-1 is fine.
        # "Derivative can not be calculated at Z = 1 or -1."
        # This implies that if abs(z) == 1.0, we should not proceed to derivative calculations
        # or expect issues. The Fortran code exits.
        if exitstatus_out_list is not None:
            exitstatus_out_list[0] = 2
            # print("Warning: Derivative calculation at |z|=1 is problematic.") # Or error out
            return # Matching Fortran's exit for this condition
        else:
            raise ValueError(f"Derivative can not be calculated at Z = 1 or -1. Input Z is {z}")

    # --- Validate csphase ---
    phase = 0
    if csphase == -1:
        phase = -1
    elif csphase == 1:
        phase = 1
    else:
        if exitstatus_out_list is not None:
            exitstatus_out_list[0] = 2
            return
        else:
            raise ValueError(f"CSPHASE must be 1 (exclude) or -1 (include). Input value is {csphase}")

    # --- Scaling factor for Holmes and Featherstone (2002) ---
    scalef = 1.0e-280

    # --- Precompute arrays if lmax has increased ---
    if lmax > _lmax_old_schmidt_d1 or _sqr_schmidt_d1 is None: # Added None check for first call
        # Deallocate (Python handles this via garbage collection, but clear refs)
        _sqr_schmidt_d1 = None
        _f1_schmidt_d1 = None
        _f2_schmidt_d1 = None
        
        try:
            # sqr(1) to sqr(2*lmax+1)
            _sqr_schmidt_d1 = np.empty(2 * lmax + 1, dtype=float)
            for i in range(2 * lmax + 1): # i from 0 to 2*lmax
                _sqr_schmidt_d1[i] = math.sqrt(float(i + 1))

            # f1 and f2 arrays, size sdim, indexed like p_out/dp1_out
            _f1_schmidt_d1 = np.zeros(sdim, dtype=float) # Initialize with zeros
            _f2_schmidt_d1 = np.zeros(sdim, dtype=float)

            # Precompute multiplicative factors f1, f2 for recursion
            # These are for PlmSchmidt(l,m) = z*f1(l,m)*PlmSchmidt(l-1,m) - f2(l,m)*PlmSchmidt(l-2,m)
            # (Note: actual recurrence in Fortran for P(l,0) is different, uses these for m>0)
            # The Fortran k is 1-based index for p, f1, f2. k_py = k_fortran - 1.
            # Loop structure from Fortran:
            # k_fortran = 3 (initial value before loop)
            # do l_f = 2, lmax
            #   k_fortran = k_fortran + 1 (for m=0)
            #   f1(k_fortran) = ... ; f2(k_fortran) = ...
            #   do m_f = 1, l_f-2
            #     k_fortran = k_fortran + 1
            #     f1(k_fortran) = ... ; f2(k_fortran) = ...
            #   end do
            #   k_fortran = k_fortran + 2 (skip for m=l-1, m=l where different recursion is used)
            # end do
            
            k_fortran = 3 # Start before the first increment
            for l_f in range(2, lmax + 1): # Fortran l from 2 to lmax
                # For m = 0
                k_fortran += 1
                p_idx = k_fortran - 1 # Python index
                if p_idx < sdim : # Bounds check
                    _f1_schmidt_d1[p_idx] = float(2 * l_f - 1) / float(l_f)
                    _f2_schmidt_d1[p_idx] = float(l_f - 1) / float(l_f)
                
                # For m = 1 to l_f - 2
                for m_f in range(1, l_f - 2 + 1): # Fortran m from 1 to l_f-2
                    k_fortran += 1
                    p_idx = k_fortran - 1
                    if p_idx < sdim: # Bounds check
                         # Need to handle get_sqr for potentially 0 or negative arguments if logic is flawed
                        if (l_f + m_f <= 0) or (l_f - m_f <= 0) or \
                           (l_f - m_f - 1 <= 0 and (l_f - m_f - 1 != 0 or l_f + m_f -1 == 0)) or \
                           (l_f + m_f - 1 <= 0 and (l_f + m_f - 1 != 0 or l_f - m_f -1 == 0)):
                            # This indicates an issue, typically l_f-m_f etc. must be > 0 for sqrt
                            # For Schmidt, l-m >= 0. l-m-1 can be -1. sqrt of negative is error.
                            # The Fortran code relies on sqr(negative) not being called due to loop bounds.
                            # sqr(l-m-1) implies l-m-1 >= 1. So l-m >= 2.
                            # This is consistent with m <= l-2.
                            pass # Should be fine with correct loop bounds

                        _f1_schmidt_d1[p_idx] = float(2 * l_f - 1) / (get_sqr(l_f + m_f) * get_sqr(l_f - m_f))
                        _f2_schmidt_d1[p_idx] = (get_sqr(l_f - m_f - 1) * get_sqr(l_f + m_f - 1)) / \
                                             (get_sqr(l_f + m_f) * get_sqr(l_f - m_f))
                k_fortran += 2 # Skip factors for m=l-1 and m=l
            _lmax_old_schmidt_d1 = lmax

        except MemoryError: # Or other allocation related errors, though less common for NumPy default sizes
            if exitstatus_out_list is not None:
                exitstatus_out_list[0] = 3
                return
            else:
                raise MemoryError("Problem allocating arrays SQR, F1, or F2")
        except IndexError as e: # Catch issues from get_sqr if logic is off
            if exitstatus_out_list is not None:
                exitstatus_out_list[0] = 3 # Using 3 for allocation/internal setup error
                print(f"Internal error during precomputation: {e}")
                return
            else:
                raise IndexError(f"Internal error during precomputation: {e}")


    # --- Calculate P(l,0) ---
    # These are initially unnormalized Legendre Polynomials P_l(z) as per Fortran comments.
    # u = sin(theta) where z = cos(theta)
    # Handle z = +/-1 carefully for u. If abs(z)=1, u=0.
    # The check for abs(z)==1.0 earlier means u will not be 0 here if that check leads to return.
    # If the check is removed or modified, u can be 0.
    if 1.0 - z < 0 or 1.0 + z < 0: # Should not happen if |z| <= 1
        val_in_sqrt = (1.0-z)*(1.0+z) # approx 1-z^2
        if abs(val_in_sqrt) < 1e-15: # effectively zero
             u = 0.0
        else: # Should not happen
            if exitstatus_out_list is not None:
                exitstatus_out_list[0] = 2 
                return
            else:
                raise ValueError(f"Invalid z = {z} leading to negative in sqrt for u")
    else:
        u = math.sqrt((1.0 - z) * (1.0 + z))
    u2 = u * u # u^2 = sin^2(theta) = 1 - z^2

    # P(0,0)
    # Python index for (l,m) is l*(l+1)//2 + m
    p_idx_00 = 0 # l=0, m=0
    p_out[p_idx_00] = 1.0
    dp1_out[p_idx_00] = 0.0

    if lmax == 0:
        return

    # P(1,0)
    p_idx_10 = 1 # l=1, m=0
    pm1_val = z  # P_1(z) = z
    p_out[p_idx_10] = pm1_val
    # dP_1/dz = 1.0. Fortran dp1(2)=1.0_dp
    dp1_out[p_idx_10] = 1.0
    
    pm2_val = 1.0 # P_0(z) = 1.0

    # P(l,0) for l >= 2
    # Fortran k = l*(l+1)/2 + 1 (1-based). Python p_idx = l*(l+1)//2.
    for l_f in range(2, lmax + 1): # Fortran l from 2 to lmax
        p_idx_l0 = l_f * (l_f + 1) // 2 + 0 # Python index for (l_f, 0)
        
        # Using precomputed f1, f2 which store (2l-1)/l and (l-1)/l for m=0
        # Recurrence for unnormalized P_l: P_l = ( (2l-1)z P_{l-1} - (l-1)P_{l-2} ) / l
        # Fortran: plm = f1(k)*z*pm1 - f2(k)*pm2
        # where f1(k) = (2l-1)/l and f2(k) = (l-1)/l
        plm_val = _f1_schmidt_d1[p_idx_l0] * z * pm1_val - _f2_schmidt_d1[p_idx_l0] * pm2_val
        p_out[p_idx_l0] = plm_val
        
        # Derivative dP_l/dz = l * (P_{l-1} - z P_l) / (1-z^2)
        if u2 == 0.0: # Should be caught by abs(z)==1.0 check
            # Handle derivative at poles for m=0 if needed, though Fortran exits.
            # P'_l(1) = l(l+1)/2, P'_l(-1) = (-1)^(l+1) * l(l+1)/2
            # For now, assume u2 != 0 due to earlier check.
            if exitstatus_out_list is not None: # Should not happen if abs(z)==1 caused early exit
                exitstatus_out_list[0] = 2 
                return
            else: # Should not happen
                raise ValueError("u2 is zero, derivative undefined (should be caught earlier)")
        else:
            dp1_out[p_idx_l0] = float(l_f) * (pm1_val - z * plm_val) / u2
        
        pm2_val = pm1_val
        pm1_val = plm_val

    # --- Calculate P(m,m), P(m+1,m), and P(l,m) for m > 0 ---
    # Using Holmes and Featherstone (2002) scaling
    
    # Initial P_mm (related to P_00 or P_11 depending on cnorm) scaled by scalef
    if cnorm == 1: # Complex normalization
        current_pmm_scaled = scalef # P_00_scaled for complex norm (P_00 = 1)
    else: # Real normalization
        current_pmm_scaled = get_sqr(2) * scalef # P_00_scaled for real norm (P_00 = sqrt(2) * P_00_unnorm = sqrt(2))
                                               # Fortran sqr(2) is sqrt(2). P_00_schmidt_real = 1.
                                               # So this should be P_00_schmidt_real * scalef = 1.0 * scalef.
                                               # SHTOOLS: P_0,0 = 1 for both norms.
                                               # Let's re-check Fortran pmm = sqr(2)*scalef.
                                               # If P_0,0 = 1, then pmm = 1.0 * scalef.
                                               # The sqr(2) might be for P_1,1 from P_0,0 relation.
                                               # For P_m,m, the factor sqrt(2-delta_0m) applies. For m>0, it's sqrt(2).
                                               # P_m,m^schmidt_real = sqrt(2) * P_m,m^schmidt_complex for m>0.
                                               # P_0,0 is same for both.
                                               # The Fortran code's `pmm` is initialized based on P_0,0.
                                               # If cnorm=0 (real), pmm = sqrt(2)*scalef. If cnorm=1 (complex), pmm=scalef.
                                               # This implies that if P_0,0=1, then for real norm, it's scaled by sqrt(2).
                                               # This is unusual. SHTOOLS doc: P_0,0 = 1.
                                               # Let's follow Fortran literally:
        current_pmm_scaled = get_sqr(2) * scalef if cnorm == 0 else scalef


    rescalem_val = 1.0 / scalef # Initial rescalem_val for m=0

    # Loop for m from 1 to lmax-1
    for m_f in range(1, lmax): # Fortran m from 1 to lmax-1
        rescalem_val *= u # rescalem = u^m / scalef

        # Calculate P(m,m)
        # current_pmm_scaled is P(m-1,m-1)_scaled. Update to P(m,m)_scaled.
        # Fortran: pmm = phase * pmm * sqr(2*m+1) / sqr(2*m)
        current_pmm_scaled = phase * current_pmm_scaled * get_sqr(2 * m_f + 1) / get_sqr(2 * m_f)
        
        p_idx_mm = m_f * (m_f + 1) // 2 + m_f # Python index for (m_f, m_f)
        
        # Fortran: p(kstart) = pmm * rescalem / sqr(2*m+1)
        p_out[p_idx_mm] = current_pmm_scaled * rescalem_val / get_sqr(2 * m_f + 1)
        if u2 != 0.0:
            dp1_out[p_idx_mm] = -float(m_f) * z * p_out[p_idx_mm] / u2
        # else: error, but abs(z)==1 handled

        # This pm2_val is for P(l,m) recurrence, related to P(m,m)_scaled
        # Fortran: pm2 = pmm / sqr(2*m+1)
        pm2_for_l_loop_scaled = current_pmm_scaled / get_sqr(2 * m_f + 1)

        # Calculate P(m+1,m)
        p_idx_mp1_m = (m_f + 1) * (m_f + 2) // 2 + m_f # Python index for (m_f+1, m_f)
        
        # Fortran: pm1 = z * sqr(2*m+1) * pm2
        # pm1 is P(m+1,m)_scaled
        pm1_for_l_loop_scaled = z * get_sqr(2 * m_f + 1) * pm2_for_l_loop_scaled
        # This simplifies to z * current_pmm_scaled
        
        p_out[p_idx_mp1_m] = pm1_for_l_loop_scaled * rescalem_val
        
        # dp1(k) = (p(k-m-1) * sqr(2*m+1) - z * (m+1) * p(k)) / u**2
        # p(k-m-1) in Fortran is p(kstart), i.e., P(m_f,m_f) which is p_out[p_idx_mm]
        if u2 != 0.0:
            dp1_out[p_idx_mp1_m] = (p_out[p_idx_mm] * get_sqr(2 * m_f + 1) - \
                                   z * float(m_f + 1) * p_out[p_idx_mp1_m]) / u2

        # --- Inner loop for P(l,m) where l >= m+2 ---
        # Initialize pm2, pm1 for this inner loop based on P(m,m)_scaled and P(m+1,m)_scaled
        current_pm2_inner_scaled = pm2_for_l_loop_scaled
        current_pm1_inner_scaled = pm1_for_l_loop_scaled

        for l_f in range(m_f + 2, lmax + 1): # Fortran l from m_f+2 to lmax
            p_idx_lm = l_f * (l_f + 1) // 2 + m_f # Python index for (l_f, m_f)
            
            f1_val = _f1_schmidt_d1[p_idx_lm]
            f2_val = _f2_schmidt_d1[p_idx_lm]
            
            plm_scaled = z * f1_val * current_pm1_inner_scaled - f2_val * current_pm2_inner_scaled
            p_out[p_idx_lm] = plm_scaled * rescalem_val
            
            # dp1(k) = ( sqr(l+m) * sqr(l-m) * p(k-l) - l * z * p(k) ) / u**2
            # p(k-l) in Fortran is P(l_f-1, m_f)
            p_idx_lm_prev_l = (l_f - 1) * l_f // 2 + m_f
            if u2 != 0.0:
                dp1_out[p_idx_lm] = (get_sqr(l_f + m_f) * get_sqr(l_f - m_f) * p_out[p_idx_lm_prev_l] - \
                                     float(l_f) * z * p_out[p_idx_lm]) / u2
            
            current_pm2_inner_scaled = current_pm1_inner_scaled
            current_pm1_inner_scaled = plm_scaled
    
    # --- Calculate P(lmax,lmax) ---
    # This block executes if lmax >= 1, because if lmax=0, it returns earlier.
    if lmax >= 1:
        rescalem_val *= u # rescalem = u^lmax / scalef
        
        p_idx_lmax_lmax = lmax * (lmax + 1) // 2 + lmax # Python index for (lmax,lmax)
        
        # current_pmm_scaled is P(lmax-1,lmax-1)_scaled from the loop,
        # or the initial pmm if lmax=1 (m-loop was skipped).
        # Fortran: pmm = phase * pmm / sqr(2*lmax)
        final_pmm_val_at_lmax_lmax = phase * current_pmm_scaled / get_sqr(2 * lmax)
        
        p_out[p_idx_lmax_lmax] = final_pmm_val_at_lmax_lmax * rescalem_val
        if u2 != 0.0:
            dp1_out[p_idx_lmax_lmax] = -float(lmax) * z * p_out[p_idx_lmax_lmax] / u2

    # No explicit return value, results are in p_out, dp1_out
