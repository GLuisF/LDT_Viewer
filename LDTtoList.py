def Mcx(Isym,Mc):                       # https://keysofthelp.transoftsolutions.com/KeyLIGHTS/6.3/Appendix%20B%20EULUMDAT%20File%20Format.htm
    if Isym == 0:
        Mc1 = 1
        Mc2 = Mc
    elif Isym == 1:
        Mc1 = 1
        Mc2 = 1
    elif Isym == 2:
        Mc1 = 1
        Mc2 = Mc / 2 + 1
    elif Isym == 3:
        Mc1 = 3 * Mc / 4 + 1
        Mc2 = Mc1 + Mc / 2
    elif Isym == 4:
        Mc1 = 1
        Mc2 = Mc / 4 + 1
    
    return [Mc1,Mc2]

class ldt:
    def __init__(self, arquivo):
        texto = open(arquivo,'r')
        linhas = texto.readlines()
        linhas = [linha[:-1] for linha in linhas]
        texto.close                       # https://docs.agi32.com/PhotometricToolbox/Content/Open_Tool/eulumdat_file_format.htm
        self.company = linhas[0]          # Company identification/databank/version/format identification
        self.Ityp = int(linhas[1])        # Type indicator (0 - point source with no symmetry; 1 - symmetry  about the vertical axis; 2 - linear luminaire; 3 - point source with any other symmetry.
        self.Isym = int(linhas[2])        # Symmetry indicator (0 ... no symmetry; 1 - symmetry about the vertical axis; 2 - symmetry to plane C0-C180; 3 - symmetry to plane C90-C270; 4 - symmetry to plane C0-C180 and to plane C90-C270)
        self.Mc = int(linhas[3])          # Number of C-planes between 0 and 360 degrees (usually 24 for interior, 36 for road lighting luminaires)
        self.Dc = int(linhas[4])          # Distance between C-planes (Dc = 0 for non-equidistantly available C-planes)
        self.Ng = int(linhas[5])          # Number Ng of luminous intensities in each C-plane (usually 19 or 37)
        self.Dg = int(linhas[6])          # Distance between luminous intensities per C-plane (Dg = 0 for non-equidistantly available luminous intensities in C-planes)
        self.LumName = linhas[8]          # Luminaire name
        self.lorl = float(linhas[22])     # LORL - Light output ratio luminaire (%)
        self.n = int(linhas[25])          # Number n of standard sets of lamps (optional, also extendable on company-specific basis)
        i = 42 + (self.n-1)*6
        j = i + self.Mc
        self.AnglesC = linhas[i:j]         # Angles C (beginning with 0 degrees) Mc * 6
        i = j
        j = i + self.Ng
        self.AnglesG = linhas[i:j]         # Angles G (beginning with 0 degrees) Ng * 6
        self.LumInt = []
        Mc1, Mc2 = Mcx(self.Isym,self.Mc)
        Planes = int(Mc2-Mc1+1)
        for k in range(Planes):
            i = j
            j = i + self.Ng
            self.LumInt.append([float(linha) for linha in linhas[i:j]])    # Luminous intensity distribution (candela / 1000 lumens)
