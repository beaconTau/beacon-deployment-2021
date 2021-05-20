# BEACON Deployment 2021

## People 

### Current Contributors:

Dan Southall - dsouthall@uchicago.edu
Andrew Zeolla - azeolla@psu.edu


# OVERVIEW

Scripts developed for the 2021 deployments of the BEACON experiment.  These scripts heavily leverage the [BEACON Analysis Package](https://github.com/djsouthall/beacon).  Instructions for installing that code are included below.

# Table of Contents

0.0.0 [Prep Work](#000-prep-work)

0.1.0 [Dependencies](#010-dependencies)

0.2.0 [Installing on Windows](#020-installing-on-windows)

0.3.0 [Installing on Ubuntu](#030-installing-on-ubuntu)

0.3.1 [Preparing Ubuntu](#031-preparing-ubuntu)

0.3.1 [Installing FFTW3](#031-installing-fftw3)

0.3.2 [Optional Git Setup](#032-optional-git-setup)

0.3.3 [Getting Setup to Code](#033-getting-setup-to-code)

0.3.4 [Optional iPython Setup](#034-optional-ipython-setup)

0.4.0 [Testing Setup](#040-testing-setup)

1.0.0 [Calibration](#100-calibration)

---

## 0.0.0 Prep Work

This sections describes how to get setup running the code.  Much of these instructions assume that you are *starting from scratch*, so feel free to skip steps if you are confident you know what you are doing.

* If you are starting on a Windows computer I recommend starting with [Section 0.2.0](https://github.com/beaconTau/beacon-deployment-2021/blob/main/README.md#020-installing-on-windows), which will tell you how to get Ubuntu runnin on a modern windows pc, before moving on to [Section 0.3.0](https://github.com/beaconTau/beacon-deployment-2021/blob/main/README.md#030-installing-on-ubuntu).
* If you are starting from a linux capable PC (linux, Mac, or Windows with WSL), then I recommend you start at [Section 0.3.0](https://github.com/beaconTau/beacon-deployment-2021/blob/main/README.md#030-installing-on-ubuntu).


## 0.1.0 Dependencies

The code was developed using compatible builds of Python 3.7.1 (or newer) and ROOT 6.22.02 (or newer).  It may work with older versions, but no guarentees are made.  Details are provided for getting started in general on Ubuntu in [Section 0.3.0](https://github.com/beaconTau/beacon-deployment-2021/blob/main/README.md#030-installing-on-ubuntu), as well as getting started on Windows via installing Ubuntu using the Windows Subsytem for Linux Version 2 (WSL2) in [Section 0.2.0](https://github.com/beaconTau/beacon-deployment-2021/blob/main/README.md#020-installing-on-windows).

This analysis framework is built using the BEACON event reader developed by [Cosmin Deaconu](https://github.com/cozzyd).  The [beaconroot](https://github.com/beaconTau/beaconroot) repository must be installed as described in that packages [README](https://github.com/beaconTau/beaconroot/blob/master/README.md).   This reader utilizes compiled C++/ROOT code to do the underlying event handling, and provides a simple python class which is what is directly referenced in this analysis code.  See [Section 0.3.3](https://github.com/beaconTau/beacon-deployment-2021/blob/main/README.md#033-getting-setup-to-code).

The majority of the scripts in this analysis package utilize the [FFTPrepper](https://github.com/djsouthall/beacon/blob/2d2233c13ca2d1d659f543ce8e78c44b760a49ba/tools/fftmath.py#L43) class, which acts as a wrapper class on the beaconroot Reader class - providing additional tools for streamlining the process of upsampling, and filtering (additionally there are some daughter classes defined to aid in cross correlations / time delay calculations as well as comparing events to a provided template event).  As part of the optional filtering available in these classes, the so-called Sine Subtraction method of CW removal is available for use when loading signals.  A FFTPrepper object can have these [SineSubtract](https://github.com/djsouthall/beacon/blob/master/tools/sine_subtract.py) objects added to it for use when loading signals.  These utilize code from [libRootFftwWrapper](https://github.com/nichol77/libRootFftwWrapper).  Instructions for installing libRootFftWrapper are included in multiple locations below, however you can also follow the instructions in the [README](https://github.com/nichol77/libRootFftwWrapper/blob/master/README.md) of that package.  Ensure to install with the correct version of python and ROOT.  See [Section 0.3.3](https://github.com/beaconTau/beacon-deployment-2021/blob/main/README.md#033-getting-setup-to-code).

Finally, there are required python packages that are required for most scripts in this analysis package.  In general you can see a list at [requirments](https://github.com/djsouthall/beacon/blob/master/requirements.txt).

## 0.2.0 Installing on Windows

This section actually gets you to the point where you can have installed and setup WSL2, and then can follow [Section 0.3.0](https://github.com/beaconTau/beacon-deployment-2021/blob/main/README.md#030-installing-on-ubuntu)

Getting setup with Windows Subsystem for Linux - Most of this section can be ignored if you are on a Mac or linux machine.

1. Follow this video to get Ubuntu setup in WSL2: https://www.youtube.com/watch?v=_fntjriRe48&ab_channel=DavidBombal 
    * You will want to update to a recent version of windows.  This will take a long time and should be done in advance
2. To get GUI interface for WSL2 install xming.
3. Allow xming through your firewall on both private and public networks.
4. Run xlaunch -> Multiple windows -> Display number 0 -> Next -> Start no client -> Next -> Clipboard enabled -> No Access Control enabled -> Next -> Finish
5. Run Ubuntu and perform any required initial setup if not already complete.
    * `cd ~`
    * `vim .bashrc`
    * `i` - This will let you edit the file in vim
    * Add a new line to the bashrc that says:
    * `export DISPLAY=$(grep -m 1 nameserver /etc/resolv.conf | awk '{print $2}'):0`
6. You can now test that the graphical elements are working by running something like xeyes
    * `sudo apt-get install x11-apps`
    * `xeyes` - A pair of eyes should pop up that track mouse movement.  You can close this with ctrl-c
7. You can see where your WSL files are stored by executing `explorer.exe .`, which will open Windows Explorer in the current directory.  You can then copy and past the path from above.  This is where you should direct any code editor, if you want to run windows programs to edit the code on your linux subsystem.

## 0.3.0 Installing on Ubuntu

This assumes you have a functional Ubuntu kernal.  Other linux systems can be used but you will need to convert some functions and syntax, the details of which are not outlined here.  If you need to get setup with Ubuntu on Windows see [Section 0.2.0](https://github.com/beaconTau/beacon-deployment-2021/blob/main/README.md#020-installing-on-windows)

## 0.3.1 Preparing Ubuntu

Before installing the code, you need to make sure you can install packages like make and cmake.  When errors occurred for me the following link helped: https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/ .  Ideally you can ignore that and just type the following:
    * `sudo apt update`
    * `sudo apt-get update`
    * `sudo apt install python3-pip`
    * `sudo apt-get install make`
    * `sudo apt-get install cmake`
    * If no errors occur then you should be good to go.

## 0.3.1 Installing FFTW3

Install FFTW3: `sudo apt-get install -y libfftw3-dev`

## 0.3.2 Optional Git Setup
Do this if you plan on using git commits and pushes.

1. Update git username: `git config --global user.name "Your Name"`
2. Update git email: `git config --global user.email "your@email"`
3. Optionally set vim as your editor: `git config --global core.editor "vim"`
4. If you have 2FA setup then pushing will take more then a simple password.  You will need to "Generate an Access Token" for your password from this specific pull.  I would google this.  You likely don't need strong access, I enable `repo`, and `write:discussion`.
5. If you don't want to enter these every time you wish to push you can setup a credential cache by following this guide: 
    * https://docs.github.com/en/github/getting-started-with-github/getting-started-with-git/caching-your-github-credentials-in-git 
    * You will still be prompted for the generated personal access token the first time you push, but it will cache this for the time window you give it.

## 0.3.3 Getting Setup to Code
1. Get the Conda installation file: `wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh`
2. Install Conda: `bash ./Anaconda3-2020.11-Linux-x86_64.sh`, Follow the prompts.
3. Create the root environment: `conda create -n my_root_env root -c conda-forge`
4. Activate the environment: `conda activate my_root_env` - You can consider adding this to bashrc if you think you will always want to be in this environment.
5. Create a BEACON directory:
    * `cd ~`
    * `mkdir beacon` - this can alternatively be done in any folder other than your home/~ folder.  I typically have a `projects` folder.  In which case I perform this after `cd ~/projects` .  You will need to account for this in step 12 and onward.
    * cd beacon
6. Clone the this repository: `git clone https://github.com/beaconTau/beacon-deployment-2021.git`
7. Clone the beacon analysis repository: `git clone https://github.com/djsouthall/beacon`
8. Clone the beaconroot repository: `git clone https://github.com/beaconTau/beaconroot`
9. Clone the libRootFftwWrapper repository: `git clone https://github.com/nichol77/libRootFftwWrapper`
10. Make a directory to store data: `mkdir data`
11. Type:
    * `cd $CONDA_PREFIX`
    * `mkdir -p ./etc/conda/activate.d`
    * `mkdir -p ./etc/conda/deactivate.d`
    * `touch ./etc/conda/activate.d/env_vars.sh`
    * `touch ./etc/conda/deactivate.d/env_vars.sh`
12. Now we must define environment variables (variables accessible by the linux kernal itself, as well as within the python shell.  Typically these will be defined in bashrc, but we are setting this all up in a conda environment, so we will define them such that they are only active when in that environment.   Type: `vim $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh` This will open a text editor called vim.
13. Starting from the top of the text editor write (replace "username" with your own):
    * `#!/bin/sh` <- Can add this at the top of the script if it does not already exist.  Not necessary likely.

            export BEACON_INSTALL_DIR=/home/username/beacon/beaconroot/
            export BEACON_ANALYSIS_DIR=/home/username/beacon/beacon/
            export BEACON_DATA=/home/username/beacon/data/
            export LIB_ROOT_FFTW_WRAPPER_DIR=/home/username/beacon/libRootFftwWrapper/
            export BEACON_ANALYSIS_DIR=/home/username/beacon/beacon/
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$BEACON_INSTALL_DIR/lib:$ANITA_INSTALL_DIR/lib
            export PYTHONPATH=$PYTHONPATH:/home/username/beacon/:/home/username/beacon/beaconroot/
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$BEACON_INSTALL_DIR/lib
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$LIB_ROOT_FFTW_WRAPPER_DIR
            export PYTHONPATH=$PYTHONPATH:/home/username/beacon/
14. Save and exit by typing esc followed by: `:x` , then enter
15. Reactivate the environment: `conda activate my_root_env`
16. Type:
    * `cd ~/beacon/libRootFftwWrapper`
    * `make`
    * `make install` - if there are troubles try `sudo make install`
    * `cd ~/beacon/beaconroot`
    * `make`
    * `make install` - if there are troubles try `sudo make install`
    * if there are problems during or after running make you may need to remove the build directory in that respect folder.  Ensure you are in the correct package directory and type `rm -rf build` before attempting make again.
17. Test if all of this worked by doing:
    * `cd ~/beacon`
    * `python beacon/analysis/sample_script_B.py`
18. The test will likely end in an error due to a missing dependency (such as pandas, matplotlib, etc.). For each error you get, install the missing dependency: `conda install -c conda-forge <missing package>`  .  A list of expected dependencies can be seen at https://github.com/djsouthall/beacon/blob/master/requirements.txt .  You can attempt to install all requirements using the command `conda install --file requirements.txt` while in the folder containing requirements.txt.  This will install what it can, of the remaining it is likely they are custom or default packages.  Likely you can ignore these unless an obvious problem occurs at some later time. 
19. Keep repeating steps 17 and 18 until you get an output that displays the number of events.
20. At this point you may start coming across errors related to not having data.  This is great!  Copy data to the data directory we made earlier and hopefully all is good moving forward. If you do not know where to access the data contact Dan Southall or someone else in the know.
21. To deactivate your environment type: `conda deactivate`

## 0.3.4 Optional iPython Setup
If it is not already installed I would recommend getting and using it.  It is a better command line interface (CLI) for python.
1. `sudo apt-get install ipython3`
2. `ipython`
3. `%run ~/beacon/beacon/analysis/sample_script_B.py` - This or any other script can be used to test running.  By using the %run shortcut in the CLI, you will stay in the namespace of the executed script, which lets you play around with plots, variables, and also helps in debugging.

## 0.4.0 Testing Setup

Attempt running both test analysis scripts from the [BEACON Analysis Package](https://github.com/djsouthall/beacon) to check if the code is functioning correctly:
* [beacon/analysis/sample_script_A.py](https://github.com/djsouthall/beacon/blob/master/analysis/sample_script_A.py) 
* [beacon/analysis/sample_script_B.py](https://github.com/djsouthall/beacon/blob/master/analysis/sample_script_B.py) 

## 1.0.0 Calibration

Once setup, include information on how to perform a calibration here.

