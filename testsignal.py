import pyvisa
import time

# Initialize the resource manager and connect to the instrument
rm = pyvisa.ResourceManager()
print(rm.list_resources())

# Connect to the function generator
FG = rm.open_resource("USB0::0x0957::0x4108::MY51400413::0::INSTR")
print(FG.query("*IDN?"))

# Define the resource address (update with your actual address)
resource_address = 'USB0::0x2A8D::0x900D::MY52250153::0::INSTR'

# Open a connection to the oscilloscope
myScope = rm.open_resource(resource_address)

# ---- Channel 1 Configuration ---- #
# Set Channel 1 as a pulse waveform with a frequency of 1 MHz, amplitude of 3.3V, and duty cycle of 50%
FG.write("SOURce:FUNCtion1 PULSE")
FG.write("SOURce:FREQuency1 2MHz")  # Set frequency to 1 MHz for Channel 1

amplitude_value_1 = 5

  # Amplitude for Channel 1
FG.write(f"SOURce:VOLTage1 {amplitude_value_1}Vpp")

offset_value_1 = amplitude_value_1 / 2
FG.write(f"SOURce:VOLTage1:OFFSet {offset_value_1}")

duty_cycle_1 = 50  # Duty cycle for Channel 2
  # Set duty cycle


# for duty_cycle in range(15, 0, -1):
#             print(f"Setting duty cycle to {duty_cycle}% and measuring...")
FG.write(f":FUNC1:PULS:DCYC {duty_cycle_1}PCT")

FG.write("OUTPut1 ON")  # Enable output on Channel 1
FG.write("OUTPut1:LOAD 50")  # Set load impedance to 50 Ohms on Channel 1

myScope.write(":CHANnel1:DISPlay ON")
myScope.write(":CHANnel1:SCALe 2")
myScope.write(":TIMebase:SCALe 8E-6")


myScope.write(":CHANnel2:DISPlay ON")
myScope.write(":CHANnel2:DISPlay:SCALe 2")
myScope.write(":TIMebase:SCALe 10E-6")

myScope.write(":TRIGger:MODE EDGE")
myScope.write(":TRIGger:EDGE:SOURCe CHANnel1")
myScope.write(":TRIGger:LEVel CHANnel1,2")
myScope.write(":TRIGger:EDGE:SLOPe POSitive")



# time.sleep()
myScope.write(":RUN")
