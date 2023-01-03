#!/usr/bin/python
import matplotlib.pyplot as plt

# forrasok:
# https://optitax.hu/adooptimalizalas/2022-es-minimalber-es-garantalt-berminimum
# https://konyvelescentrum.hu/adok-es-jarulekok-kozterhek/egyeni-vallalkozo-adozasanak-osszehasonlitasa-kata-versus-szja/  <- 2021, már nem teljesen aktuális!
# https://www.hypercortex.hu/atalanyadozas-ujratoltve-2022/


berminimum_brutto = 296400
minimalber_brutto = 232000
huf_to_eur = 400
max_income = 30 # million HUF


def szjaado(bevetel):
    egyebkoltseg = 0
    ugyvezeto_brutto = 12*berminimum_brutto # berminimum
    ugyvezeto_superbrutto = ugyvezeto_brutto*1.13
    ugyvezeto_netto = ugyvezeto_brutto*133/200
    ugyvezetoado = ugyvezeto_superbrutto - ugyvezeto_netto
    eredmeny = max(bevetel-ugyvezeto_superbrutto-egyebkoltseg,0)
    a = eredmeny
    a *= 0.98 # IPA
    a *= 0.91 # TAO
    szocho_alap_felso_korlat = minimalber_brutto*24
    szocho = min(a,(szocho_alap_felso_korlat-ugyvezeto_brutto))*0.13
    szja = a*0.15
    a -= szocho + szja
    netto_osztalek = a
    return ugyvezetoado + (eredmeny-netto_osztalek)


def atalany(bevetel):
    koltseghanyad = 0.4
    mentesitett = minimalber_brutto*12/2
    adoalap = (1-koltseghanyad)*bevetel
    szja = max( (adoalap-mentesitett)*0.15,0)
    tbj = max( (adoalap-mentesitett)*0.185,berminimum_brutto*12*0.185)
#    szocho_alap_felso_korlat = minimalber_brutto*24
#    szocho = max(min( (adoalap-mentesitett),szocho_alap_felso_korlat),berminimum_brutto*12*1.125)*0.13
    szocho = max( (adoalap-mentesitett),berminimum_brutto*12*1.125)*0.13
    ipa = adoalap*1.2*0.02
    if bevetel>12*10*minimalber_brutto:
        return bevetel
    else:
        return szja+tbj+szocho+ipa

def kata(bevetel):
    bunteto = 0.4 * max(0,bevetel-18e6)
    return bunteto + 50000 + 12*50000  # IPA es SZJA KATA


#  forras wikipedia
def nemet_szja(x):
    if (x<10347):
         return 0
    if x<14926:
        return (0.14 + (x-10347)*1088.67e-8)*(x-10347)
    if x<58596:
        return (0.2397+(x-14926)*206.43e-8)*(x-14926) + 869.32
    if x<277825:
        return 0.42*x-9336.45
    return 0.45*x-17671.2


def nemet(bevetel):
    egeszseg_biztositas = 12*200 # kotelezo, de vannak olcsobbak
#    return nemet_szja(bevetel)
    a = max(bevetel - 24500,0) # minus freiBetrag
    gewerbesteuer = 0.035*3.91*a  # Hessen
    szja_alap = bevetel-gewerbesteuer
    return gewerbesteuer + nemet_szja(szja_alap) + egeszseg_biztositas


# forras https://www.expatica.com/es/finance/taxes/freelance-tax-spain-471615/#socialsecurity
def spanyol(bevetel):
    a = bevetel
    b = min(a,12450)
    tax = b*0.19
    a-=b
    b = min(a,20200-12450)
    tax += b*0.24
    a-=b
    b = min(a,35200-20200)
    tax += b*0.3
    a-=b
    b = min(a,60000-35200)
    tax += b*0.37
    a-=b
    b = min(a,300000-60000)
    tax += b*0.45
    a-=b
    tax += a*0.47
    socialpago = 286.15*12
    return tax+socialpago


# forras https://www.expatica.com/pt/finance/taxes/self-employment-freelance-and-corporate-tax-in-portugal-1092039/#system
def portugal(bevetel):
    caps = [7116,10736,15216,19696,25076,36757,48033,75009,1e30]
    rates = [0.145,0.23,0.265,0.285,0.35,0.37,0.435,0.45,0.48]
    a = bevetel
    tax = 0.
    for i in range(0,len(caps)):
        b = min(caps[i],a)
        tax += rates[i]*b
        a-=b
    seguro_social = bevetel*0.214
    return tax + seguro_social


# forras https://www.czechmobility.info/en/topics/status-of-the-artist/status-of-the-artist-in-the-czech-republic/self-employed-person
# valószínűleg téves a cseh: 
def cseh(bevetel):
    social = 12*(1906+115+2061)
    if (bevetel<67756):
        social = 0
    return social + bevetel*0.15


  
cx = []
cy_szja = []
cy_atalany = []
cy_kata = []
cy_nemet = []
cy_spanyol = []
cy_portugal = []
cy_cseh = []

for x in range(1,1000):
    bevetel = 1 + max_income*1e6*(x/1000)
    beveteleur = bevetel/huf_to_eur
    bevetel_czk = bevetel/16.6
    cx.append(bevetel/1e6)
    cy_szja.append(szjaado(bevetel)/bevetel*100)
    cy_atalany.append(  atalany(bevetel)/bevetel * 100 )
    cy_kata.append(  kata(bevetel)/bevetel * 100 )
    cy_nemet.append( nemet(beveteleur) / beveteleur * 100 )
    cy_spanyol.append( spanyol(beveteleur) / beveteleur * 100 )
    cy_portugal.append( portugal(beveteleur) / beveteleur * 100 )
    cy_cseh.append( cseh(bevetel_czk) / bevetel_czk * 100 )


plt.plot(cx, cy_szja,label='TAO+SZJA',linestyle='dashed',)
plt.plot(cx, cy_atalany,label="átalany",linestyle='dashed',)
plt.plot(cx, cy_kata,label="KATA sok ügyfél",linestyle='dashed',)
plt.plot(cx, cy_nemet,label="Germany")
plt.plot(cx, cy_spanyol,label="Spain")
plt.plot(cx, cy_portugal,label="Portugalia")
#plt.plot(cx, cy_cseh,label="csehia")

plt.legend(loc='upper center', shadow=True, fontsize='medium')
plt.ylim([0, 102])
plt.xlim([0, max_income])
plt.xlabel('éves bevetel (millio HUF)')
plt.ylabel('ado%')
plt.title('TAO+SZJA vs átalány')
plt.show()
