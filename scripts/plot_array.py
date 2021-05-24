import os
import sys
import inspect
import numpy
import matplotlib.pyplot as plt
plt.ion()

from beacon.tools import info
default_deploy = info.returnDefaultDeploy()


def plotStationAndPulsers(deploy_index=default_deploy,plot_phase=False):
    '''
    Currently only intended to plot the most recent station with the three pulsers that we used for it.
    '''
    try:
        antennas_physical, antennas_phase_hpol, antennas_phase_vpol = info.loadAntennaLocationsENU(deploy_index=deploy_index)

        print(info.loadAntennaLocationsENU(deploy_index=deploy_index))

        colors = ['b','g','r','c']

        fig = plt.figure()
        if str(deploy_index).isdigit():
            fig.canvas.set_window_title('Antenna Locations: Calibration %i'%deploy_index)
        else:
            fig.canvas.set_window_title('Antenna Locations: %s'%os.path.split(deploy_index)[-1].replace('.json', '').replace('_', ' '))
        ax = fig.add_subplot(111, projection='3d')

        for i, a in antennas_physical.items():
            ax.scatter(a[0], a[1], a[2], marker='o',color=colors[i],label='Physical %i'%i,alpha=0.8)

        if plot_phase == True:
            for i, a in antennas_phase_hpol.items():
                ax.plot([antennas_physical[i][0],antennas_phase_hpol[i][0]],[antennas_physical[i][1],antennas_phase_hpol[i][1]],[antennas_physical[i][2],antennas_phase_hpol[i][2]],color=colors[i],linestyle='--',alpha=0.5)
                ax.scatter(a[0], a[1], a[2], marker='*',color=colors[i],label='%s Phase Center %i'%('Hpol', i),alpha=0.8)
            for i, a in antennas_phase_vpol.items():
                ax.plot([antennas_physical[i][0],antennas_phase_vpol[i][0]],[antennas_physical[i][1],antennas_phase_vpol[i][1]],[antennas_physical[i][2],antennas_phase_vpol[i][2]],color=colors[i],linestyle='--',alpha=0.5)
                ax.scatter(a[0], a[1], a[2], marker='^',color=colors[i],label='%s Phase Center %i'%('Vpol', i),alpha=0.8)

        ax.set_xlabel('E (m)')
        ax.set_ylabel('N (m)')
        ax.set_zlabel('Relative Elevation (m)')
        plt.legend()
        return fig, ax
    except Exception as e:
        print('\nError in %s'%inspect.stack()[0][3])
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

if __name__ == '__main__':
    #plt.ion()
    for deploy_file in [30,os.path.join(os.environ['BEACON_DEPLOYMENT_DIR'], 'config/deploy_30.json') ]:
        try:
            plt.close('all')
            fig, ax = plotStationAndPulsers(deploy_index=deploy_file,plot_phase=False)

        except Exception as e:
            print('Error in main loop.')
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    plt.show(block=True) # I hate having to do this but I can't get it to work interactively otherwise.