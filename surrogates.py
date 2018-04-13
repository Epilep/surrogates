import glob
import csv
import scipy.io
import random
import numpy as np
from scipy.signal import hilbert
#import matplotlib.pyplot as plt

def mod(vec):
    return np.sqrt(np.sum(vec*vec))

def iaaft(signal, niter, metodo='amplitude'):
    ftrans = np.fft.rfft(signal)
    famp = mod(ftrans)
    sig_famp = famp

    r = signal
    random.shuffle(r)
    for i in range(niter):
        ftrans = np.fft.rfft(r)
        famp = mod(ftrans)
        fase = ftrans / famp
        s = np.fft.irfft(fase * sig_famp)
        r = s[signal.argsort()]
        
    if metodo == 'amplitude':
        return r
    elif metodo == 'espectro':
        return s
    else :
        return (r,s)
        
def surrogates(pattern,nsur,nsteps):
    files = glob.glob(pattern) # Cria uma lista com todos os arquivos
    for f in files: # Laço sobre todos os arquivos
        clip = scipy.io.loadmat(f) # Abre cada arquivo
        freq = int(clip['freq'][0]) # Seleciona a frequência de amostragem
        chan = np.vstack(clip['channels'][0][0]) # Transforma os canais em um único array
        data = clip['data'] # Armazena os dados do arquivo
        nchan = len(chan)

    sur = []
    for ch in range(nchan):
        sur_chan = [list(data[ch])]
        for s in range(nsur):
            si = iaaft(data[ch],nsteps)
            sur_chan = sur_chan + [list(si)]
        sur =  sur + [sur_chan]

    return sur

pattern='Patient_1/*_ictal_*_1.mat'
n_sur = 10
n_iter = 1000
sur = surrogates(pattern,n_sur,n_iter)

with open("out.csv","w") as f:
    f.write('# channels = ' +  str(len(sur)-1) + ', surrogates = ' + str(len(sur[0])) + ', lenght = ' + str(len(sur[0][0])) + '\n')
    for i in range(len(sur)) :
        for j in range(len(sur[i])) :
            for k in range(len(sur[i][j])):
                f.write(str(sur[i][j][k]) + '\t')
            f.write('\n')
#        f.write('\n')
        
#plt.plot(sur[0][0])
#plt.plot(sur[0][1])
#plt.plot(sur[0][2])
#plt.plot(sur[0][3])
#plt.show()

