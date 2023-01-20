====================================================
Library to control network switch tp-link TL-SG108PE
====================================================

.. image:: https://circleci.com/gh/marcinooo/switch_TL_SG108PE/tree/main.svg?style=svg
    :target: https://circleci.com/gh/marcinooo/switch_TL_SG108PE/?branch=main


|

:Author: marcinooo
:Tags: Python, Selenium, tp-link, switch, TL-SG108PE, Library

:abstract:

   Library to control switch via admin page.

.. contents ::


Description
===========

Switch tp-link TL-SG108PE:

.. image:: switch_tp_link_TL_SG108PE.jpg
    :alt: tp-link TL-SG108PE

**Details**

.. list-table::

   * - Firmware Version
     - 1.0.0 Build 20200415 Rel.54962
   * - Hardware Version
     - TL-SG108PE 3.0

Above switch can be control from Python code. It implements methods to manage main switch settings.
Methods are divided in sections:

.. role:: python(code)
   :language: python

* system:
    * :python:`system_info() -> Dict[str, str]`
    * :python:`set_device_description(description: str) -> None`
    * :python:`ip_settings() -> Dict[str, str]`
    * :python:`enable_dhcp_configuration() -> None`
    * :python:`disable_dhcp_configuration() -> None`
    * :python:`set_ip(ip_address: str, subnet_mask: str, default_gateway: str) -> None`
    * :python:`led_on() -> None`
    * :python:`led_off() -> None`
    * :python:`user_account() -> Dict[str, str]`
    * :python:`set_user_account_details(username: str, current_password: str, new_password: str, confirm_password: str) -> None`
* switching:
    * :python:`ports_settings() -> Dict[str, Dict[str, str]]`
    * :python:`set_port_settings(port: int, status: STATUS, speed: SPEED, flow_control: FLOW_CONTROL) -> None`
    * :python:`igmp_snooping() -> Dict[str, str]`
    * :python:`enable_igmp_snooping() -> None`
    * :python:`disable_igmp_snooping() -> None`
    * :python:`enable_report_message_suppression() -> None`
    * :python:`disable_report_message_suppression() -> None`
    * :python:`lag_settings() -> Dict[str, str]`
    * :python:`set_lag_ports(lag_id: int, ports: List[int]) -> None`
    * :python:`unset_lag_ports(lag_id: int) -> None`
* monitoring:
    * :python:`port_statistics(refresh: bool = True) -> Dict[str, Dict[str, str]]`
    * :python:`refresh_port_statistics() -> None`
    * :python:`mirrored_ports() -> Dict[str, Dict[str, str]]`
    * :python:`mirroring_port() -> Dict[str, str]`
    * :python:`enable_port_mirroring(mirrored_ports: List[int], mirroring_port: int, ingress: bool = True, egress: bool = True) -> None`
    * :python:`disable_port_mirroring() -> None`
    * :python:`loop_prevention() -> Dict[str, str]`
    * :python:`enable_loop_prevention() -> None`
    * :python:`disable_loop_prevention() -> None`
* VLAN:
    * :python:`mtu_vlan_configuration() -> Dict[str, str]`
    * :python:`enable_mtu_vlan_configuration() -> None`
    * :python:`disable_mtu_vlan_configuration() -> None`
    * :python:`change_mtu_vlan_uplink_port(port: int) -> None`
    * :python:`port_based_vlan_configuration() -> Dict[str, Union[List[str], str]]`
    * :python:`enable_port_based_vlan_configuration() -> None`
    * :python:`disable_port_based_vlan_configuration() -> None`
    * :python:`add_port_based_vlan(vlan_id: int, ports: List[int]) -> None`
    * :python:`remove_port_based_vlan(vlan_id: int) -> None`
    * :python:`ieee_802_1q_vlan_configuration() -> Dict[str, str]`
    * :python:`enable_ieee_802_1q_vlan_configuration() -> None`
    * :python:`disable_ieee_802_1q_vlan_configuration() -> None`
    * :python:`add_ieee_802_1q_vlan(vlan_id: int, ports: List[IEEE8021QPort], vlan_name: str = '') -> None`
    * :python:`remove_ieee_802_1q_vlan(vlan_id: int) -> None`
* QoS:
   * :python:`qos_mode(self) -> str`
   * :python:`set_port_base_qos_mode(self) -> None`
   * :python:`set_802_1p_based_qos_mode(self) -> None`
   * :python:`set_dscp_802_1p_based_qos_mode(self) -> None`
   * :python:`priority_queue_port_settings(self) -> Dict[str, str]`
   * :python:`set_priority_queue_in_port_based_qos_mode(self, port: int, priority_queue: PriorityQueue) -> None`


Documentation
-------------

Documentation can be found `here <https://switch-tl-sg108pe.readthedocs.io/en/latest/>`_ :smiley:.

Usage
=====

An example of using the library to create port based VLAN.

Before running script install library. Next set environment variables in console via commands:

``$ export ADMIN_IP=<switch ip>``

``$ export ADMIN_USERNAME=<admin username>``

``$ export ADMIN_PASSWORD=<admin password>``


.. code:: python

    import os
    from switch_TL_SG108PE.switch_manager import SwitchManager


    # set required system variables before running script (example for Linux system)
    # $ export ADMIN_IP=<switch ip>
    # $ export ADMIN_USERNAME=<admin username>
    # $ export ADMIN_PASSWORD=<admin password>

    switch_manager = SwitchManager()
    switch_manager.connect(os.environ['ADMIN_IP'],
                           os.environ['ADMIN_USERNAME'],
                           os.environ['ADMIN_PASSWORD'])
    system = switch_manager.control('system')
    info = system.system_info()
    print(info)
    switch_manager.disconnect()


More examples can be found in documentation :wink:.


Installation
============

Install from PyPI:

``$ pip install switch_TL_SG108PE``

Install from github:

``$ pip install git+https://github.com/marcinooo/switch_TL_SG108PE``


License
=======

license_ (MIT)

.. _license: https://github.com/marcinooo/switch_TL_SG108PE/blob/main/LICENSE.txt

.. role:: python(code)
   :language: python
