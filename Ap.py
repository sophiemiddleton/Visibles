# Example of how to use the LHE Reader for an Ap decay (didecay) example
from lhereader import readLHEF
from ROOT import TCanvas, TH1F, TH2F, TLorentzVector, TF1
import math
import matplotlib.pyplot as plt
import numpy as np
import argparse
from sklearn.preprocessing import normalize
import matplotlib as mpl # for plotting
import matplotlib.pyplot as plt # common shorthand
import mplhep as hep
plt.style.use(hep.style.CMS)
plt.rcParams.update({'font.size':32})

path = "/Users/sophie/LDMX/software/NewClone/Aps/displaced/ApLHEs"

def main(args):
    # Extract decays:

    pts = []
    pzs = []
    elecpzs=[]
    angles = []
    angles_z =[]
    alpenergies = []
    alpfracenergies = []
    alpsangles = []
    alppxs = []
    alppts = []
    alppys = []
    alppzs = []
    alpdises=[]
    alpdzs = []
    weightz = []
    weightsg = []
    weights1g = []
    for i, data in enumerate(args.fullfilename):
        data=[]
        print(str(args.fullfilename[i]))
        data_list=readLHEF(str(args.fullfilename[i]))
        decays=data_list.getParticlesByIDs([11,-11])
        Aps=data_list.getParticlesByIDs([622])
        electrons=data_list.getParticlesByIDs([11])

        # make an empty vector to fill with the quantity you want to plot
        pt = []
        pz = []
        angle = []
        anglez = []
        ndecay=0
        weight = []
        weightg = []
        weight1g = []
        elecpz=[]
        # TLorentzVector for the two decays
        gamma1_4mom = TLorentzVector()
        gamma2_4mom = TLorentzVector()
        # Loop over all decays:
        for g in decays:
            # Outgoing decays (status ==1):
            if (g.status == 1):
                ndecay+=1
                # all decays
                pt.append(g.p4.Pt())
                pz.append(g.p4.Pz())
                weight1g.append(1/ndecay)
                # to get details of each decay (assume two per event in even structure - this should be OK)
                if ndecay%2!=0:
                    print(ndecay, "this is the outgoing first decay in event")
                    gamma1_4mom = g.p4
                if ndecay%2==0:
                    print(ndecay,"this is the outgoing second decay in event")
                    gamma2_4mom = g.p4
                    # angle between the two decays
                    print("---------------------")
                    angle.append(gamma1_4mom.Angle(gamma2_4mom.Vect()))
                    weightg.append(1/ndecay)

        pts.append(pt)
        pzs.append(pz)
        angles.append(angle)
        weightsg.append(weightg)
        weights1g.append(weight1g)
        nAps = 1
        alp_energy = []
        alp_frac_e = []
        alp_px = []
        alp_py = []
        alp_pz = []
        alp_angle = []
        alp_p = []
        alp_pt = []
        alp_vtims = []
        alp_mass = []
        alp_gammas = []
        alp_dz = []
        alp_dis = []
        velocities = []
        vtims = []
        for a in Aps:
            alp_energy.append(a.energy/10)
            alp_frac_e.append(a.energy/80)
            alp_px.append(a.p4.Px())
            alp_py.append(a.p4.Py())
            alp_pz.append(a.p4.Pz()/10)
            alp_pt.append(math.sqrt(a.p4.Px()*a.p4.Px() + a.p4.Py()*a.p4.Py()))
            alp_angle.append(math.atan(a.p4.Px()/a.p4.Pz()))
            alp_vtims.append(a.vtim)
            alp_mass.append(a.mass)
            alp_gammas.append(a.p4.Gamma())
            alp_p.append(a.p4.P())
            velocity = a.p4.Vect() / (a.p4.Gamma() * a.mass) #in units of c?
            velocities.append(velocity[2])
            displacement = velocity * a.vtim   #in mm
            vtims.append(a.vtim)
            #calculate magnitude
            alp_dis.append(np.sqrt(displacement[0]**2 + displacement[1]**2 + displacement[2]**2))
            alp_dz.append(displacement[2])
            weight.append(1/(nAps))
            nAps+=1
        alpenergies.append(alp_energy)
        alpfracenergies.append(alp_frac_e)
        alppxs.append(alp_px)
        alppys.append(alp_py)
        alppzs.append(alp_pz)
        alppts.append(alp_pt)
        alpsangles.append(alp_angle)
        alpdises.append(alp_dis)
        alpdzs.append(alp_dz)
        weightz.append(weight)
        for e in electrons:
            if (e.status == 1):
                elecpz.append(e.p4.Pz())
        elecpzs.append(elecpz)

    styles = ["solid","solid","solid"]#,"solid","solid","solid","solid"]
    colors = ["#0133ff","#9900cc","#049900"]#,"blue","orange","magenta","red"]
    masses = ["5MeV","50MeV","100MeV"]#,"100MeV","200MeV","300MeV","500MeV"]
    procs = ["Ap=5MeV","Ap=50MeV","Ap=100MeV"]#,"prima","prima","prima","prima"]
    labels = ["Ap=5MeV","Ap=50MeV","Ap=100MeV"]#"masses[0],masses[1],masses[2],masses[3],masses[4],masses[5]]
    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(pts):

        #plt.title("e+/e- Transverse Momentum")
        n, bins, patches = ax.hist(pts[i],
                                   bins=50,
                                   range=(0,2),
                                   histtype = 'step',
                                   linestyle = styles[i],
                                   color = colors[i],
                                   label=labels[i],
                                   weights=weights1g[i])
    #plt.legend()
    ax.set_yscale('log')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('events per bin')
    ax.set_xlabel('pt of all e+/e-s [GeV/c]')
    fig.savefig('signalpt.pdf')

    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,**{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(pzs):

        #plt.title("e+/e- Pz Momentum")
        n, bins, patches = ax.hist(pzs[i],
                                   bins=25,
                                   range=(0,8),
                                   histtype = 'step',
                                   linestyle = styles[i],
                                   color = colors[i],
                                   label=labels[i],
                                   weights=weights1g[i])
    #plt.legend()
    ax.set_yscale('log')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('pz of all e+/e-s [GeV/c]')
    fig.savefig('signalelecpz.pdf')



    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(angles):

        #plt.title("Angle between e+/e-s")
        n, bins, patches = ax.hist(angles[i],
                                   bins=25,
                                   range=(0,math.pi),
                                   histtype = 'step',
                                   linestyle = styles[i],
                                   color = colors[i],
                                   label=labels[i],
                                   weights=weightsg[i])
                                   # Put a legend to the right of the current axis

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_yscale('log')
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('angle between e+/e-s [rad]')
    fig.savefig('signalangle.pdf')

    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(alpenergies):

        ##plt.title("mAp= "+str(args.mass)+" GeV")
        #normalize([alpenergies[i]])[0],
        n, bins, patches = ax.hist( alpenergies[i],
                                    bins=25,
                                    range=(0,8),
                                    histtype = 'step',
                                    linestyle = styles[i],
                                    color = colors[i],
                                    label=labels[i],
                                    weights=weightz[i])

    #plt.legend()
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_yscale('log')
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('Ap Energy [GeV]')
    fig.savefig('ap_energy.pdf')

    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(alpenergies):

        ##plt.title("mAp= "+str(args.mass)+" GeV")
        #normalize([alpenergies[i]])[0],
        n, bins, patches = ax.hist( alpfracenergies[i],
                                    bins=25,
                                    range=(0,1),
                                    histtype = 'step',
                                    linestyle = styles[i],
                                    color = colors[i],
                                    label=labels[i],
                                    weights=weightz[i])

        #plt.legend()
        # Shrink current axis by 20%

        ax.legend(loc='upper right')
        ax.set_yscale('log')
        ax.set_ylabel('Arb. Units')
        ax.set_xlabel('Ap Energy/Beam Energy')
        fig.savefig('ap_energy_frac.pdf')


    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(alpenergies):
        ##plt.title("mAp= "+str(args.mass)+" GeV")
        #normalize([alpenergies[i]])[0],
        n, bins, patches = ax.hist( alppxs[i],
                                    bins=25,
                                    range=(-8,8),
                                    histtype = 'step',
                                    linestyle = styles[i],
                                    color = colors[i],
                                    label=labels[i],
                                    weights=weightz[i])
    #plt.legend()
    ax.set_yscale('log')
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('Ap Px [GeV/c]')
    fig.savefig('ap_px.pdf')

    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(alpenergies):
        ##plt.title("mAp= "+str(args.mass)+" GeV")
        #normalize([alpenergies[i]])[0],
        n, bins, patches = ax.hist( alppts[i],
                                    bins=25,
                                    range=(0,8),
                                    histtype = 'step',
                                    linestyle = styles[i],
                                    color = colors[i],
                                    label=labels[i],
                                    weights=weightz[i])
    #plt.legend()
    ax.set_yscale('log')
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('Ap Pt [GeV/c]')
    fig.savefig('ap_pt.pdf')

    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(alpenergies):
        n, bins, patches = ax.hist( alppys[i],
                                    bins=25,
                                    range=(-8,8),
                                    histtype = 'step',
                                    linestyle = styles[i],
                                    color = colors[i],
                                    label=labels[i],
                                    weights=weightz[i])
    #plt.legend()
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_yscale('log')
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('Ap Py [GeV/c]')
    fig.savefig('ap_py.pdf')

    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(alpenergies):
        n, bins, patches = ax.hist( alppzs[i],
                                    bins=25,
                                    range=(0,8),
                                    histtype = 'step',
                                    linestyle = styles[i],
                                    color = colors[i],
                                    label=labels[i],
                                    weights=weightz[i])
    #plt.legend()
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_yscale('log')
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('Ap Pz [GeV/c]')
    fig.savefig('ap_pz.pdf')

    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(alpenergies):
        n, bins, patches = ax.hist( alpsangles[i],
                                    bins=25,
                                    range=(-0.5,0.5),
                                    histtype = 'step',
                                    linestyle = styles[i],
                                    color = colors[i],
                                    label=labels[i],
                                    weights=weightz[i])
    #plt.legend()
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_yscale('log')
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('Ap Angle [rad]')
    fig.savefig('ap_angle.pdf')

    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(alpdises):

        #plt.title("Ap Displacement Magnitude")
        n, bins, patches = ax.hist(alpdises[i],
                                   bins=25,
                                   range=(250,5500),
                                   histtype = 'step',
                                   linestyle = styles[i],
                                   color = colors[i],
                                   label=labels[i],
                                   weights=weightz[i])
    #plt.legend()
    ax.set_yscale('log')
    #ax.set_xscale('log')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('Ap Displacement Mag [mm]')
    fig.savefig('alpdis.pdf')

    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(alpdzs):

        #plt.title("Ap Displacement in Z")
        n, bins, patches = ax.hist(alpdzs[i],
                                   bins=25,
                                   range=(0,10),
                                   histtype = 'step',
                                   linestyle = styles[i],
                                   color = colors[i],
                                   label=labels[i],
                                   weights=weightz[i])
    #plt.legend()
    ax.set_yscale('log')
    #ax.set_xscale('log')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('Ap Displacement Z [mm]')
    fig.savefig('alpdz.pdf')


    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(alppzs):

        ##plt.title("Photon Pz Momentum")
        plt.hist2d(alppzs[i], alpsangles[i], bins=(50,50), cmap=plt.cm.jet)
        ax.set_ylabel('Ap Pz [GeV/c]')
        ax.set_xlabel('Ap Angle [rad]')
        fig.savefig('Ap2D_angle_energy'+str(i)+'.pdf')

    fig, ax = plt.subplots(1,1)
    hep.cms.text(text="Simulation Internal", loc=0, ax=ax,
            **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True, False)})
    for i, data in enumerate(elecpzs):

        #plt.title("Electron Pz Momentum")
        n, bins, patches = ax.hist(elecpzs[i],
                                   bins=25,
                                   range=(0,8),
                                   histtype = 'step',
                                   linestyle = styles[i],
                                   color = colors[i],
                                   label=labels[i])

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_yscale('log')
    ax.set_ylabel('Arb. Units')
    ax.set_xlabel('pz of electrons [GeV/c]')
    fig.savefig('elecpz.pdf')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    files = ["unweighted_events_5_MeV.lhe","unweighted_events_50_MeV.lhe","unweighted_events_100_MeV.lhe"]#["m10_prima_vertex.lhe","m50_prima_vertex.lhe","m100_prima_vertex.lhe","m200_prima_vertex.lhe","m300_prima_vertex.lhe","m500_prima_vertex.lhe"]
    parser.add_argument("--fullfilename", help="full filename with path", default=files)
    parser.add_argument("--process", help="Primakoff or Photon Fusion")
    parser.add_argument("--mass", help="Ap mass")
    args = parser.parse_args()
    (args) = parser.parse_args()
    main(args)
