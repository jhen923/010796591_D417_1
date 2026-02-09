import os
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

#---Reporting Mechanism---
report_lines = []
documents_dir = os.path.join(os.path.expanduser('~'), 'Documents')
report_filename = os.path.join(documents_dir, "vlan_provisioning_report.txt")

# --- Device Definitions ---
all_devices = [
    { 'device_type': 'extreme_exos', 'ip':'10.10.1.22', 'username': 'admin', 'password': '' }, # ESW1
    { 'device_type': 'extreme_exos', 'ip':'10.10.1.32', 'username': 'admin', 'password': '' }, # ESW2
    { 'device_type': 'extreme_exos', 'ip':'10.10.1.31', 'username': 'admin', 'password': '' }, # ESW3
    { 'device_type': 'extreme_exos', 'ip':'10.10.1.30', 'username': 'admin', 'password': '' }, # ESW4
]

# --- VLAN Definitions ---
vlans_to_create = [
    { 'name': 'User_Network', 'tag': 10 }, # For ESW1
    { 'name': 'ACCT_Network', 'tag': 20 }, # For ESW2
    { 'name': 'MGMT_Network', 'tag': 30 }, # For ESW3
    { 'name': 'IT_Network',   'tag': 40 }, # For ESW4
]

for device, vlan_info in zip(all_devices, vlans_to_create):

    report_lines.append("\n{0} PROCESSING DEVICE: {1} {0}".format('='*25, device['ip']))
    net_connect = None
    
    #Imma be honest, I had a lot of help from Gemini and Reddit AND Stackables to make all of this
    
    try:
        net_connect = ConnectHandler(**device)
        
        #IDENTIFY EXISTING VLANS
        report_lines.append("\n---IDENTIFYING INITIAL VLAN STATE---")
        initial_vlans = net_connect.send_command('show vlan')
        report_lines.append(initial_vlans)
        
        #CONFIGURE THE ASSIGNED VLAN
        vlan_name = vlan_info['name']
        vlan_tag = vlan_info['tag']
            
        report_lines.append("\n---CONFIGURING ASSIGNED VLAN: '{0}' (Tag: {1}) ---".format(vlan_name, vlan_tag))

        config_commands = [
            'create vlan {}'.format(vlan_name),
            'configure vlan {} tag {}'.format(vlan_name, vlan_tag)
        ]
        output = net_connect.send_config_set(config_commands)
        report_lines.append(output)
            
        #VERIFY FINAL VLAN CONFIGURATION
        report_lines.append("\n---VERIFYING FINAL VLAN STATE ---")
        final_vlans = net_connect.send_command('show vlan')
        report_lines.append(final_vlans)
        
        # --- FIXED: Replaced f-string with .format() ---
        report_lines.append("\n--- SUCCESSFULLY PROCESSED {0} ---".format(device['ip']))

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        # --- FIXED: Replaced f-string with .format() ---
        report_lines.append("!!! LOGIN OR CONNECTION FAILED for {0}: {1} !!!".format(device['ip'], e))
    except Exception as e:
        # --- FIXED: Replaced f-string with .format() ---
        report_lines.append("!!! AN UNEXPECTED ERROR OCCURRED for {0}: {1} !!!".format(device['ip'], e))
        
    finally:
        if net_connect:
            net_connect.disconnect()
            # --- FIXED: Replaced f-string with .format() ---
            report_lines.append("--- Connection to {0} closed ---".format(device['ip']))

try:
    os.makedirs(documents_dir, exist_ok=True)
    
    with open(report_filename, 'w') as f:
        f.write('\n'.join(report_lines))
        
    print("Script finished. Report saved to '{}'".format(report_filename))
    
except Exception as e:
    print("!!! FAILED TO WRITE REPORT FILE: {} !!!".format(e))
