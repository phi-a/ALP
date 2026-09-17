import numpy as np
from darknessalp.bfield.PlmSchmidt_d1 import PlmSchmidt_d1




def MagFieldCalculator(cilm, a, r, lat, lon, lmax=None, dealloc=0):
    if lmax is None:
        lmax = cilm.shape[1] - 1

    """
    This function will determine the 3 components (r-hat, theta-hat, phi-hat)
    of the magnetic field vector at a given latitude, longitude and radius.
    Latitude and longitude must be input in degrees. The input coefficients
    must be Schmidt semi-normalized, excluding the Condon-Shortley phase
    factor.

    Parameters:
    cilm : numpy.ndarray
        Spherical harmonic coefficients, with dimensions (2, LMAX_COEFF+1, LMAX_COEFF+1).
        cilm[0, l, m] are cosine coefficients (Clm)
        cilm[1, l, m] are sine coefficients (Slm)
        where l is degree, m is order (0-indexed).
    lmax_in : int
        Maximum degree to use in the expansion.
    a : float
        Reference radius of the potential coefficients.
    r : float
        Radius where the magnetic field is computed (meters).
    lat : float
        Latitude where the magnetic field vector is computed, in degrees.
    lon : float
        Longitude where the magnetic field vector is computed, in degrees.
    dealloc : int, optional
        If 1, deallocate saved memory in the Legendre function routines.
        Default is 0 (not to deallocate memory).

    Returns:
    numpy.ndarray
        A 3-element array with the r, theta, and phi components of the magnetic field.
    """
    # Validate cilm dimensions
    # cilm should be (2, max_degree_stored + 1, max_degree_stored + 1)
    if not (isinstance(cilm, np.ndarray) and cilm.ndim == 3):
        raise ValueError("cilm must be a 3D numpy array.")
    if cilm.shape[0] < 2:
        raise ValueError(f"cilm.shape[0] must be at least 2. Got {cilm.shape[0]}")

    # Max degree stored in cilm array (0-indexed)
    max_degree_in_cilm = cilm.shape[1] - 1
    if cilm.shape[1] < lmax + 1 or cilm.shape[2] < lmax + 1:
        # This check is slightly different from Fortran's, which checks against lmax_in+1.
        # If cilm stores up to degree L, shape[1] is L+1.
        # We need to be able to access cilm[lmax_in, m].
        pass # The lmax_comp calculation will handle using available degrees

    # Determine the maximum degree to compute, ensuring it doesn't exceed cilm's bounds
    # lmax_comp is the maximum degree (0-indexed sense) for computation loops.
    # Fortran: lmax_comp = min(lmax, size(cilm(1,1,:)) - 1)
    # size(cilm(1,1,:)) - 1 is the max degree stored in cilm (0-indexed sense).
    lmax_comp = min(lmax, max_degree_in_cilm)

    # Allocate memory for Legendre polynomials and derivatives
    # Size is (N+1)*(N+2)/2 for max degree N
    pl_size = (lmax_comp + 1) * (lmax_comp + 2) // 2
    pl = np.empty(pl_size, dtype=float)
    dpl = np.empty(pl_size, dtype=float)

    # Allocate memory for sines and cosines of longitude
    # Stores values for orders 0 to lmax_comp
    cosm = np.empty(lmax_comp + 1, dtype=float)
    sinm = np.empty(lmax_comp + 1, dtype=float)

    # Mathematical constants and angle conversions
    pi_val = np.pi
    lat_rad = np.deg2rad(lat)
    lon_rad = np.deg2rad(lon)
    x = np.sin(lat_rad) # Argument for Legendre functions: sin(latitude) = cos(colatitude)

    # Call PlmSchmidt_d1
    # The Python version of PlmSchmidt_d1 should handle its own memory (globals)
    # csphase=1 means do not include (-1)^m phase factor.
    # Note: The PlmSchmidt_d1 provided by user needs to be correctly imported/defined.
    PlmSchmidt_d1(lmax_comp, x, pl, dpl, csphase=1) # Assuming cnorm=0 default

    # Modify dpl as per Fortran code
    # dpl = -dpl * cos(lat * pi / 180.0_dp)
    # Note: The derivative from PlmSchmidt_d1 is dP/dz. Here z=sin(lat).
    # The Fortran dpl is dP/d(colatitude) which is -dP/d(lat).
    # dP/d(lat) = dP/dz * dz/d(lat) = dP/dz * cos(lat)
    # So, if dpl from PlmSchmidt_d1 is dP/dz, then dpl * cos(lat_rad) is dP/dlat.
    # The Fortran line `dpl = -dpl * cos(lat * pi / 180.0_dp)` suggests
    # that the `dpl` from `PlmSchmidt_d1` might be dP/d(colatitude) or something similar.
    # SHTOOLS PlmSchmidt_d1 returns dP_lm(x)/dx and P_lm(x).
    # The magnetic field equations use dP_lm(cos(theta))/dtheta = -sin(theta) * dP_lm(cos(theta))/d(cos(theta))
    # If x = cos(colatitude) = sin(latitude), then theta = colatitude.
    # dP_lm(x)/dtheta = dP_lm(x)/dx * dx/dtheta = dP_lm(x)/dx * (-sin(colatitude)) = dP_lm(x)/dx * (-cos(latitude))
    # The Fortran line `dpl = -dpl * cos(lat * pi / 180.0_dp)` is consistent with this.
    dpl *= -np.cos(lat_rad)


    # Precompute sines and cosines of longitude multiples
    # sinm[order_idx], cosm[order_idx]
    sinm[0] = 0.0  # For order m=0
    cosm[0] = 1.0  # For order m=0

    if lmax_comp > 0:
        sinm[1] = np.sin(lon_rad)  # For order m=1
        cosm[1] = np.cos(lon_rad)  # For order m=1

    # Loop for orders m from 2 up to lmax_comp
    for m_order in range(2, lmax_comp + 1):
        # Using multiple angle identity:
        # sin((k+1)a) = 2*sin(ka)*cos(a) - sin((k-1)a)
        # cos((k+1)a) = 2*cos(ka)*cos(a) - cos((k-1)a)
        # Here, a = lon_rad (cosm[1], sinm[1])
        # k = m_order - 1
        # k+1 = m_order
        # k-1 = m_order - 2
        sinm[m_order] = 2.0 * sinm[m_order - 1] * cosm[1] - sinm[m_order - 2]
        cosm[m_order] = 2.0 * cosm[m_order - 1] * cosm[1] - cosm[m_order - 2]

    # Precompute (a/r)^l factors
    # prefactor[l_minus_1] stores (a/r)^(l) for degree l (l from 1 to lmax_comp)
    if lmax_comp == 0: # handle case where lmax_comp is 0, prefactor might not be used or needed
        prefactor = np.array([])
    else:
        prefactor = np.empty(lmax_comp, dtype=float)
        prefactor[0] = a / r  # For l=1
        for l_idx_pf in range(1, lmax_comp): # Corresponds to l = 2 to lmax_comp
            prefactor[l_idx_pf] = prefactor[l_idx_pf - 1] * (a / r)

    # Initialize expansion components (Br, Btheta, Bphi)
    expand = np.zeros(3, dtype=float)

    # Contribution from l=0 (monopole term for potential, typically C00 for potential)
    # Fortran: expand(1) = -cilm(1,1,1)
    # This is -C00, which is unusual for magnetic field (usually no monopole).
    # If cilm are potential coefficients, then Br relates to -Sum (l+1)*(a/r)^(l+2)*C_lm*Y_lm
    # Let's follow the Fortran literally. cilm[0,0,0] is C00.
    if cilm.shape[1] > 0 and cilm.shape[2] > 0 : # Check if C00 exists
         expand[0] = -cilm[0, 0, 0] # Assuming this is related to radial component setup

    # Summation over degree l and order m
    # Fortran loop: l = 1, lmax_comp
    for l_f in range(1, lmax_comp + 1):  # l_f is the current degree (1-based)
        l1_f = l_f + 1 # (l+1) factor in Fortran

        # Index for prefactor: prefactor[l_f-1] corresponds to (a/r)^l_f
        current_prefactor = prefactor[l_f-1]

        # --- m = 0 terms ---
        # Legendre polynomial P_l,0(x) and its derivative
        # Index for pl, dpl: for degree l_f, order 0
        idx_pl_dpl_m0 = l_f * (l_f + 1) // 2 + 0
        
        # cilm[0, l_f, 0] is C_l_f,0
        # expand(1) = expand(1) - prefactor(l) * l1 * cilm(1,l1,1) * pl(index)
        # Note: Fortran cilm(1,l1,1) means C_{l_f,0} because l1=l_f+1.
        # So cilm index for degree is l_f.
        expand[0] -= current_prefactor * l1_f * cilm[0, l_f, 0] * pl[idx_pl_dpl_m0]
        
        # expand(2) = expand(2) + prefactor(l) * cilm(1,l1,1) * dpl(index)
        expand[1] += current_prefactor * cilm[0, l_f, 0] * dpl[idx_pl_dpl_m0]

        # --- m > 0 terms ---
        # Fortran loop: m = 1, l
        for m_f in range(1, l_f + 1): # m_f is current order (1-based)
            # Index for pl, dpl: for degree l_f, order m_f
            idx_pl_dpl_mf = l_f * (l_f + 1) // 2 + m_f
            
            # cilm[0, l_f, m_f] is C_l_f,m_f
            # cilm[1, l_f, m_f] is S_l_f,m_f
            # cosm[m_f], sinm[m_f] are cos(m_f*lon), sin(m_f*lon)
            
            term_cos_sin = (cilm[0, l_f, m_f] * cosm[m_f] +
                            cilm[1, l_f, m_f] * sinm[m_f])
            
            # expand(1) = expand(1) - prefactor(l) * l1 * pl(index) * term_cos_sin
            expand[0] -= current_prefactor * l1_f * pl[idx_pl_dpl_mf] * term_cos_sin
            
            # expand(2) = expand(2) + prefactor(l) * dpl(index) * term_cos_sin
            expand[1] += current_prefactor * dpl[idx_pl_dpl_mf] * term_cos_sin
            
            # expand(3) = expand(3) + prefactor(l) * pl(index) *
            #             (-m * cilm(1,l1,m1) * sinm(m1) + m * cilm(2,l1,m1) * cosm(m1))
            # m1 in Fortran for cosm/sinm is m_f.
            # m in Fortran for cilm is m_f.
            term_phi = (-m_f * cilm[0, l_f, m_f] * sinm[m_f] +
                         m_f * cilm[1, l_f, m_f] * cosm[m_f])
            expand[2] += current_prefactor * pl[idx_pl_dpl_mf] * term_phi

    # Final scaling and adjustments
    # expand(1:3) = -expand(1:3) * (a / r)**2
    expand *= -(a / r)**2

    # Adjust phi component for latitude
    # if (abs(lat) /= 90.0_dp) then
    #     expand(3) = expand(3) / cos(lat * pi / 180.0_dp)
    # else
    #     expand(3) = 0.0_dp
    # end if
    if not np.isclose(abs(lat), 90.0):
        cos_lat = np.cos(lat_rad)
        if not np.isclose(cos_lat, 0.0): # Avoid division by zero if lat is very near 90/-90
            expand[2] /= cos_lat
        else: # Should be caught by isclose(abs(lat), 90.0) but as a safeguard
            expand[2] = 0.0
    else: # lat is 90 or -90 degrees
        expand[2] = 0.0
        
    # Handle deallocation if requested
    if dealloc == 1:
        # Call PlmSchmidt_d1 with lmax = -1 to trigger deallocation
        # The other parameters might be dummies if lmax=-1 is the primary trigger.
        # Ensure the Python PlmSchmidt_d1 handles this correctly.
        dummy_pl = np.array([0.0]) # Minimal array
        dummy_dpl = np.array([0.0])
        PlmSchmidt_d1(-1, x, dummy_pl, dummy_dpl) # x (sin_lat) is available

    # Fortran deallocates pl, dpl, cosm, sinm explicitly.
    # In Python, these NumPy arrays (pl, dpl, cosm, sinm, prefactor, expand)
    # are local to the function and will be garbage collected when they go out of scope.
    # No explicit deallocation is needed for them.

    return expand



