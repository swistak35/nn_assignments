export PATH=/home/swistak35/apps/anaconda2/bin:$PATH

# The directory where the script is
export NN="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ \( "`which ipython`" != /pio/os/anaconda/bin/ipython \) -a \( -e /pio/os/anaconda/set-env.sh \) ]
then
    echo "Adding Anaconda Python from /pio/os to your environment"
    source /pio/os/anaconda/set-env.sh
fi

export FUEL_DATA_PATH=$NN/datasets/

export BLOCKS_CONFIG=$NN/config/blocks.yaml
export THEANORC=$NN/config/theano.rc:$HOME/.theanorc

#python modules
export PYTHONPATH=$NN:$NN/libs/Theano:$NN/libs/fuel:$NN/libs/picklable-itertools:$PYTHONPATH
export PATH=$NN/libs/fuel/bin:$PATH
