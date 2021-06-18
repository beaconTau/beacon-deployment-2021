import os
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import sys
import math
#import BeaconTau as bt
import beacon_data_reader as bdr
from scipy.optimize import minimize

class Antenna:
    def __init__(self,x0,y0,z0):
        self.x=x0
        self.y=y0
        self.z=z0

class Vector:
    def __init__(self,x0,y0,z0):
        self.x=x0
        self.y=y0
        self.z=z0


#   To run this code, you must have Ben Strutt's BeaconTau python package installed!
#   If you just run "python generate_correlator.py" it will run the code in "main"
#   If you want to reference these functions in another code, include the following on the top of the code:
#   from generate_correlator import Antenna
#   from generate_correlator import correlator #(or whatever other function you want)



def setup(run_num, ent_num, pol):
    #dd= bt.DataDirectory()
    #r=dd.run(run_num)
    #e = r.get_entry(ent_num)
    #times = r.get_entry(ent_num).times()

    d = bdr.Reader(os.environ['BEACON_DATA_DIR'], run_num)
    d.setEntry(ent_num)
    times = d.t()

    if(pol == 1): #Hpol
        #ADC0 = np.asarray(e.channel(0))
        #ADC1 = np.asarray(e.channel(2))
        #ADC2 = np.asarray(e.channel(4))
        #ADC3 = np.asarray(e.channel(6))
        ADC0 = d.wf(0)
        ADC1 = d.wf(2)
        ADC2 = d.wf(4)
        ADC3 = d.wf(6)
    else: #Vpol
        #ADC0 = np.asarray(e.channel(1))
        #ADC1 = np.asarray(e.channel(3))
        #ADC2 = np.asarray(e.channel(5))
        #ADC3 = np.asarray(e.channel(7))
        ADC0 = d.wf(1)
        ADC1 = d.wf(3)
        ADC2 = d.wf(5)
        ADC3 = d.wf(7)

    volt0 = (ADC0-sum(ADC0)/len(ADC0))
    volt1 = (ADC1-sum(ADC1)/len(ADC1))
    volt2 = (ADC2-sum(ADC2)/len(ADC2))
    volt3 = (ADC3-sum(ADC3)/len(ADC3))
    return (volt0,volt1,volt2,volt3,times)
        
def get_norm(theta, phi): #negatives because wave travels towards antennas, so normal vector should be opposite direction from angles
    x=math.cos(math.radians(phi))*math.sin(math.radians(theta))*-1
    y=math.sin(math.radians(phi))*math.sin(math.radians(theta))*-1
    z=math.cos(math.radians(theta))*-1
    return Vector(x, y, z)

#time delay calculation.
#postive time delay: hits vector "smaller valued" antenna first
#negative time delay: hits second "larger valued" antenna first
def time_delay(ant,vec):
    #print((ant.x*vec.x+ant.y*vec.y+ant.z*vec.z)/3e8*1e9)
    return (ant.x*vec.x+ant.y*vec.y+ant.z*vec.z)/3e8*1e9

def asub(ant2, ant1):
    return Antenna(ant2.x-ant1.x, ant2.y-ant1.y, ant2.z-ant1.z)


#Loop over thetas and phis:

def generate_time_arrays(A0,A1,A2,A3):

    #theta_vec = np.linspace(0,180,60).astype(int)
    #phi_vec = np.linspace(-180,180,120)

    theta_vec = np.arange(0.,180.,0.1)
    phi_vec = np.arange(-180.,180.,0.1)
    
    t1 = np.zeros([len(theta_vec),len(phi_vec)])
    t2 = np.zeros([len(theta_vec),len(phi_vec)])
    t3 = np.zeros([len(theta_vec),len(phi_vec)])
    t4 = np.zeros([len(theta_vec),len(phi_vec)])
    t5 = np.zeros([len(theta_vec),len(phi_vec)])
    t6 = np.zeros([len(theta_vec),len(phi_vec)])

    #Calculate time delays for each correlation box:

    
    for i in range(len(theta_vec)):
        for j in range(len(phi_vec)):
            norm_vector = get_norm(theta_vec[i],phi_vec[j])#norm vector at A0=

            #Start with Antenna 0. Calculate dot product of norm with v1,v2,v3.
            t1[i,j]=-time_delay(asub(A1,A0),norm_vector) #time in nanoseconds between A0 and A1
            t2[i,j]=-time_delay(asub(A2,A0),norm_vector) #A0 and A2
            t3[i,j]=-time_delay(asub(A3,A0),norm_vector) #A0 and A3
            t4[i,j]=-time_delay(asub(A2,A1),norm_vector) #A1 and A2
            t5[i,j]=-time_delay(asub(A3,A1),norm_vector) #A1 and A3
            t6[i,j]=-time_delay(asub(A3,A2),norm_vector) #A2 and A3

    return(t1,t2,t3,t4,t5,t6)


#def correlator(volt0,volt1,volt2,volt3,t1,t2,t3,t4,t5,t6):
def correlator(times,volt0,volt1,volt2,volt3,A0,A1,A2,A3,include=[1,1,1,1,1,1],show_plots=True):

    #theta_vec = np.linspace(0,180,60).astype(int)
    #phi_vec = np.linspace(-180,180,120)

    theta_vec = np.arange(0.,180.,0.1)
    phi_vec = np.arange(-180.,180.,0.1)

    dt = times[1]-times[0]
    
    t1,t2,t3,t4,t5,t6 = generate_time_arrays(A0,A1,A2,A3)
    center = len(times)
    cor1 = np.asarray(signal.correlate(volt0,volt1))
    cor2 = np.asarray(signal.correlate(volt0,volt2))
    cor3 = np.asarray(signal.correlate(volt0,volt3))
    cor4 = np.asarray(signal.correlate(volt1,volt2))
    cor5 = np.asarray(signal.correlate(volt1,volt3))
    cor6 = np.asarray(signal.correlate(volt2,volt3))


    d1=cor1[np.rint(t1/dt+(center-1)).astype(int)]#0 and 1
    d2=cor2[np.rint(t2/dt+(center-1)).astype(int)]#0 and 2
    d3=cor3[np.rint(t3/dt+(center-1)).astype(int)]#0 and 3
    d4=cor4[np.rint(t4/dt+(center-1)).astype(int)]#1 and 2
    d5=cor5[np.rint(t5/dt+(center-1)).astype(int)]#1 and 3
    d6=cor6[np.rint(t6/dt+(center-1)).astype(int)]#2 and 3


    corr_array = []
    if include[0]:
    	corr_array.append(d1)
    if include[1]:
    	corr_array.append(d2)
    if include[2]:
    	corr_array.append(d3)
    if include[3]:
    	corr_array.append(d4)
    if include[4]:
    	corr_array.append(d5)
    if include[5]:
    	corr_array.append(d6)
    corr_array = np.array(corr_array)
    corr_val=np.mean(corr_array,axis=0)
    
    if( show_plots):
       fig=plt.figure(3)
       ax = fig.add_subplot(1,1,1)
       im = ax.imshow(corr_val, interpolation='none', extent=[-180,180,180,0],cmap=plt.cm.coolwarm) #cmap=plt.cm.jet)
       fig.colorbar(im, ax=ax)
       plt.xlabel('Azimuth Angle (Degrees)')
       plt.ylabel('Zenith Angle (Degrees)')

    #print('maximum of corr_val is: ', np.unravel_index(corr_val.argmax(),corr_val.shape))
    a1,a2=np.unravel_index(corr_val.argmax(),corr_val.shape)
    #print(corr_val[a1,a2])
    theta_best=theta_vec[a1]
    phi_best=phi_vec[a2]
    while(theta_best>125):
        corr_val[a1,a2]=0
        a1,a2=np.unravel_index(corr_val.argmax(),corr_val.shape)
        theta_best=theta_vec[a1]
        phi_best=phi_vec[a2]
    t1_best=t1[a1,a2]
    t2_best=t2[a1,a2]
    t3_best=t3[a1,a2]
    t4_best=t4[a1,a2]
    t5_best=t5[a1,a2]
    t6_best=t6[a1,a2]


    print("From the correlation plot:")
    print("Best zenith angle:",theta_best)
    print("Best azimuth angle:",phi_best)
    print('predicted time delays between A0 and A1:', t1_best)
    print('predicted time delays between A0 and A2:', t2_best)
    print('predicted time delays between A0 and A3:', t3_best)

    if(show_plots):
        plt.figure(4)
        plt.plot(times, volt0, label="Antenna 0")
        plt.plot(times+t1_best, volt1, label="Antenna 1")
        plt.plot(times+t2_best, volt2, label="Antenna 2")
        plt.plot(times+t3_best, volt3, label="Antenna 3")
        plt.legend()
        plt.title("Aligned Pulses from Best Correlator Bin")


    d1_best=(np.argmax(cor1)-(center-1))*dt
    d2_best=(np.argmax(cor2)-(center-1))*dt
    d3_best=(np.argmax(cor3)-(center-1))*dt

    print('')
    print('Compare to perfect time delays (not from map):')
    print('A0 and A1:',d1_best)
    print('A0 and A2:',d2_best)
    print('A0 and A3:',d3_best)


    if( show_plots):
        #plt.savefig('/home/avz5228/Documents/correlator.png')
        plt.show()
    
    return t1_best, t2_best, t3_best, d1_best, d2_best, d3_best, theta_best, phi_best, corr_val.argmax(), corr_val


def align(times,volt0,volt1,volt2,volt3,show_plots=True):

    n = len(times)
        
    cor1 = np.asarray(signal.correlate(volt0,volt1,mode='full'))
    cor2 = np.asarray(signal.correlate(volt0,volt2,mode='full'))
    cor3 = np.asarray(signal.correlate(volt0,volt3,mode='full'))
    
    volt1_aligned = np.roll(volt1, np.argmax(cor1)-(n-1))
    volt2_aligned = np.roll(volt2, np.argmax(cor2)-(n-1))
    volt3_aligned = np.roll(volt3, np.argmax(cor3)-(n-1))
        
    if(show_plots):
        plt.figure(1)
        plt.plot(times, volt0, label="Antenna 0")
        plt.plot(times, volt1_aligned, label="Antenna 1")
        plt.plot(times, volt2_aligned, label="Antenna 2")
        plt.plot(times, volt3_aligned, label="Antenna 3")
        plt.legend()
        plt.title("Aligned Pulses")

    return volt1_aligned, volt2_aligned, volt3_aligned


def delay(theta, phi, times, volt0, volt1, volt2, volt3, A0, A1, A2, A3, show_plots=True):

    norm_vector = get_norm(theta, phi)

    delay1 = time_delay(asub(A1,A0),norm_vector) 
    delay2 = time_delay(asub(A2,A0),norm_vector)
    delay3 = time_delay(asub(A3,A0),norm_vector)
    
    dt = times[1]-times[0]
    
    idx_delay1 = np.rint(delay1/dt).astype(int)
    idx_delay2 = np.rint(delay2/dt).astype(int)
    idx_delay3 = np.rint(delay3/dt).astype(int)
    
    volt1_delayed = np.roll(volt1, idx_delay1)
    volt2_delayed = np.roll(volt2, idx_delay2)
    volt3_delayed = np.roll(volt3, idx_delay3)

    if(show_plots):
        plt.figure(2)
        plt.plot(times, volt0, label="Antenna 0")
        plt.plot(times, volt1_delayed, label="Antenna 1")
        plt.plot(times, volt2_delayed, label="Antenna 2")
        plt.plot(times, volt3_delayed, label="Antenna 3")
        plt.legend()
        plt.title("Delayed Pulses")
    
    return volt1_delayed, volt2_delayed, volt3_delayed 

def random_delays(theta, phi, times, volt0, volt1, volt2, volt3, A0, A1, A2, A3, show_plots=True):
    
    volt1_delayed, volt2_delayed, volt3_delayed = delay(theta, phi, times, volt0, volt1, volt2, volt3, A0, A1, A2, A3)

    # Add random, small time delays
    dt = times[1]-times[0]
    
    volt1_delayed = np.roll(volt1_delayed, np.random.randint(0, 100/dt))
    volt2_delayed = np.roll(volt2_delayed, np.random.randint(0, 100/dt))
    volt3_delayed = np.roll(volt3_delayed, np.random.randint(0, 100/dt))
    
    cor1 = np.asarray(signal.correlate(volt0,volt1_delayed))
    cor2 = np.asarray(signal.correlate(volt0,volt2_delayed))
    cor3 = np.asarray(signal.correlate(volt0,volt3_delayed))
    cor4 = np.asarray(signal.correlate(volt1_delayed,volt2_delayed))
    cor5 = np.asarray(signal.correlate(volt1_delayed,volt3_delayed))
    cor6 = np.asarray(signal.correlate(volt2_delayed,volt3_delayed))

    center = len(times)

    delay1 = (np.argmax(cor1)-(center-1))*dt
    delay2 = (np.argmax(cor2)-(center-1))*dt
    delay3 = (np.argmax(cor3)-(center-1))*dt
    delay4 = (np.argmax(cor4)-(center-1))*dt
    delay5 = (np.argmax(cor5)-(center-1))*dt
    delay6 = (np.argmax(cor6)-(center-1))*dt

    return delay1, delay2, delay3, delay4, delay5, delay6, volt1_delayed, volt2_delayed, volt3_delayed

def chi_square(antennas, A0, theta, phi, delay1, delay2, delay3, delay4, delay5, delay6):
    
    norm_vector = get_norm(theta, phi)
    
    A1 = Antenna(antennas[0], antennas[1], antennas[2])
    A2 = Antenna(antennas[3], antennas[4], antennas[5])
    A3 = Antenna(antennas[6], antennas[7], antennas[8])

    t1 = -time_delay(asub(A1,A0),norm_vector) 
    t2 = -time_delay(asub(A2,A0),norm_vector)
    t3 = -time_delay(asub(A3,A0),norm_vector)
    t4 = -time_delay(asub(A2,A1),norm_vector) 
    t5 = -time_delay(asub(A3,A1),norm_vector) 
    t6 = -time_delay(asub(A3,A2),norm_vector) 

    return (delay1-t1)**2 + (delay2-t2)**2 + (delay3-t3)**2 + (delay4-t4)**2 + (delay5-t5)**2 + (delay6-t6)**2

def minimizer(A0, A1, A2, A3, theta, phi, delay1, delay2, delay3, delay4, delay5, delay6):

    res = minimize(chi_square, x0 = np.array([[A1.x, A1.y, A1.z], [A2.x, A2.y, A2.z], [A3.x, A3.y, A3.z]]), args=(A0, theta, phi, delay1, delay2, delay3, delay4, delay5, delay6))
    print(res)
    
    new_A1 = Antenna(res.x[0], res.x[1], res.x[2])
    new_A2 = Antenna(res.x[3], res.x[4], res.x[5])
    new_A3 = Antenna(res.x[6], res.x[7], res.x[8])
    
    return new_A1, new_A2, new_A3

def main(theta, phi):

    #Set these variables before running:
    run_num = 1507
    ent_num = 18453
    pol = 0 #1 for Hpol, 0 for Vpol
    os.environ["BEACON_DATA_DIR"]="/data/beacon/data/"

    #Antenna Positions
    A0 = Antenna(0,0,0)
    A1 = Antenna(-33.49373061801294, -12.216161215847706, 15.23990049241125) #east, north, elevation
    A2 = Antenna(-8.660668526919165, -44.5336329143579, 5.489838290379097) 
    A3 = Antenna(-32.16822443711699, -43.200941168610264, 11.889772376808601)
    
    #t1,t2,t3,t4,t5,t6 = generate_time_arrays(A0,A1,A2,A3)
    
    volt0,volt1,volt2,volt3,times = setup(run_num,ent_num,pol)
 
    volt1_aligned,volt2_aligned,volt3_aligned = align(times,volt0,volt1,volt2,volt3)

    volt1_delayed,volt2_delayed,volt3_delayed = delay(theta,phi,times,volt0,volt1_aligned,volt2_aligned,volt3_aligned,A0,A1,A2,A3)

    correlator(times,volt0,volt1_delayed,volt2_delayed,volt3_delayed,A0,A1,A2,A3)
    
    #delay1, delay2, delay3, delay4, delay5, delay6, volt1_delayed, volt2_delayed, volt3_delayed = random_delays(theta, phi, times, volt0, volt1_aligned, volt2_aligned, volt3_aligned, A0, A1, A2, A3, show_plots=True)

    #new_A1, new_A2, new_A3 = minimizer(A0, A1, A2, A3, theta, phi, delay1, delay2, delay3, delay4, delay5, delay6)

    #correlator(times, volt0, volt1_delayed, volt2_delayed, volt3_delayed, A0, new_A1, new_A2, new_A3)

if __name__=="__main__":

    theta = float(sys.argv[1]) if len(sys.argv) > 1 else 90
    phi = float(sys.argv[2]) if len(sys.argv) > 2 else 0

    main(theta, phi)
