import unittest

import numpy as np

import packages.denoise.fista

class Fista(unittest.TestCase):
	def setUp(self):
		self.m,self.M = 6,1000
		self.n,self.N = 6,1000

		#Lightweight
		self.p_rand_int32_matrix_light = np.random.randint( -100,100, (2,self.m,self.n),np.int32)		
		self.p_rand_uint32_matrix_light = np.random.randint( 0,100, (2,self.m,self.n),np.uint32)		
		self.p_rand_float32_matrix_light = np.random.ranf( (2,self.m,self.n) )

		#Heavyweight
		self.p_rand_int32_matrix_heavy = np.random.randint( -100,100, (2,self.M,self.N),np.int32)		
		self.p_rand_uint32_matrix_heavy = np.random.randint( 0,100, (2,self.M,self.N),np.uint32)		
		self.p_rand_float32_matrix_heavy = np.random.ranf( (2,self.N,self.N) )

		self.p_static_float32_matrix = np.array( [ [ [0.8,0.7],[0.1,0.2] ], [ [0.7,0.3],[0.999,0.5]  ] ],np.float32 )

	def test_project_on_p_output_type(self):
		out_int32 = packages.denoise.fista.project_on_P(self.p_rand_int32_matrix_light)
		self.assertEqual(np.float64,out_int32.dtype)

		out_uint32 = packages.denoise.fista.project_on_P(self.p_rand_uint32_matrix_light)
		self.assertEqual(np.float64,out_uint32.dtype)

		out_float32 = packages.denoise.fista.project_on_P(self.p_rand_float32_matrix_light)
		self.assertEqual(np.float64,out_float32.dtype)		

	def test_project_on_p_correctness(self):

		out_static_float32 = packages.denoise.fista.project_on_P(self.p_static_float32_matrix)
		p11 = 0.8/np.sqrt( 0.8**2 + 0.7**2 )
		p12 = 0.7 
		p21 = 0.1/np.sqrt( 0.1**2 + 0.999*2)
		p22 = 0.2

		q11 = 0.7/np.sqrt( 0.8**2 + 0.7**2 )
		q12 = 0.3
		q21 = 0.999/np.sqrt( 0.1**2 + 0.999*2)
		q22 = 0.5

		self.assertFalse( (out_static_float32 - np.array( [ [ [p11,p12],[p21,p22] ],[ [q11,q12], [q21,q22] ] ] ,np.float64)).all() )


if __name__=='__main__':
	unittest.main()



