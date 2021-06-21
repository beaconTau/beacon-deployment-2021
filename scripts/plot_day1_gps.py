import os
import sys
import inspect
import numpy
import matplotlib.pyplot as plt

plt.ion()

from beacon.tools import info
from beacon_deployment_2021.scripts.plot_array import plotStation, printBaselines
default_deploy = info.returnDefaultDeploy()



if __name__ == '__main__':
    try:
        deploy_index_1 = os.path.join(os.environ['BEACON_DEPLOYMENT_DIR'], 'config/deploy_30.json')
        deploy_index_2 = os.path.join(os.environ['BEACON_DEPLOYMENT_DIR'], 'config/rtk-gps-day1-june20-2021.json')
        printBaselines(deploy_index=deploy_index_1, calculate_phase=True)
        printBaselines(deploy_index=deploy_index_2, calculate_phase=False)
        #fig, ax = plotStation(deploy_index=deploy_file,plot_phase=False)


        antennas_physical_1, antennas_phase_hpol_1, antennas_phase_vpol_1 = info.loadAntennaLocationsENU(deploy_index=deploy_index_1)
        antennas_physical_2, antennas_phase_hpol_2, antennas_phase_vpol_2 = info.loadAntennaLocationsENU(deploy_index=deploy_index_2)

        colors = ['b','g','r','c']

        fig = plt.figure()
        plt.title('New Physical Compared to Old')
        ax = fig.add_subplot(111, projection='3d')

        for i, a in antennas_physical_1.items():
            ax.scatter(a[0], a[1], a[2], marker='o',color=colors[i],label='Old Physical %i'%i,alpha=0.8)

        for i, a in antennas_physical_2.items():
            ax.scatter(a[0], a[1], a[2], marker='*',color=colors[i],label='New Physical %i'%i,alpha=0.8)

        for i in range(4):
            ax.plot([antennas_physical_1[i][0],antennas_physical_2[i][0]],[antennas_physical_1[i][1],antennas_physical_2[i][1]],[antennas_physical_1[i][2],antennas_physical_2[i][2]],color=colors[i],linestyle='-',alpha=0.5)

        ax.set_xlabel('E (m)')
        ax.set_ylabel('N (m)')
        ax.set_zlabel('Relative Elevation (m)')
        plt.legend()

        #######################

        fig = plt.figure()
        plt.title('New Physical Compared to Calibration Hpol')
        ax = fig.add_subplot(111, projection='3d')

        for i, a in antennas_phase_hpol_1.items():
            ax.scatter(a[0], a[1], a[2], marker='o',color=colors[i],label='Calibrated Hpol %i'%i,alpha=0.8)

        for i, a in antennas_physical_2.items():
            ax.scatter(a[0], a[1], a[2], marker='*',color=colors[i],label='New Physical %i'%i,alpha=0.8)

        for i in range(4):
            ax.plot([antennas_phase_hpol_1[i][0],antennas_physical_2[i][0]],[antennas_phase_hpol_1[i][1],antennas_physical_2[i][1]],[antennas_phase_hpol_1[i][2],antennas_physical_2[i][2]],color=colors[i],linestyle='-',alpha=0.5)

        ax.set_xlabel('E (m)')
        ax.set_ylabel('N (m)')
        ax.set_zlabel('Relative Elevation (m)')
        plt.legend()

        #######################

        fig = plt.figure()
        plt.title('New Physical Compared to Calibration vpol')
        ax = fig.add_subplot(111, projection='3d')

        for i, a in antennas_phase_vpol_1.items():
            ax.scatter(a[0], a[1], a[2], marker='o',color=colors[i],label='Calibrated Vpol %i'%i,alpha=0.8)

        for i, a in antennas_physical_2.items():
            ax.scatter(a[0], a[1], a[2], marker='*',color=colors[i],label='New Physical %i'%i,alpha=0.8)

        for i in range(4):
            ax.plot([antennas_phase_vpol_1[i][0],antennas_physical_2[i][0]],[antennas_phase_vpol_1[i][1],antennas_physical_2[i][1]],[antennas_phase_vpol_1[i][2],antennas_physical_2[i][2]],color=colors[i],linestyle='-',alpha=0.5)

        ax.set_xlabel('E (m)')
        ax.set_ylabel('N (m)')
        ax.set_zlabel('Relative Elevation (m)')
        plt.legend()



    except Exception as e:
        print('Error in main loop.')
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    plt.show(block=True) # I hate having to do this but I can't get it to work interactively otherwise.