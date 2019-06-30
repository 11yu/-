import pygal
with open("university.txt") as Kobe:
	lines=Kobe.readlines()
	
aset=set(lines)
print(aset)
frequencies=[]
for value in aset:
	frequency=lines.count(value)
	frequencies.append(frequency)
hist=pygal.Bar()
hist.title="Statistics of KFC in Beijing"
hist.x_labels=aset
hist.x_title="Types of District"
hist.y_titlt="Frequency of KFC"
hist.add('KFC',frequencies)
hist.render_to_file('KFC.svg')
