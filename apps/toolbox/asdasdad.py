import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from global_land_mask import globe
import cmocean
import datetime
import calendar

north_pacific_density = np.array([[4.945419847328244, 'April-2017'], [7.615839694656488, 'May-2017'], [13.135687022900763, 'June-2017'], [10.787977099236642, 'July-2017'], [13.222709923664123, 'August-2017'], [14.313358778625954, 'September-2017'], [7.614503816793893, 'October-2017'], [8.122709923664122, 'November-2017'], [7.124809160305343, 'December-2017'], [6.390648854961832, 'January-2018'], [5.945992366412214, 'February-2018'], [6.532824427480916, 'March-2018'], [7.298473282442748, 'April-2018'], [10.78587786259542, 'May-2018'], [10.345229007633588, 'June-2018'], [8.934923664122138, 'July-2018'], [6.7293893129771, 'August-2018'], [9.093702290076337, 'September-2018'], [10.03530534351145, 'October-2018'], [7.125, 'November-2018'], [4.633969465648855, 'December-2018'], [5.764503816793893, 'January-2019'], [5.105725190839695, 'February-2019'], [6.179770992366413, 'March-2019'], [8.309923664122138, 'April-2019'], [10.534351145038167, 'May-2019'], [9.434351145038168, 'June-2019'], [16.45, 'July-2019'], [16.572900763358778, 'August-2019'], [15.061641221374046, 'September-2019'], [15.440648854961832, 'October-2019'], [11.04618320610687, 'November-2019'], [8.310687022900764, 'December-2019'], [7.606870229007634, 'January-2020'], [6.651526717557252, 'February-2020'], [9.077671755725191, 'March-2020'], [12.04675572519084, 'April-2020'], [13.262977099236641, 'May-2020'], [13.924045801526718, 'June-2020'], [12.914885496183206, 'July-2020'], [16.921564885496185, 'August-2020'], [16.295419847328244, 'September-2020'], [13.445801526717558, 'October-2020'], [8.836641221374046, 'November-2020'], [7.36793893129771, 'December-2020'], [6.5232824427480915, 'January-2021'], [6.045229007633588, 'February-2021'], [7.572519083969466, 'March-2021'], [10.929580152671756, 'April-2021'], [10.892557251908396, 'May-2021']])
south_pacific_density = np.array([[5.225074882327771, 'April-2017'], [4.96348595064898, 'May-2017'], [6.707887605191841, 'June-2017'], [4.9580658964484385, 'July-2017'], [5.45685351590358, 'August-2017'], [6.42533162173727, 'September-2017'], [6.355726715161889, 'October-2017'], [6.771359292540294, 'November-2017'], [10.125089145628298, 'December-2017'], [9.831693053772643, 'January-2018'], [8.188988731992582, 'February-2018'], [7.376836399942947, 'March-2018'], [7.379831693053773, 'April-2018'], [7.287120239623449, 'May-2018'], [5.8744829553558695, 'June-2018'], [5.159463699900157, 'July-2018'], [3.7011838539438027, 'August-2018'], [4.916274425902154, 'September-2018'], [7.171159606332905, 'October-2018'], [6.841534731136785, 'November-2018'], [6.39823135073456, 'December-2018'], [6.874910854371701, 'January-2019'], [6.444301811439167, 'February-2019'], [7.38496648124376, 'March-2019'], [8.30808729139923, 'April-2019'], [7.043217800599058, 'May-2019'], [4.1112537441163886, 'June-2019'], [6.847240051347882, 'July-2019'], [7.775067750677507, 'August-2019'], [8.584795321637428, 'September-2019'], [10.087861931250892, 'October-2019'], [11.747682213664241, 'November-2019'], [11.670517757809158, 'December-2019'], [11.292968192839822, 'January-2020'], [9.039366709456568, 'February-2020'], [13.822849807445444, 'March-2020'], [11.921551847097419, 'April-2020'], [8.441306518328341, 'May-2020'], [7.493795464270432, 'June-2020'], [6.337184424475824, 'July-2020'], [6.497218656397091, 'August-2020'], [6.657538154328912, 'September-2020'], [7.552274996434175, 'October-2020'], [9.817144487234346, 'November-2020'], [9.955070603337612, 'December-2020'], [9.405790900014264, 'January-2021'], [10.318927399800314, 'February-2021'], [10.24504350306661, 'March-2021'], [11.362430466409927, 'April-2021'], [7.642989587790614, 'May-2021']])
mediterranian_density = np.array([[2.7907801418439715, 'April-2017'], [4.916666666666667, 'May-2017'], [6.069148936170213, 'June-2017'], [5.25354609929078, 'July-2017'], [6.530141843971631, 'August-2017'], [5.845744680851064, 'September-2017'], [4.212765957446808, 'October-2017'], [5.042553191489362, 'November-2017'], [3.6950354609929077, 'December-2017'], [3.726950354609929, 'January-2018'], [2.1595744680851063, 'February-2018'], [2.398936170212766, 'March-2018'], [3.1897163120567376, 'April-2018'], [3.8226950354609928, 'May-2018'], [3.4468085106382977, 'June-2018'], [3.5815602836879434, 'July-2018'], [2.143617021276596, 'August-2018'], [3.2109929078014185, 'September-2018'], [2.5372340425531914, 'October-2018'], [2.645390070921986, 'November-2018'], [1.7783687943262412, 'December-2018'], [1.0141843971631206, 'January-2019'], [1.4734042553191489, 'February-2019'], [2.00177304964539, 'March-2019'], [2.5726950354609928, 'April-2019'], [2.645390070921986, 'May-2019'], [3.423758865248227, 'June-2019'], [3.948581560283688, 'July-2019'], [5.053191489361702, 'August-2019'], [5.067375886524823, 'September-2019'], [4.725177304964539, 'October-2019'], [2.49290780141844, 'November-2019'], [2.3031914893617023, 'December-2019'], [2.515957446808511, 'January-2020'], [3.618794326241135, 'February-2020'], [2.4592198581560285, 'March-2020'], [3.8315602836879434, 'April-2020'], [3.4468085106382977, 'May-2020'], [3.9308510638297873, 'June-2020'], [4.148936170212766, 'July-2020'], [4.560283687943262, 'August-2020'], [3.74290780141844, 'September-2020'], [5.310283687943262, 'October-2020'], [3.856382978723404, 'November-2020'], [2.9609929078014185, 'December-2020'], [2.0797872340425534, 'January-2021'], [2.948581560283688, 'February-2021'], [3.349290780141844, 'March-2021'], [2.950354609929078, 'April-2021'], [5.707446808510638, 'May-2021']])
indian_density = np.array([[4.947531341897539, 'April-2017'], [5.2416034669555795, 'May-2017'], [4.937780529329825, 'June-2017'], [4.4620027859464475, 'July-2017'], [4.364494660269308, 'August-2017'], [6.903730072744157, 'September-2017'], [6.018263426714131, 'October-2017'], [7.622039931899087, 'November-2017'], [8.119176598049837, 'December-2017'], [6.630862095650828, 'January-2018'], [8.001857297631945, 'February-2018'], [7.336789970592788, 'March-2018'], [7.6451013774957435, 'April-2018'], [7.532580095960378, 'May-2018'], [4.766135273177527, 'June-2018'], [3.843213124903266, 'July-2018'], [2.361863488624052, 'August-2018'], [4.964247020585049, 'September-2018'], [7.020739823556725, 'October-2018'], [6.198885621420833, 'November-2018'], [7.000619099210648, 'December-2018'], [6.5912397461693235, 'January-2019'], [7.445906206469587, 'February-2019'], [7.666769849868442, 'March-2019'], [8.812412939173502, 'April-2019'], [6.831295465098282, 'May-2019'], [3.94397152143631, 'June-2019'], [5.205076613527318, 'July-2019'], [5.390342052313883, 'August-2019'], [8.032347933756384, 'September-2019'], [10.48042098746324, 'October-2019'], [9.701129856059433, 'November-2019'], [10.247949233864727, 'December-2019'], [10.578238662745704, 'January-2020'], [9.314192849404117, 'February-2020'], [13.21467265129237, 'March-2020'], [12.081256771397616, 'April-2020'], [7.995511530722799, 'May-2020'], [6.8184491564773255, 'June-2020'], [6.08079244698963, 'July-2020'], [6.742609503172884, 'August-2020'], [7.8894907908992415, 'September-2020'], [9.402104937316205, 'October-2020'], [9.267296084197493, 'November-2020'], [8.140225971211887, 'December-2020'], [7.686581024609193, 'January-2021'], [8.744312026002167, 'February-2021'], [11.254449775576536, 'March-2021'], [11.06779136356601, 'April-2021'], [8.026311716452561, 'May-2021']])
north_atlantic_density = np.array([[4.593092105263158, 'April-2017'], [6.447368421052632, 'May-2017'], [9.633881578947369, 'June-2017'], [7.199671052631579, 'July-2017'], [8.948684210526316, 'August-2017'], [10.025, 'September-2017'], [7.123684210526315, 'October-2017'], [7.573684210526316, 'November-2017'], [5.908223684210526, 'December-2017'], [4.484539473684211, 'January-2018'], [4.540131578947369, 'February-2018'], [4.545723684210526, 'March-2018'], [4.7953947368421055, 'April-2018'], [6.875328947368421, 'May-2018'], [8.072697368421053, 'June-2018'], [6.162171052631579, 'July-2018'], [6.112828947368421, 'August-2018'], [6.569078947368421, 'September-2018'], [7.10625, 'October-2018'], [4.640460526315789, 'November-2018'], [5.559868421052632, 'December-2018'], [5.9625, 'January-2019'], [4.552302631578947, 'February-2019'], [5.0855263157894735, 'March-2019'], [7.096052631578948, 'April-2019'], [7.7894736842105265, 'May-2019'], [6.7319078947368425, 'June-2019'], [10.675, 'July-2019'], [11.382894736842106, 'August-2019'], [12.305592105263157, 'September-2019'], [11.74046052631579, 'October-2019'], [8.497039473684211, 'November-2019'], [6.1480263157894735, 'December-2019'], [8.183223684210526, 'January-2020'], [7.807565789473684, 'February-2020'], [8.141776315789473, 'March-2020'], [8.165460526315789, 'April-2020'], [8.786184210526315, 'May-2020'], [10.144407894736842, 'June-2020'], [10.113157894736842, 'July-2020'], [11.630263157894737, 'August-2020'], [9.540131578947369, 'September-2020'], [11.021381578947368, 'October-2020'], [5.575986842105263, 'November-2020'], [6.943421052631579, 'December-2020'], [6.04046052631579, 'January-2021'], [5.265789473684211, 'February-2021'], [7.01875, 'March-2021'], [9.055263157894737, 'April-2021'], [8.654276315789474, 'May-2021']])
south_atlantic_density = np.array([[4.2163925127623365, 'April-2017'], [4.150311968235961, 'May-2017'], [4.843165059557572, 'June-2017'], [4.6029495178672715, 'July-2017'], [5.19058423142371, 'August-2017'], [4.612308564946114, 'September-2017'], [3.2830402722631877, 'October-2017'], [4.3235961429381735, 'November-2017'], [6.054169030062393, 'December-2017'], [7.195121951219512, 'January-2018'], [7.021270561542825, 'February-2018'], [7.214123652864435, 'March-2018'], [6.62251843448667, 'April-2018'], [4.738513896766874, 'May-2018'], [4.324730572887124, 'June-2018'], [4.754963131026659, 'July-2018'], [2.6764038570618265, 'August-2018'], [2.909812819058423, 'September-2018'], [4.471922858763471, 'October-2018'], [3.824730572887124, 'November-2018'], [5.818774815655133, 'December-2018'], [7.256381168462847, 'January-2019'], [6.83494044242768, 'February-2019'], [6.08252977878616, 'March-2019'], [6.290697674418604, 'April-2019'], [5.7007941009642655, 'May-2019'], [3.9075439591605217, 'June-2019'], [5.171298922291548, 'July-2019'], [5.787294384571752, 'August-2019'], [5.398184912081679, 'September-2019'], [6.929381735677822, 'October-2019'], [6.7714123652864435, 'November-2019'], [7.4889393079977316, 'December-2019'], [10.096426545660805, 'January-2020'], [7.396483267158253, 'February-2020'], [10.168462847419171, 'March-2020'], [7.567782189449802, 'April-2020'], [5.990924560408395, 'May-2020'], [5.290130459444129, 'June-2020'], [5.043108338060125, 'July-2020'], [4.46596710153148, 'August-2020'], [5.863017583664209, 'September-2020'], [5.289279636982417, 'October-2020'], [5.9463981849120815, 'November-2020'], [6.597277368122518, 'December-2020'], [6.662790697674419, 'January-2021'], [7.058423142370959, 'February-2021'], [7.689733408961996, 'March-2021'], [7.354792966534316, 'April-2021'], [5.609472490073738, 'May-2021']])
global_density = np.array([[4.575763888888889, 'April-2017'], [5.322256944444445, 'May-2017'], [7.223888888888889, 'June-2017'], [5.956666666666667, 'July-2017'], [6.843680555555555, 'August-2017'], [7.9122916666666665, 'September-2017'], [5.777986111111111, 'October-2017'], [6.5934375, 'November-2017'], [7.374479166666666, 'December-2017'], [6.761840277777778, 'January-2018'], [6.538298611111111, 'February-2018'], [6.353472222222222, 'March-2018'], [6.613854166666667, 'April-2018'], [7.183854166666666, 'May-2018'], [6.193611111111111, 'June-2018'], [5.458298611111111, 'July-2018'], [3.8829166666666666, 'August-2018'], [5.392569444444445, 'September-2018'], [6.779375, 'October-2018'], [5.651076388888889, 'November-2018'], [5.581388888888889, 'December-2018'], [6.017986111111111, 'January-2019'], [5.80875, 'February-2019'], [6.2440625, 'March-2019'], [7.484340277777778, 'April-2019'], [7.07625, 'May-2019'], [5.1717361111111115, 'June-2019'], [8.144444444444444, 'July-2019'], [8.639513888888889, 'August-2019'], [9.131736111111111, 'September-2019'], [10.20079861111111, 'October-2019'], [9.307465277777778, 'November-2019'], [8.713229166666666, 'December-2019'], [9.125208333333333, 'January-2020'], [7.656493055555556, 'February-2020'], [10.596284722222222, 'March-2020'], [10.189131944444444, 'April-2020'], [8.463090277777777, 'May-2020'], [8.072256944444444, 'June-2020'], [7.471041666666666, 'July-2020'], [8.561145833333333, 'August-2020'], [8.621631944444445, 'September-2020'], [8.724652777777777, 'October-2020'], [7.806493055555555, 'November-2020'], [7.544791666666667, 'December-2020'], [7.029722222222222, 'January-2021'], [7.464479166666667, 'February-2021'], [8.5425, 'March-2021'], [9.633506944444445, 'April-2021'], [7.733923611111111, 'May-2021']])

y = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []
y7 = []

labels  = []
for measure in north_pacific_density:
    y.append(float(measure[0]))
    labels.append(measure[1])

for measure in south_pacific_density:
    y2.append(float(measure[0]))

for measure in mediterranian_density:
    y3.append(float(measure[0]))

for measure in indian_density:
    y4.append(float(measure[0]))

for measure in north_atlantic_density:
    y5.append(float(measure[0]))

for measure in south_atlantic_density:
    y6.append(float(measure[0]))

for measure in global_density:
    y7.append(float(measure[0]))

x = np.arange(len(y))

plt.xlabel("Month and Year")
plt.ylabel("Average Peak Density")

fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111)
plt.title("Average peak density per bin")
plt.xticks(x, labels, rotation=45)
plt.xlabel("Month and Year")
plt.ylabel("Peak Density")

#plt.plot(x, y, label="North Pacific")
#plt.plot(x, y2, label="South Pacific")
#plt.plot(x, y3, label="Mediterranian")
#plt.plot(x, y4, label="Indian")
#plt.plot(x, y5, label="North Atlantic")
#plt.plot(x, y6, label="South Atlantic")
plt.plot(x, y7, label="Global")


plt.legend()
plt.tight_layout()
plt.savefig('only_NA_density.png', dpi=300, bbox_inches='tight')

plt.show()



