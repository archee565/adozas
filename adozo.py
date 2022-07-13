#!/usr/bin/python
import matplotlib.pyplot as plt

# forrasok:
# https://www.hypercortex.hu/atalanyadozas-ujratoltve-2022/


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
    minimalber_brutto = 200000
    koltseghanyad = 0.4
    mentesitett = minimalber_brutto*12/2
    adoalap = (1-koltseghanyad)*bevetel
    szja = max( (adoalap-mentesitett)*0.15,0)
    tbj = max(adoalap*0.185,minimalber_brutto*0.185)
    szocho = max(min(adoalap*0.13,628000),minimalber_brutto*1.125*0.13)
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
    cx.append(bevetel/1e6)
    cy_szja.append(szjaado(bevetel)/bevetel*100)
    cy_atalany.append(  atalany(bevetel)/bevetel * 100 )


plt.plot(cx, cy_szja)
plt.plot(cx, cy_atalany)
plt.ylim([0, 100])
plt.xlabel('éves bevetel (millio HUF)')
plt.ylabel('ado%')
plt.title('TAO+SZJA vs átalány')
plt.show()
