from numpy import linspace, sqrt, zeros
from scipy.io import loadmat
from matplotlib import rcParams
from bicycleid import data, plot, model # version debd089142e0d9e1bc2c448bbcfdab4060c08dc4

params = {'axes.labelsize': 10,
          'text.fontsize': 10,
          'legend.fontsize': 10,
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'text.usetex': True}
rcParams.update(params)

dat = data.ExperimentalData()

coefPlot = plot.CoefficientPlot()

subDef = {}
subDef['Rider'] = ['Charlie', 'Jason', 'Luke']
subDef['Environment'] = ['Treadmill', 'Pavilion']
subDef['Maneuver'] = ['Balance', 'Track Straight Line',
    'Balance With Disturbance', 'Track Straight Line With Disturbance']
subDef['Speed'] = ['1.4', '2.0', '3.0', '4.0', '4.92', '5.8', '7.0', '9.0']
subDef['MeanFit'] = 0.0
subDef['Duration'] = 0.0

subDat = dat.subset(**subDef)

speedRange = linspace(0.0, 10.0, num=50)
models = {rider: model.Whipple(rider).matrices(speedRange) for rider in ['Charlie']}

coefPlot.update_graph(subDat, models)

# now add the whipple model
m = loadmat('armsAB.mat', squeeze_me=True) # this is charlie at 11 speeds

stateMats = zeros((11, 4, 4))
for i, A in enumerate(m['stateMatrices']):
    stateMats[i] = A[[3, 6, 16, 18], :][:, [3, 6, 16, 18]]

inputMats = zeros((11, 4, 2))
for i, B in enumerate(m['inputMatrices']):
    inputMats[i] = B[[3, 6, 16, 18], 2:4]

for lab, ax in coefPlot.axes.items():
    row, col = int(lab[-2]), int(lab[-1])
    if lab[0] == 'a':
        ax.plot(m['speed'], stateMats[:, row - 1, col - 1], 'r')
    elif lab[0] == 'b':
        ax.plot(m['speed'], inputMats[:, row - 1, col - 1], 'r')

coefPlot.title.set_fontsize(10.0)
coefPlot.figure.set_figwidth(7.5)
goldenRatio = (sqrt(5)-1.0)/2.0
coefPlot.figure.set_figheight(7.5 * goldenRatio)
coefPlot.figure.savefig('figures/coefficients.pdf')
