#!/usr/bin/python
import matplotlib.pyplot as plt

def szjaado(bevetel):
    egyebkoltseg = 0
    ugyvezeto_brutto = 12*200000
    ugyvezeto_superbrutto = ugyvezeto_brutto*1.13
    ugyvezeto_netto = ugyvezeto_brutto*133/200
    ugyvezetoado = ugyvezeto_superbrutto - ugyvezeto_netto
    eredmeny = max(bevetel-ugyvezeto_superbrutto-egyebkoltseg,0)
    a = eredmeny
    a *= 0.98 # IPA
    a *= 0.91 # TAO
    szocho = min(a*0.13,628000-ugyvezeto_brutto*0.13)
    szja = a*0.15
    a -= szocho + szja
    netto_osztalek = a
    return ugyvezetoado + (eredmeny-netto_osztalek)


def atalany(bevetel):
    koltseghanyad = 0.4
    adoalap = (1-koltseghanyad)*bevetel
    szja = adoalap*0.15
    tbj = adoalap*0.185
    szocho = min(adoalap*0.13,628000)
    ipa = adoalap*1.2*0.02
    if bevetel>12*10*200000:
        return bevetel
    else:
        return szja+tbj+szocho+ipa

  
cx = []
cy_szja = []
cy_atalany = []

for x in range(1,1000):
    bevetel = 1 + 26*1e6*(x/1000)
    cx.append(bevetel)
    cy_szja.append(szjaado(bevetel)/bevetel*100)
    cy_atalany.append(  atalany(bevetel)/bevetel * 100 )


plt.plot(cx, cy_szja)
plt.plot(cx, cy_atalany)
plt.ylim([0, 100])
plt.xlabel('bevetel')
plt.ylabel('ado%')
plt.title('TAO+SZJA vs átalány')
plt.show()
