import numpy
import scipy.stats as stats

class RandomGenerator(object):
	def __init__(self):
		pass
	def __init__(self,seed,N):
		numpy.random.seed(seed)
		self.N = N
	
	def GetRandomValues(self,id,args):
		if id == "constant":
			return [args[0]]*self.N
		if id == "uniform":#uniform distribution
			return numpy.random.uniform(low=args[0],high=args[1],size=self.N)
		if id == "triangular":#triangular distribution
			return numpy.random.triangular(left=args[0],mode=args[1],right=args[2],size=self.N)
		if id == "normal":#normal distribution
			return numpy.random.normal(loc=args[0],scale=args[1],size=self.N)
		if id == "lognormal":#log normal distribution
			return numpy.random.lognormal(mean=args[0],sigma=args[1],size=self.N)
	def CalculateSpearman(self,a,b):
		rho,pval = stats.spearmanr(a,b,axis=None)
		return [rho,pval]
	def CalculatePearson(self,a,b):
		rho = stats.pearsonr(a,b)
		return rho
	
class RandomGeneratorDics(object):
	def __init__(self):
		pass
	def __init__(self,seed,N):
		self.seed = seed
		numpy.random.seed(self.seed)
		self.N = N
	
	def GetRandomValues(self,args):
		id = args['Distribution']
		if id == "constant":
			return [args['Constant']]*self.N
		elif id == "uniform":#uniform distribution
			return numpy.random.uniform(low=args['Min'],high=args['Max'],size=self.N)
		elif id == "triangular":#triangular distribution
			return numpy.random.triangular(left=args['Min'],mode=args['Mean'],right=args['Max'],size=self.N)
		elif id == "normal":#normal distribution
			return numpy.random.normal(loc=args['Mean'],scale=args['StdDev'],size=self.N)
		elif id == "lognormal":#log normal distribution
			return numpy.random.lognormal(mean=args['Mean'],sigma=args['Sigma'],size=self.N)
		elif id == "truncated_normal":
			a = args['Min']
			b = args['Max']
			my = args['Mean']
			sig = args['StdDev']
			#print a, " ",b," ",my," ",sig
			normal = stats.norm(my,sig)
			u = numpy.random.uniform(low=0.0,high=1.0,size=self.N)
			x = normal.ppf(normal.cdf(a)+u*(normal.cdf(b)-normal.cdf(a)))
			return x
	
	def GetNRandomValues(self,args,N):
		id = args['Distribution']
		if id == "constant":
			return args['const']*N
		elif id == "uniform":#uniform distribution
			return numpy.random.uniform(low=args['Min'],high=args['Max'],size=N)
		elif id == "triangular":#triangular distribution
			return numpy.random.triangular(left=args['Min'],mode=args['Mean'],right=args['Max'],size=N)
		elif id == "normal":#normal distribution
			return numpy.random.normal(loc=args['Mean'],scale=args['StdDev'],size=N)
		elif id == "lognormal":#log normal distribution
			return numpy.random.lognormal(mean=args['Mean'],sigma=args['Sigma'],size=N)
		elif id == "truncated_normal":
			a = args['Min']
			b = args['Max']
			my = args['Mean']
			sig = args['StdDev']
			print a, " ",b," ",my," ",sig
			normal = stats.norm(my,sig)
			u = numpy.random.uniform(low=0.0,high=1.0,size=N)
			x = normal.ppf(normal.cdf(a)+u*(normal.cdf(b)-stats.normal.cdf(a)))
			return x
			#return stats.truncnorm.rvs(args['Min'],args['Max'],loc=args['Mean'],scale=args['StdDev'],size=N)
		
	def CalculateSpearman(self,a,b):
		rho,pval = stats.spearmanr(a,b,axis=None)
		return [rho,pval]
	def CalculatePearson(self,a,b):
		rho= stats.pearsonr(a,b)
		return rho
	def GetRandomInteger(self,low,high,N):
		return numpy.random.randint(low,high,N)