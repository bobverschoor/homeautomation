from sensor.p1_device import P1Device

p1 = P1Device()
data = p1.get_data()

print(data)