from ParameterEstimater import CalculateTruncatedNormalPorosityParameters
#BSCProject Configuration File for MonteCarlo Method
Dump = True
Model_Name = "BSCProject_LM_FS"
N = 100000
Seed = 66323

#Property_Descriptors = {'Property 1':{'Name':"Porosity",'Distribution':"Normal"},'Property 2':{'Name':"Sw",'Distribution':"Triangular"},'Property 3':{'Name':"Area",'Distribution':"Constant"}}
#not enough data for packstone, coarse sand, fine sand and medium sand => std.dev 0.05, marl=largest uncertainty => std.dev 0.1
trunc_norm = {'grainstone':{'a':0.0009,'b':0.4817,'loc':0.1017,'scale':0.0118},'wackstone':{'a':0.0009,'b':0.4812,'loc':0.0929,'scale':0.0108},'mudstone':{'a':0.0013,'b':0.4797,'loc':0.0598,'scale':0.0062},'packstone':{'a':0.0,'b':0.475,'loc':0.0394,'scale':0.05},'coarse':{'a':0.0,'b':0.475,'loc':0.2324,'scale':0.05},'fine':{'a':0.0,'b':0.475,'loc':0.213,'scale':0.05},'medium':{'a':0.0,'b':0.475,'loc':0.2284,'scale':0.05},'marl':{'a':0.0,'b':0.475,'loc':0.3,'scale':0.1}}
#Rocktype Definitions

#Rocktype Grainstones SCAL Data 4, SWi Data RRT 8b
#RockType1_Porosity = {'Name':"Porosity",'Distribution':"truncated_normal",'Min':trunc_norm['grainstone']['a'],'Max':trunc_norm['grainstone']['b'],'Mean':trunc_norm['grainstone']['loc'],'StdDev':trunc_norm['grainstone']['scale']}
RockType1_Porosity = {'Name':"Porosity",'Distribution':"truncated_normal",'Min':0.0003,'Max':0.5,'Mean':0.25,'StdDev':0.001}
RockType1_Sw = {'Name':"Sw",'Distribution':"triangular",'Min':0.07,'Max':0.14,'Mean':0.0976}
Grainstones = {'Porosity':RockType1_Porosity,'Sw':RockType1_Sw}

#Rocktype Mudstones SCAL Data 1, SWi Data RRT 6
RockType2_Porosity = {'Name':"Porosity",'Distribution':"truncated_normal",'Min':trunc_norm['mudstone']['a'],'Max':trunc_norm['mudstone']['b'],'Mean':trunc_norm['mudstone']['loc'],'StdDev':trunc_norm['mudstone']['scale']}
RockType2_Sw = {'Name':"Sw",'Distribution':"triangular",'Min':0.06,'Max':0.13,'Mean':0.098}
Mudstones = {'Porosity':RockType2_Porosity,'Sw':RockType2_Sw}

#Rocktype Packstone SCAL Data 3, SWi Data RRT 11
RockType3_Porosity = {'Name':"Porosity",'Distribution':"truncated_normal",'Min':trunc_norm['packstone']['a'],'Max':trunc_norm['packstone']['b'],'Mean':trunc_norm['packstone']['loc'],'StdDev':trunc_norm['packstone']['scale']}
RockType3_Sw = {'Name':"Sw",'Distribution':"triangular",'Min':0.06,'Max':0.117,'Mean':0.0794}
Packstones = {'Porosity':RockType3_Porosity,'Sw':RockType3_Sw}

#Rocktype Wackstone SCAL Data 2, SWi Data RRT 15
RockType4_Porosity = {'Name':"Porosity",'Distribution':"truncated_normal",'Min':trunc_norm['wackstone']['a'],'Max':trunc_norm['wackstone']['b'],'Mean':trunc_norm['wackstone']['loc'],'StdDev':trunc_norm['wackstone']['scale']}
RockType4_Sw = {'Name':"Sw",'Distribution':"triangular",'Min':0.08,'Max':0.11,'Mean':0.086}
Wackstones = {'Porosity':RockType4_Porosity,'Sw':RockType4_Sw}

#Rocktype Marls Rocktype 11
RockType5_Porosity = {'Name':"Porosity",'Distribution':"truncated_normal",'Min':trunc_norm['marl']['a'],'Max':trunc_norm['marl']['b'],'Mean':trunc_norm['marl']['loc'],'StdDev':trunc_norm['marl']['scale']}
RockType5_Sw = {'Name':"Sw",'Distribution':"triangular",'Min':0.052,'Max':0.25,'Mean':0.13}
Marls = {'Porosity':RockType5_Porosity,'Sw':RockType5_Sw}

#Rocktype CoarseSandstones Rocktype 8
RockType6_Porosity = {'Name':"Porosity",'Distribution':"truncated_normal",'Min':trunc_norm['coarse']['a'],'Max':trunc_norm['coarse']['b'],'Mean':trunc_norm['coarse']['loc'],'StdDev':trunc_norm['coarse']['scale']}
RockType6_Sw = {'Name':"Sw",'Distribution':"triangular",'Min':0.1,'Max':0.3,'Mean':0.15}
CoarseSandstones = {'Porosity':RockType6_Porosity,'Sw':RockType6_Sw}

#Rocktype MediumSandstones Rocktype 9
RockType7_Porosity = {'Name':"Porosity",'Distribution':"truncated_normal",'Min':trunc_norm['medium']['a'],'Max':trunc_norm['medium']['b'],'Mean':trunc_norm['medium']['loc'],'StdDev':trunc_norm['medium']['scale']}
RockType7_Sw = {'Name':"Sw",'Distribution':"triangular",'Min':0.12,'Max':0.28,'Mean':0.2}
MediumSandstones = {'Porosity':RockType7_Porosity,'Sw':RockType7_Sw}

#Rocktype FineSandstones Rocktype 10
RockType8_Porosity = {'Name':"Porosity",'Distribution':"truncated_normal",'Min':trunc_norm['fine']['a'],'Max':trunc_norm['fine']['b'],'Mean':trunc_norm['fine']['loc'],'StdDev':trunc_norm['fine']['scale']}
RockType8_Sw = {'Name':"Sw",'Distribution':"triangular",'Min':0.14,'Max':0.25,'Mean':0.19}
FineSandstones = {'Porosity':RockType8_Porosity,'Sw':RockType8_Sw}


#Region Definitions
#Grainstones
Grainstone_1 = {'Name':"Grainstone_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':599.4}},'RockType':"Class 1"}
Grainstone_2 = {'Name':"Grainstone_2",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':1345.73}},'RockType':"Class 1"}
Grainstone_3 = {'Name':"Grainstone_3",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':586.82}},'RockType':"Class 1"}
Grainstone_4 = {'Name':"Grainstone_4",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':600.95}},'RockType':"Class 1"}
Grainstone_5 = {'Name':"Grainstone_5",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':508.54}},'RockType':"Class 1"}
Grainstone_6 = {'Name':"Grainstone_6",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':751.14}},'RockType':"Class 1"}
Grainstone_7 = {'Name':"Grainstone_7",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':515.45}},'RockType':"Class 1"}
Grainstone_8 = {'Name':"Grainstone_8",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':367.6}},'RockType':"Class 1"}
Grainstone_9 = {'Name':"Grainstone_9",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':166.29}},'RockType':"Class 1"}

#Mudstones
Mudstone_1 = {'Name':"Mudstone_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':539.08}},'RockType':"Class 2"}
Mudstone_2 = {'Name':"Mudstone_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':254.07}},'RockType':"Class 2"}
Mudstone_3 = {'Name':"Mudstone_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':138.47}},'RockType':"Class 2"}
Mudstone_4 = {'Name':"Mudstone_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':113.335}},'RockType':"Class 2"}
Mudstone_5 = {'Name':"Mudstone_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':135.045}},'RockType':"Class 2"}

#Packstones
Packstone_1 = {'Name':"Packstone_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':391.67}},'RockType':"Class 3"}

#Wackstones
Wackstone_1 = {'Name':"Wackstone_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':156.06}},'RockType':"Class 4"}

#Marls
Marl_1 = {'Name':"Marl_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':2773.29}},'RockType':"Class 5"}
Marl_2 = {'Name':"Marl_2",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':3043.19}},'RockType':"Class 5"}
Marl_3 = {'Name':"Marl_3",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':3126.25}},'RockType':"Class 5"}
Marl_4 = {'Name':"Marl_4",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':3841.57}},'RockType':"Class 5"}
Marl_5 = {'Name':"Marl_5",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':627.07}},'RockType':"Class 5"}
Marl_6 = {'Name':"Marl_6",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':503.72}},'RockType':"Class 5"}
Marl_7 = {'Name':"Marl_7",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':1639.89}},'RockType':"Class 5"}
Marl_8 = {'Name':"Marl_8",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':47.37}},'RockType':"Class 5"}

#Coarse Sandstones
CoarseSandstone_1 = {'Name':"CoarseSandstone_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':203.18}},'RockType':"Class 6"}

#Medium Sandstones
MediumSandstone_1 = {'Name':"MediumSandstone_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':587.05}},'RockType':"Class 7"}
MediumSandstone_2 = {'Name':"MediumSandstone_2",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':590.06}},'RockType':"Class 7"}
MediumSandstone_3 = {'Name':"MediumSandstone_3",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':47.29}},'RockType':"Class 7"}

#Fine Sandstones
FineSandstone_1 = {'Name':"FineSandstone_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':689.44}},'RockType':"Class 8"}

#Unknowns - Rocktype Marls
Unknown_1 = {'Name':"Unknown_1",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':5015.360}},'RockType':"Class 5"}
Unknown_2 = {'Name':"Unknown_2",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':1145.97}},'RockType':"Class 5"}
Unknown_3 = {'Name':"Unknown_3",'Layer_Properties':{'Area':{'Name':"Area",'Distribution':"constant",'Constant':4899.48}},'RockType':"Class 5"}


#Region Collocation
Regions = {'Region 1': Grainstone_1,
           'Region 2': Grainstone_2,
           'Region 3': Grainstone_3,
           'Region 4': Grainstone_4,
           'Region 5': Grainstone_5,
           'Region 6': Grainstone_6,
           'Region 7': Grainstone_7,
           'Region 8': Grainstone_8,
           'Region 9': Grainstone_9,
           'Region 10': Mudstone_1,
           'Region 11': Mudstone_2,
           'Region 12': Mudstone_3,
           'Region 13': Mudstone_4,
           'Region 14': Mudstone_5,
           'Region 15': Packstone_1,
           'Region 16': Wackstone_1,
           'Region 17': Marl_1,
           'Region 18': Marl_2,
           'Region 19': Marl_3,
           'Region 20': Marl_4,
           'Region 21': Marl_5,
           'Region 22': Marl_6,
           'Region 23': Marl_7,
           'Region 24': Marl_8,
           'Region 25': CoarseSandstone_1,
           'Region 26': MediumSandstone_1,
           'Region 27': MediumSandstone_2,
           'Region 28': MediumSandstone_3,
           'Region 29': FineSandstone_1,
           'Region 30': Unknown_1,
           'Region 31': Unknown_2,
           'Region 32': Unknown_3}

#Rock Type Collocation
Parameter_Classes = {'Class 1':Grainstones,'Class 2':Mudstones,'Class 3':Packstones,'Class 4':Wackstones,'Class 5':Marls,'Class 6':CoarseSandstones,'Class 7':MediumSandstones,'Class 8':FineSandstones}

GlobalProperties = []
