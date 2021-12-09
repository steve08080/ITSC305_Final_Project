import spidev
import time

# Commands from page 8 of the datasheet. I only use READ, WRITE, WREN in lab 5 but included all of them
# If I do more with EEPROM I can expand this file later and reuse it
READ    = 0b00000011
# Read reads from memory. When EEPROM receives this, it then expects a 16 bit address
# Then, it will send data from memory over MISO each clock pulse, incrementing the internal address counter each time
WRITE   = 0b00000010
# Write writes to memory. When EEPROM receives this, it then expects a 16 bit address, then up to 128 bytes of data
WREN    = 0b00000110
# WREN is Write Enable. It sets the write latch to allow writing operations
# The write latch resets: on powerup, when a write occurs, when an erase occurs, when disabled by WRDI (Write Disable)
WRDI    = 0b00000100
RDSR    = 0b00000101
WRSR    = 0b00000001
PE      = 0b01000010
SE      = 0b11011000
CE      = 0b11000111
RDID    = 0b10101011
DPD     = 0b10111001

# Max speed on lower power is 10 MHz from page 3 of datasheet
MAXSPEED = 10000000

class EEPROM:
    def __init__(self, bus, CE):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, CE)
        self.spi.max_speed_hz = MAXSPEED

    def write(self, address, data):
        # This function takes an address to write to, and writes there, using writebytes
        upper = address >> 8  # Splits the given address to upper and lower 8 bits
        lower = address & 0x00FF 
        self.spi.writebytes([WREN])  # Write Enable required before write can take place. Resets after Write
        time.sleep(0.005)
        self.spi.writebytes([WRITE,upper,lower,data])  
        time.sleep(0.005)

    def read(self, address, count=1):

        # This function takes an address to read from, and the number of bytes to read, using xfer2
        # xfer does a SPI transaction. What that means is it sends data and then reads MISO. It returns the read MISO values
        # spi.xfer2([READ,0x00,0x11,0x00]) will return [0, 0, 0, <value at 0x11>]
        ## Sends READ(0x3), no output from slave (0)
        ## Sends 0x00,      the upper 8 bits of 16 bit address, no output from slave (0)
        ## Sends 0x11,      the lower 8 bits of 16 bit address, no output from slave (0)
        ## Sends 0x00,      arbitrary value to pulse clock,     slave outputs value at 0x11 (and increments its Address Pointer)
        # This function returns an array of only the values read from memory

        upper = address >> 8  # Gets the upper 8 bits of the address
        lower = address & 0x00FF  # Gets the lower 8 bits of the address
        args = [READ,upper,lower]
        for i in range(count):  # This loop adds a number 0s to the args equal to amount of bytes to read, to pulse clock that many times
            args.append(0x00)
        values = self.spi.xfer2(args)
        time.sleep(0.005)
        return values[3:]  # Chops off the first 3 values, they will be 0 because nothing was read from memory yet


# mem = EEPROM(0,0)
# mem.write(0,123)
# mem.write(2,7)
# print(mem.read(0,3))
## Result: [123, <value at 0x1>, 7]
