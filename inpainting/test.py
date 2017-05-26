from masnou import *

occlusion = [(50,50),(50,70),(70,70),(70,50)]
level_lines = [40,70,85,100,115,130,160]

img_file = "img/lena_256.png"
original = misc.imread(img_file)

def test_paint_region():
	img = np.copy(original)
	intersection_points = 0

	cmp_occlusion = complete_points(occlusion)

	img_level,level_points = compute_level_lines(img,120)
	intersection_points+=len( intersect(cmp_occlusion,level_points) )

	img[np.invert(img_level)] = 255	
	paint_region(img,cmp_occlusion,60)	

	img[img_level] = 0	

	img_temp = np.copy(original)		
	img_level,level_points = compute_level_lines(img_temp,100)
	intersection_points+= len( intersect(cmp_occlusion,level_points) )

	img[img_level] = 0	
	print(intersection_points)

	plt.imshow(img,cmap="gray")
	plt.show()	


def test_four_neighborhood():
	for x in get_four_neighborhood(4,4,10,10):
		print(x)

	for x in get_four_neighborhood(9,9,10,10):
		print(x)		


def test_complete_points():
	region = [(1,1),(3,1),(3,3),(1,3)]
	print( complete_points(region) )

def test_intersect():
	region1 = [(1,1),(5,1),(5,5),(1,5)]
	region2 = [(3,3),(6,3),(6,6),(3,6)]

	cr1 = complete_points(region1)
	cr2 = complete_points(region2)

	print( intersect(cr1,cr2) )


def test_level_set_intersection():
	img_file = "img/lena_256.png"
	img = misc.imread(img_file)

	img_level,level_points = compute_level_lines(img,103)
	draw_level_line(img,img_level)
	# draw_upper_level_set(img,10)

	cmp_occlusion = complete_points(occlusion)
	paint_region(img,cmp_occlusion)

	ri = intersect(cmp_occlusion,level_points)
	paint_region(img,ri,190)

	plt.imshow(img,cmap="gray")
	plt.show()	

def mock_tjoints():
	cmp_occlusion = complete_points(occlusion)	
	rg = RegionGrid(Grid(100,100),cmp_occlusion)

	return rg

def plot_points(x,y):
	plt.clf()
	plt.plot(x,y,'ro')
	plt.show()	

def plot_scatter(x,y,colors):
	plt.clf()
	plt.scatter(x,y,c=colors)
	plt.show()		

def plot_tjoints():
	img_file = "img/lena_256.png"
	original = misc.imread(img_file)

	rg = mock_tjoints()

	x = [ e["pixels"][0][0] for e in rg.dict_grid.values()]
	y = [ e["pixels"][0][1] for e in rg.dict_grid.values()]	

	plot_points(x,y)	

def plot_region_grid():
	img_file = "img/lena_256.png"
	original = misc.imread(img_file)

	rg = mock_tjoints()
	
	x = [ e[0] for e in rg.dict_grid.keys()]
	y = [ e[1] for e in rg.dict_grid.keys()]

	plot_points(x,y)	

def plot_processed_tjoints():
	img_file = "img/lena_256.png"
	original = misc.imread(img_file)

	cmp_occlusion = complete_points(occlusion)	
	tjoints = compute_tjoints(original,level_lines,cmp_occlusion) 

	x = [ e[0] for e in tjoints.keys()]
	y = [ e[1] for e in tjoints.keys()]

	plot_points(x,y)

def plot_counterclock_tjoints():
	img_file = "img/lena_256.png"
	original = misc.imread(img_file)

	cmp_occlusion = complete_points(occlusion)	
	tjoints = compute_tjoints(original,level_lines,cmp_occlusion) 
	filled_tjoints = fill_in_intermediate_level_lines(tjoints)

	colors = np.linspace(0,1,len(filled_tjoints))

	x = [ tj["grid"][0] for tj in filled_tjoints ]
	y = [ tj["grid"][1] for tj in filled_tjoints ]

	plot_scatter(x,y,colors)


if __name__=='__main__':
	# test_paint_region()
	# test_intersect()
	# test_level_set_intersection()

	# plot_tjoints()
	# plot_region_grid()
	# plot_processed_tjoints()
	plot_counterclock_tjoints()