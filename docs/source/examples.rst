========
Examples
========

Setting port mirroring
======================

Example of setting port mirroring. Traffic will be redirected from port 1 to port 2.

.. literalinclude :: ../../examples/02_set_port_mirroring.py
   :language: python

Output:

.. code::

   $ python 02_set_port_mirroring.py
   Connecting... OK
   Setting port mirroring... OK

   Mirrored ports:
   {'Mirrored Ports': {'Port 1': {'Egress': 'Enable', 'Ingress': 'Enable'},
                       'Port 2': {'Egress': 'Disable', 'Ingress': 'Disable'},
                       'Port 3': {'Egress': 'Disable', 'Ingress': 'Disable'},
                       'Port 4': {'Egress': 'Disable', 'Ingress': 'Disable'},
                       'Port 5': {'Egress': 'Disable', 'Ingress': 'Disable'},
                       'Port 6': {'Egress': 'Disable', 'Ingress': 'Disable'},
                       'Port 7': {'Egress': 'Disable', 'Ingress': 'Disable'},
                       'Port 8': {'Egress': 'Disable', 'Ingress': 'Disable'}}}

   Mirroring port:
   {'Mirroring Port': 'Port 2'}



Creating Port Based VLAN
========================

Creating port base VLAN with ID 2. Ports 1 nad 2 are added.

.. literalinclude :: ../../examples/03_create_port_based_vlan.py
   :language: python

Output:

.. code::

   $ python 03_create_port_based_vlan.py
   {'Port Based VLAN Configuration': 'Enable', 'VLANs': [{'VLAN ID': '1', 'VLAN Member Port': '3-8'}, {'VLAN ID': '2', 'VLAN Member Port': '1-2'}]}wink:|


Creating CLI Script
===================

Basic script with error handling.

.. literalinclude :: ../../examples/04_psv.py
   :language: python

Output:

.. code::

   $ python 04_psv.py -i=192.168.1.42 -l=admin -p=admin -s=3
   [*] Port 3
   Status:        Enabled
   Link Status:   Link Down
   TxGoodPkt:     0
   TxBadPkt:      0
   RxGoodPkt:     0
   RxBadPkt:      0


Yes, I know - password |:wink:|
