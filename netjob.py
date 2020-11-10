from netmiko import ConnectHandler, SCPConn
import machine


def sendFileToMachine(host: machine.Machine, source_file, dest_file):
    net_device = {
        'device_type': 'linux',
        'ip': host.ip,
        'username': host.username,
        'password': host.password,
    }
    try:
        ssh_conn = ConnectHandler(**net_device)
        scp_conn = SCPConn(ssh_conn)
        putFileState = scp_conn.scp_put_file(source_file, dest_file)
        scp_conn.close()
        ssh_conn.disconnect()
        host.status = 2  # Passed
        return True  # succeeded sending the file to machine
    except:
        print(f"Failed connect to {host.ip}")
        host.status = 0  # Failed
        return False  # Filed sending the file to machine


def runCommandOnMachine(host: machine.Machine, command) -> list:
    net_device = {
        'device_type': 'linux',
        'ip': host.ip,
        'username': host.username,
        'password': host.password,
    }
    # SSH connection
    try:
        net_connect = ConnectHandler(**net_device)
        transferState = net_connect.send_command(command)
        net_connect.disconnect()
        # print(f"transferState = {transferState}")
        return [True, str(transferState)]  # Passed
    except:
        print(f"Failed connect to {host.ip}")
        return [False, '']


def pullFileFromMachine(host: machine.Machine, filename):
    net_device = {
        'device_type': 'linux',
        'ip': host.ip,
        'username': host.username,
        'password': host.password,
    }
    try:
        ssh_conn = ConnectHandler(**net_device)
        scp_conn = SCPConn(ssh_conn)
        putFileState = scp_conn.p
        print(putFileState)
        scp_conn.close()
        ssh_conn.disconnect()
        host.status = 2  # Passed
        return True  # succeeded sending the file to machine
    except:
        print(f"Failed connect to {host.ip}")
        host.status = 0  # Failed
        return False  # Filed sending the file to machine
