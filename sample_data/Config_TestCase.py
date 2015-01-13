# TestCase Var File
Dump = False
Model_Name = "TestCase"
N = 100000
Seed = 666
Regions = [["Sandstone Reservoir"]]  # Name,Seed
GlobalProperties = [["Bo", "normal", [1.34, 0.06]]]
Properties = [[["Porosity", "uniform", [0.05, 0.1]], ["Height","uniform",[0,1000]]]]
ooip_equation = "7758*(self.properties[0].samples*self.properties[1].samples*self.properties[3].samples*(1-self.properties[2].samples)/self.parent_model.global_properties[0].samples)"
perm_grainstone = "45.35E8*m.pow(self.properties[0].samples,8.537)"
swi_grainstone = "0.02219*m.pow(self.properties[1].samples,-0.316)*m.pow(self.properties[0].samples,-1.745)"
Equations = [["Class 1 Permeability", perm_grainstone], ["Class 1 Swi", swi_grainstone]]