import configparser
import yaml
import io

file_content = """
[Local_Switch]
ram=512MB
vcpus=1
qemu_binary=/usr/bin/qemu-system-x86_64(v4.2.1)
boot_priority=cddvd-rom,hdd
on_close=power_off_vm
console_type=telnet
adapters=13
base_mac=0c:c0:5e:66:00:00
type=Realtek 8139 Ethernet (rtl8139)
replicate_network_connection_status=Y

[IT_Network]
ram=512MB
vcpus=1
qemu_binary=/usr/bin/qemu-system-x86_64(v4.2.1)
boot_priority=cddvd-rom,hdd
on_close=power_off_vm
console_type=telnet
adapters=13
base_mac=0c:1c:b2:85:00:00
type=Realtek 8139 Ethernet (rtl8139)
replicate_network_connection_status=Y

[MGMT_Network]
ram=512MB
vcpus=1
qemu_binary=/usr/bin/qemu-system-x86_64(v4.2.1)
boot_priority=cddvd-rom,hdd
on_close=power_off_vm
console_type=telnet
adapters=13
base_mac=0c:cc:78:5d:00:00
type=Realtek 8139 Ethernet (rtl8139)
replicate_network_connection_status=Y

[ACCT_Network]
ram=512MB
vcpus=1
qemu_binary=/usr/bin/qemu-system-x86_64(v4.2.1)
boot_priority=cddvd-rom,hdd
on_close=power_off_vm
console_type=telnet
adapters=13
base_mac=0c:40:34:07:00:00
type=Realtek 8139 Ethernet (rtl8139)
replicate_network_connection_status=Y

[User_Network]
ram=512MB
vcpus=1
qemu_binary=/usr/bin/qemu-system-x86_64(v4.2.1)
boot_priority=cddvd-rom,hdd
on_close=power_off_vm
console_type=telnet
adapters=13
base_mac=0c:e0:f2:0b:00:00
type=Realtek 8139 Ethernet (rtl8139)
replicate_network_connection_status=Y
        
         # End of Inventory #
"""



file_name = "Switch_Inventory.yaml"

config = configparser.ConfigParser()

config.read_string(file_content)

data_dict = {section: dict(config.items(section)) for section in config.sections()}

#I went from txt to ini to yaml, so I changed a LOT of this using random things online.
try:
    with open(file_name, "w", encoding="utf-8") as f:
        yaml.dump(data_dict, f, default_flow_style=False, sort_keys=False)
    print(f"YAML inventory '{file_name}' has been created successfully. Nice!")

except Exception as e:
    print(f"Dawg idk what happened, JK here is: {e}")
