#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def createNetwork():
    net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')

    info('*** Adding controller\n')
    kmc0=net.addController(name='kmc0',
                                   controller=Controller,
                                   protocol='tcp',
                                   port=6633)

    info('*** Add switches\n')
    kms11 = net.addSwitch('kms11', cls=OVSKernelSwitch)
    kms12 = net.addSwitch('kms12', cls=OVSKernelSwitch)
    kms21 = net.addSwitch('kms21', cls=OVSKernelSwitch)
    kms22 = net.addSwitch('kms22', cls=OVSKernelSwitch)
    kms23 = net.addSwitch('kms23', cls=OVSKernelSwitch)
    kms24 = net.addSwitch('kms24', cls=OVSKernelSwitch)

    info('*** Add hosts\n')
    kmh211 = net.addHost('kmh211', cls=Host, ip='10.99.1.11/24', defaultRoute='via 10.99.1.1')
    kmh212 = net.addHost('kmh212', cls=Host, ip='10.99.1.12/24', defaultRoute='via 10.99.1.1')
    kmh221 = net.addHost('kmh221', cls=Host, ip='10.99.1.21/24', defaultRoute='via 10.99.1.1')
    kmh222 = net.addHost('kmh222', cls=Host, ip='10.99.1.22/24', defaultRoute='via 10.99.1.1')
    kmh231 = net.addHost('kmh231', cls=Host, ip='10.99.1.31/24', defaultRoute='via 10.99.1.1')
    kmh232 = net.addHost('kmh232', cls=Host, ip='10.99.1.32/24', defaultRoute='via 10.99.1.1')
    kmh241 = net.addHost('kmh241', cls=Host, ip='10.99.1.41/24', defaultRoute='via 10.99.1.1')
    kmh242 = net.addHost('kmh242', cls=Host, ip='10.99.1.42/24', defaultRoute='via 10.99.1.1')

    info('*** Add links\n')
    # Connect switches in the upper layer to the controller switch
    net.addLink(kms11, kms21)
    net.addLink(kms11, kms22)
    net.addLink(kms12, kms23)
    net.addLink(kms12, kms24)

    # Connect hosts to switches
    net.addLink(kms21, kmh211)
    net.addLink(kms21, kmh212)

    net.addLink(kms22, kmh221)
    net.addLink(kms22, kmh222)

    net.addLink(kms23, kmh231)
    net.addLink(kms23, kmh232)

    net.addLink(kms24, kmh241)
    net.addLink(kms24, kmh242)

    info('*** Starting network\n')
    net.build()

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('kms11').start([kmc0])
    net.get('kms12').start([kmc0])
    net.get('kms21').start([kmc0])
    net.get('kms22').start([kmc0])
    net.get('kms23').start([kmc0])
    net.get('kms24').start([kmc0])

    info('*** Post configure switches and hosts\n')
    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createNetwork()

