from py3dbp import Packer, Bin, Item, Painter
import time
import pandas as pd
start = time.time()

'''

Check stability on item - second' rule
1. If the ratio below the support surface does not exceed this ratio, then check the second rule.
2. If there is no support under any of the bottom four vertices of the item, then remove the item.

'''
df= pd.read_csv('cuboid_dimensions.csv')
# init packing function
packer = Packer()
#  init bin 
box = Bin('example6', (240, 240, 200), 3000,0,0)
#  add item
# Item('item partno', (W,H,D), Weight, Packing Priority level, load bear, Upside down or not , 'item color')
packer.addBin(box)
for idx, row in df.iterrows():
    packer.addItem(Item(
        partno=idx+1,
        name='test',
        typeof='cube',
        WHD=(row['L'], row['B'], row['H']),  # Tuple for dimensions
        weight=40,
        level=1,
        loadbear=3500,
        updown=True,
        color='Yellow'
    ))
# packer.addItem(Item(partno='Box-1', name='test', typeof='cube', WHD=(5, 4, 1), weight=1, level=1,loadbear=100, updown=True, color='yellow'))
# packer.addItem(Item(partno='Box-2', name='test', typeof='cube', WHD=(1, 1, 4), weight=1, level=2,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-3', name='test', typeof='cube', WHD=(3, 4, 2), weight=1, level=3,loadbear=100, updown=True, color='pink'))
# packer.addItem(Item(partno='Box-4', name='test', typeof='cube', WHD=(1, 1, 4), weight=1, level=4,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-5', name='test', typeof='cube', WHD=(1, 2, 1), weight=1, level=5,loadbear=100, updown=True, color='pink'))
# packer.addItem(Item(partno='Box-6', name='test', typeof='cube', WHD=(1, 2, 1), weight=1, level=6,loadbear=100, updown=True, color='pink'))
# packer.addItem(Item(partno='Box-7', name='test', typeof='cube', WHD=(1, 1, 4), weight=1, level=7,loadbear=100, updown=True, color='olive'))
# packer.addItem(Item(partno='Box-8', name='test', typeof='cube', WHD=(1, 1, 4), weight=1, level=8,loadbear=100, updown=True, color='olive'))# Try switching WHD=(1, 1, 3) and (1, 1, 4) to compare the results
# packer.addItem(Item(partno='Box-9', name='test', typeof='cube', WHD=(5, 4, 2), weight=1, level=9,loadbear=100, updown=True, color='brown'))
# packages = [
#     (60, 50, 4000, 85),
#     (70, 50, 60000, 90),
#     (30, 20345, 20, 30),
#     (180, 40, 33450, 70),
#     (83450, 60, 40, 100),
#     (20, 20, 10, 20),
#     (10, 70, 50, 130),
#     (40, 30, 20, 40),
#     (60, 50, 30, 60),
#     (10, 10, 10, 10),
#     (50, 30, 40, 70),
#     (70, 60, 50, 110),
#     (40, 170, 30, 50),
#     (80, 70, 60, 30),
#     (30, 20, 100, 30),
#     (50, 50, 40, 80),
#     (90, 40, 60, 20),
#     (20, 20, 30, 40),
#     (40, 30, 30, 50),
#     (60, 40, 30, 70),
#     (70, 60, 40, 100),
#     (20, 10, 10, 20),
#     (40, 30, 40, 80),
#     (200, 180, 230, 40),
# ]

# for i, (length, width, height, weight) in enumerate(packages, 1):
#     packer.addItem(
#         Item(
#             partno=f'Box-{i}',
#             name='test',
#             typeof='cube',
#             WHD=(width, length, height),
#             weight=weight,
#             level=1,
#             loadbear=6000,
#             updown=True,
#             color='yellow'
#         )
#     )

# calculate packing 
packer.pack(
    bigger_first=True,
    distribute_items=False,
    fix_point=True,
    check_stable=True,
    support_surface_ratio=0.75,
    number_of_decimals=0
)

# put order
packer.putOrder()

# print result
b = packer.bins[0]
volume = b.width * b.height * b.depth
print(":::::::::::", b.string())
total_volume=0
print("FITTED ITEMS:")
volume_t = 0
volume_f = 0
unfitted_name = ''
for item in b.items:
    print("partno : ",item.partno)
    print("color : ",item.color)
    print("position : ",item.position)
    print("rotation type : ",item.rotation_type)
    print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
    print("volume : ",float(item.width) * float(item.height) * float(item.depth))
    # print("weight : ",float(item.weight))
    volume_t += float(item.width) * float(item.height) * float(item.depth)
    total_volume+=(float(item.width) * float(item.height) * float(item.depth))
    print("***************************************************")
print("***************************************************")
# print("UNFITTED ITEMS:")
# for item in b.unfitted_items:
#     print("partno : ",item.partno)
#     print("color : ",item.color)
#     print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
#     print("volume : ",float(item.width) * float(item.height) * float(item.depth))
#     print("weight : ",float(item.weight))
#     volume_f += float(item.width) * float(item.height) * float(item.dept40
#     unfitted_name += '{},'.format(item.partno)
#     print("***************************************************")
# print("***************************************************")
# print('space utilization : {}%'.format(round(volume_t / float(volume) * 100 ,2)))
# print('residual volumn : ', float(volume) - volume_t )
# print('unpack item : ',unfitted_name)
# print('unpack item volumn : ',volume_f)
# print("gravity distribution : ",b.gravity)
stop = time.time()
print('used time : ',stop - start)
print (total_volume)
print ("Bhot share chut ka land ",len(b.items))
# draw results
painter = Painter(b)
fig = painter.plotBoxAndItems(
    title=b.partno,
    alpha=0.8,
    write_num=False,
    fontsize=10
)
fig.show()