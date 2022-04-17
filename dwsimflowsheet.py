# function PowerGenerated1 returns power generated from ORC simulation from a number of inputs

def PowerGenerated1(massFlow = 10.0, temperature = 260.0, return_dict = {}):
	# imports needed
	import pythoncom
	pythoncom.CoInitialize()
	import clr
	import System
	from System.IO import Directory, Path, File
	from System import String, Environment, Array

	# path to your dwsim file
	path2dwsim = "C:\\DWSIM7\\"

	# clr references needed
	clr.AddReference(path2dwsim + "CapeOpen.dll")
	clr.AddReference(path2dwsim + "DWSIM.Automation.dll")
	clr.AddReference(path2dwsim + "DWSIM.Interfaces.dll")
	clr.AddReference(path2dwsim + "DWSIM.GlobalSettings.dll")
	clr.AddReference(path2dwsim + "DWSIM.SharedClasses.dll")
	clr.AddReference(path2dwsim + "DWSIM.Thermodynamics.dll")
	clr.AddReference(path2dwsim + "DWSIM.UnitOperations.dll")

	clr.AddReference(path2dwsim + "DWSIM.Inspector.dll")
	clr.AddReference(path2dwsim + "DWSIM.MathOps.dll")
	clr.AddReference(path2dwsim + "TcpComm.dll")
	clr.AddReference(path2dwsim + "Microsoft.ServiceBus.dll")
	clr.AddReference(path2dwsim + "System.Buffers.dll")
	clr.AddReference(path2dwsim + "SkiaSharp.dll")

	# path to your dwsim simulation/flowsheet
	path2sim = "C:\\DWSIM Models\\DWSIM_complexer.dwxmz"

	from DWSIM.Automation import Automation2

	# create automation manager
	interf = Automation2() 

	# load simulation
	sim = interf.LoadFlowsheet(path2sim)

	# creating streams and objects from simulation
	# can add streams and objects as you like
	steamIn = sim.GetFlowsheetSimulationObject("Steam In")
	turbine = sim.GetFlowsheetSimulationObject("Turbine")

	# setting mass flow and temperature of stream "steam in"
	# can set properties of streams and objects as you like
	steamIn.SetMassFlow(float(massFlow))
	steamIn.SetTemperature(float(temperature) + 273.15)

	print("Running Simulation with mass flow " + massFlow + " kg/s, please wait...")
	print("Running Simulation with temperature " + temperature + " C, please wait...")

	# running and calculating simulation
	interf.CalculateFlowsheet(sim, None)

	# checking for errors
	if sim.Solved == False:
		print("Error solving flowsheet: " + sim.ErrorMessage)

	# output is Power Generated from Turbine
	return_dict["pg"] = String.Format("Power Generated: {0} kW", turbine.DeltaQ)

