#from numpy import *
import numpy as np

class bhmie_hagen():
    """ This file is converted from mie.m, see http://atol.ucsd.edu/scatlib/index.htm
         Bohren and Huffman originally published the code in their book on light scattering
        
         Calculation based on Mie scattering theory  
         input:
              x      - size parameter = k*radius = 2pi/lambda * radius   
                           (lambda is the wavelength in the medium around the scatterers)
              refrel - refraction index (n in complex form for example:  1.5+0.02*i;
              nang   - number of angles for S1 and S2 function in range from 0 to pi/2
         input optional:
              diameter - to calculate the crosssections this value is needed
         output:
                S1, S2 - funtion which correspond to the (complex) phase functions
                Qext   - extinction efficiency
                Qsca   - scattering efficiency 
                Qback  - backscatter efficiency
                gsca   - asymmetry parameter"""

    def __init__(self,xold,refrel,noOfAngles, diameter = False):
        self.diameter = diameter
        self.noOfAngles = noOfAngles
        self.sizeParameter = xold
        self.indOfRefraction = refrel

        s1_1=np.zeros(self.noOfAngles,dtype=np.complex128)
        s1_2=np.zeros(self.noOfAngles,dtype=np.complex128)
        s2_1=np.zeros(self.noOfAngles,dtype=np.complex128)
        s2_2=np.zeros(self.noOfAngles,dtype=np.complex128)
        pi=np.zeros(self.noOfAngles,dtype=np.complex128)
        tau=np.zeros(self.noOfAngles,dtype=np.complex128)

        if (self.noOfAngles > 1000):
            print ('error: self.noOfAngles > mxself.noOfAngles=1000 in bhmie')
            return

        # Require NANG>1 in order to calculate scattering intensities
        if (self.noOfAngles < 2):
            self.noOfAngles = 2

        pii = 4.*np.arctan(1.)
#        dx = x

#        drefrl = self.indOfRefraction



        self.calc_noOfTerms()



        dang = .5*pii/ (self.noOfAngles-1)


        amu=np.arange(0.0,self.noOfAngles,1)
        amu=np.cos(amu*dang)

        pi0=np.zeros(self.noOfAngles,dtype=np.complex128)
        pi1=np.ones(self.noOfAngles,dtype=np.complex128)
        
        logDeriv = self.get_logDeriv()
        



        #*** Riccati-Bessel functions with real argument X
        #    calculated by upward recurrence

        psi0 = np.cos(self.sizeParameter)
        psi1 = np.sin(self.sizeParameter)
        chi0 = -np.sin(self.sizeParameter)
        chi1 = np.cos(self.sizeParameter)
        xi1 = psi1-chi1*1j
        qsca = 0.
        gsca = 0.
        p = -1

        for n in xrange(0,self.noOfTermses[0]):
            en = n+1.0
            fn = (2.*en+1.)/(en* (en+1.))

        # for given N, PSI  = psi_n        CHI  = chi_n
        #              PSI1 = psi_{n-1}    CHI1 = chi_{n-1}
        #              PSI0 = psi_{n-2}    CHI0 = chi_{n-2}
        # Calculate psi_n and chi_n
            psi = (2.*en-1.)*psi1/self.sizeParameter - psi0
            chi = (2.*en-1.)*chi1/self.sizeParameter - chi0
            xi = psi-chi*1j
        #*** Store previous values of AN and BN for use
        #    in computation of g=<cos(theta)>
            if (n > 0):
                an1 = an
                bn1 = bn

        #*** Compute AN and BN:
            an = (logDeriv[n]/self.indOfRefraction+en/self.sizeParameter)*psi - psi1
            an = an/ ((logDeriv[n]/self.indOfRefraction+en/self.sizeParameter)*xi-xi1)
            bn = (self.indOfRefraction*logDeriv[n]+en/self.sizeParameter)*psi - psi1
            bn = bn/ ((self.indOfRefraction*logDeriv[n]+en/self.sizeParameter)*xi-xi1)

        #*** Augment sums for Qsca and g=<cos(theta)>
            qsca += (2.*en+1.)* (abs(an)**2+abs(bn)**2)
            gsca += ((2.*en+1.)/ (en* (en+1.)))*( np.real(an)* np.real(bn)+np.imag(an)*np.imag(bn))

            if (n > 0):
                gsca += ((en-1.)* (en+1.)/en)*( np.real(an1)* np.real(an)+np.imag(an1)*np.imag(an)+np.real(bn1)* np.real(bn)+np.imag(bn1)*np.imag(bn))


        #*** Now calculate scattering intensity pattern
        #    First do angles from 0 to 90
            pi=0+pi1    # 0+pi1 because we want a hard copy of the values
            tau=en*amu*pi-(en+1.)*pi0
            s1_1 += fn* (an*pi+bn*tau)
            s2_1 += fn* (an*tau+bn*pi)
        #*** Now do angles greater than 90 using PI and TAU from
        #    angles less than 90.
        #    P=1 for N=1,3,...% P=-1 for N=2,4,...
        #   remember that we have to reverse the order of the elements
        #   of the second part of s1 and s2 after the calculation
            p = -p
            s1_2+= fn*p* (an*pi-bn*tau)
            s2_2+= fn*p* (bn*pi-an*tau)

            psi0 = psi1
            psi1 = psi
            chi0 = chi1
            chi1 = chi
            xi1 = psi1-chi1*1j

        #*** Compute pi_n for next value of n
        #    For each angle J, compute pi_n+1
        #    from PI = pi_n , PI0 = pi_n-1
            pi1 = ((2.*en+1.)*amu*pi- (en+1.)*pi0)/ en
            pi0 = 0+pi   # 0+pi because we want a hard copy of the values

        #*** Have summed sufficient terms.
        #    Now compute QSCA,QEXT,QBACK,and GSCA

        #   we have to reverse the order of the elements of the second part of s1 and s2
        s1=np.concatenate((s1_1,s1_2[-2::-1]))
        s2=np.concatenate((s2_1,s2_2[-2::-1]))
        gsca = 2.*gsca/qsca
        qsca = (2./ (self.sizeParameter**2))*qsca
#        qext = (4./ (self.sizeParameter**2))* real(s1[0])

        # more common definition of the backscattering efficiency,
        # so that the backscattering cross section really
        # has dimension of length squared
#        qback = 4*(abs(s1[2*self.noOfAngles-2])/self.sizeParameter)**2
        #qback = ((abs(s1[2*self.noOfAngles-2])/self.sizeParameter)**2 )/pii  #old form
        self.s1 = s1
        self.s2 = s2
#        self.qext = qext
        self.calc_qext()
        self.qsca = qsca
#        self.qback = qback
        self.calc_qback()
        self.gsca = gsca
        if self.diameter:
            self.csca =  self.qsca * self.diameter**2 * np.pi * 0.5**2  #scattering crosssection
        else:
            self.csca = 0

    def get_logDeriv(self):
        """ original comment:
            Logarithmic derivative D(J) calculated by downward recurrence
            beginning with initial value (0.,0.) at J=NMX"""
        y = self.sizeParameter * self.indOfRefraction
        nn = int(self.noOfTermses[1]) - 1
        d=np.zeros(nn+1,dtype=np.complex128)
        for n in range(0,nn):
            en = self.noOfTermses[1] - n
            d[nn-n-1] = (en/y) - (1./ (d[nn-n]+en/y)) 
        return d
        
    def get_natural(self):
        return np.abs(self.s1)**2 + np.abs(self.s2)**2
        
    def get_perpendicular(self):
        return np.abs(self.s1)**2
        
    def get_parallel(self):
        return np.abs(self.s2)**2
        
        
        
    def calc_noOfTerms(self):
        """Original comment:
        Series expansion terminated after NSTOP (noOfTerms) terms
            Logarithmic derivatives calculated from NMX on down
         BTD experiment 91/1/15: add one more term to series and compare resu<s
              NMX=AMAX1(XSTOP,YMOD)+16
         test: compute 7001 wavelen>hs between .0001 and 1000 micron
         for a=1.0micron SiC grain.  When NMX increased by 1, only a single
         computed number changed (out of 4*7001) and it only changed by 1/8387
         conclusion: we are indeed retaining enough terms in series!
         """
         
        ymod = abs(self.sizeParameter*self.indOfRefraction) 
        xstop = self.sizeParameter + 4.*self.sizeParameter**0.3333 + 2.0
        #xstop = x + 4.*x**0.3333 + 10.0
        nmx = max(xstop,ymod) + 15.0
        nmx=np.fix(nmx)
        
        
        self.noOfTermses = (int(xstop),nmx)
        
        # Hagen: now idea, what the following is exactly doing?!?
        nmxx=150000
        if (nmx > nmxx):
            raise ValueError( "error: nmx > nmxx=%f for |m|x=%f" % ( nmxx, ymod) )
        
    def calc_qsca(self):
        """scattering efficiency"""
        print 'bla'
        
    def calc_qext(self):
        """extinction efficiency. normalized real part of s1 at 0 deg (forward)"""
        self.qext = (4./ (self.sizeParameter**2))* np.real(self.s1[0])
        if self.diameter:
            self.cext =  self.qext * self.diameter**2 * np.pi * 0.5**2
        else:
            self.cext = 0
        
    def calc_qback(self):
        """ Backscattering efficiency. Looks like it simpy locks for the efficiency 
        at 180 deg... I am surprised why they are not simpy taking the last one?
        -> it is the same!! -> fixed"""
        self.qback = 4*(abs(self.s1[-1])/self.sizeParameter)**2
            
    def return_Values_as_dict(self):
        
            return {'phaseFct_S1': self.s1, 
                    'phaseFct_S2': self.s2, 
                    'extinction_efficiency': self.qext, 
                    'scattering_efficiency': self.qsca, 
                    'backscatter_efficiency': self.qback, 
                    'asymmetry_parameter': self.gsca, 
                    'scattering_crosssection': self.csca,
                    'extinction_crosssection': self.cext}
        
    def return_Values(self):
        return self.s1, self.s2, self.qext, self.qsca, self.qback, self.gsca


def bhmie(x,refrel,nang):
    """ This file is converted from mie.m, see http://atol.ucsd.edu/scatlib/index.htm
         Bohren and Huffman originally published the code in their book on light scattering
        
         Calculation based on Mie scattering theory  
         input:
              x      - size parameter = k*radius = 2pi/lambda * radius   
                           (lambda is the wavelength in the medium around the scatterers)
              refrel - refraction index (n in complex form for example:  1.5+0.02*i;
              nang   - number of angles for S1 and S2 function in range from 0 to pi/2
         output:
                S1, S2 - funtion which correspond to the (complex) phase functions
                Qext   - extinction efficiency
                Qsca   - scattering efficiency 
                Qback  - backscatter efficiency
                gsca   - asymmetry parameter"""


    nmxx=150000

    s1_1=zeros(nang,dtype=complex128)
    s1_2=zeros(nang,dtype=complex128)
    s2_1=zeros(nang,dtype=complex128)
    s2_2=zeros(nang,dtype=complex128)
    pi=zeros(nang,dtype=complex128)
    tau=zeros(nang,dtype=complex128)

    if (nang > 1000):
        print ('error: nang > mxnang=1000 in bhmie')
        return

    # Require NANG>1 in order to calculate scattering intensities
    if (nang < 2):
        nang = 2

    pii = 4.*arctan(1.)
    dx = x

    drefrl = refrel
    y = x*drefrl
    ymod = abs(y)


    #    Series expansion terminated after self.noOfTerms terms
    #    Logarithmic derivatives calculated from NMX on down

    xstop = x + 4.*x**0.3333 + 2.0
    #xstop = x + 4.*x**0.3333 + 10.0
    nmx = max(xstop,ymod) + 15.0
    nmx=fix(nmx)

    # BTD experiment 91/1/15: add one more term to series and compare resu<s
    #      NMX=AMAX1(XSTOP,YMOD)+16
    # test: compute 7001 wavelen>hs between .0001 and 1000 micron
    # for a=1.0micron SiC grain.  When NMX increased by 1, only a single
    # computed number changed (out of 4*7001) and it only changed by 1/8387
    # conclusion: we are indeed retaining enough terms in series!

    nstop = int(xstop)

    if (nmx > nmxx):
        print ( "error: nmx > nmxx=%f for |m|x=%f" % ( nmxx, ymod) )
        return

    dang = .5*pii/ (nang-1)


    amu=arange(0.0,nang,1)
    amu=cos(amu*dang)

    pi0=zeros(nang,dtype=complex128)
    pi1=ones(nang,dtype=complex128)

    # Logarithmic derivative D(J) calculated by downward recurrence
    # beginning with initial value (0.,0.) at J=NMX

    nn = int(nmx)-1
    d=zeros(nn+1,dtype=complex128)
    for n in range(0,nn):
        en = nmx - n
        d[nn-n-1] = (en/y) - (1./ (d[nn-n]+en/y))

    #*** Riccati-Bessel functions with real argument X
    #    calculated by upward recurrence

    psi0 = cos(dx)
    psi1 = sin(dx)
    chi0 = -sin(dx)
    chi1 = cos(dx)
    xi1 = psi1-chi1*1j
    qsca = 0.
    gsca = 0.
    p = -1

    for n in range(0,nstop):
        en = n+1.0
        fn = (2.*en+1.)/(en* (en+1.))

    # for given N, PSI  = psi_n        CHI  = chi_n
    #              PSI1 = psi_{n-1}    CHI1 = chi_{n-1}
    #              PSI0 = psi_{n-2}    CHI0 = chi_{n-2}
    # Calculate psi_n and chi_n
        psi = (2.*en-1.)*psi1/dx - psi0
        chi = (2.*en-1.)*chi1/dx - chi0
        xi = psi-chi*1j

    #*** Store previous values of AN and BN for use
    #    in computation of g=<cos(theta)>
        if (n > 0):
            an1 = an
            bn1 = bn

    #*** Compute AN and BN:
        an = (d[n]/drefrl+en/dx)*psi - psi1
        an = an/ ((d[n]/drefrl+en/dx)*xi-xi1)
        bn = (drefrl*d[n]+en/dx)*psi - psi1
        bn = bn/ ((drefrl*d[n]+en/dx)*xi-xi1)

    #*** Augment sums for Qsca and g=<cos(theta)>
        qsca += (2.*en+1.)* (abs(an)**2+abs(bn)**2)
        gsca += ((2.*en+1.)/ (en* (en+1.)))*( real(an)* real(bn)+imag(an)*imag(bn))

        if (n > 0):
            gsca += ((en-1.)* (en+1.)/en)*( real(an1)* real(an)+imag(an1)*imag(an)+real(bn1)* real(bn)+imag(bn1)*imag(bn))


    #*** Now calculate scattering intensity pattern
    #    First do angles from 0 to 90
        pi=0+pi1    # 0+pi1 because we want a hard copy of the values
        tau=en*amu*pi-(en+1.)*pi0
        s1_1 += fn* (an*pi+bn*tau)
        s2_1 += fn* (an*tau+bn*pi)

    #*** Now do angles greater than 90 using PI and TAU from
    #    angles less than 90.
    #    P=1 for N=1,3,...% P=-1 for N=2,4,...
    #   remember that we have to reverse the order of the elements
    #   of the second part of s1 and s2 after the calculation
        p = -p
        s1_2+= fn*p* (an*pi-bn*tau)
        s2_2+= fn*p* (bn*pi-an*tau)

        psi0 = psi1
        psi1 = psi
        chi0 = chi1
        chi1 = chi
        xi1 = psi1-chi1*1j

    #*** Compute pi_n for next value of n
    #    For each angle J, compute pi_n+1
    #    from PI = pi_n , PI0 = pi_n-1
        pi1 = ((2.*en+1.)*amu*pi- (en+1.)*pi0)/ en
        pi0 = 0+pi   # 0+pi because we want a hard copy of the values

    #*** Have summed sufficient terms.
    #    Now compute QSCA,QEXT,QBACK,and GSCA

    #   we have to reverse the order of the elements of the second part of s1 and s2
    s1=concatenate((s1_1,s1_2[-2::-1]))
    s2=concatenate((s2_1,s2_2[-2::-1]))
    gsca = 2.*gsca/qsca
    qsca = (2./ (dx*dx))*qsca
    qext = (4./ (dx*dx))* real(s1[0])

    # more common definition of the backscattering efficiency,
    # so that the backscattering cross section really
    # has dimension of length squared
    qback = 4*(abs(s1[2*nang-2])/dx)**2
    #qback = ((abs(s1[2*nang-2])/dx)**2 )/pii  #old form

    return s1,s2,qext,qsca,qback,gsca

if __name__ == "__main__":
#    x = 10
    x_sizePara = 5
    n_refraction = 1.5 + 0.01j
    nang_no = 10
    bhh = bhmie_hagen(x_sizePara, n_refraction, nang_no)
    s1,s2,qext,qsca,qback,gsca = bhh.return_Values()   
    
    s1,s2,qext,qsca,qback,gsca = bhmie(x_sizePara,n_refraction,nang_no)    
    
    print 'done'