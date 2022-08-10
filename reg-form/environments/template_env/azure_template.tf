
# Configure the Microsoft Azure Provider
provider "azurerm" {

}

#LDS User Variables
variable "USERNAME" {
  type        = string
}

# Create a resource group if it doesn’t exist
resource "azurerm_resource_group" "CloudGuard" {
    name     = "${var.USERNAME}"
    location = "westus"

}

# Create virtual network
resource "azurerm_virtual_network" "network" {
    name                = "myVnet"
    address_space       = ["10.0.0.0/16"]
    location            = "westus"
    resource_group_name = "${azurerm_resource_group.CloudGuard.name}"

}

# Create subnet
resource "azurerm_subnet" "subnet" {
    name                 = "mySubnet"
    resource_group_name  = "${azurerm_resource_group.CloudGuard.name}"
    virtual_network_name = "${azurerm_virtual_network.network.name}"
    address_prefix       = "10.0.1.0/24"
}

# Create public IPs
resource "azurerm_public_ip" "publicip" {
    name                         = "cpPublicIP"
    location                     = "westus"
    resource_group_name          = "${azurerm_resource_group.CloudGuard.name}"
    allocation_method            = "Dynamic"
}

# Create Network Security Group and rule
resource "azurerm_network_security_group" "CPnsg" {
    name                = "myNetworkSecurityGroup"
    location            = "westus"
    resource_group_name = "${azurerm_resource_group.CloudGuard.name}"
    
    security_rule {
        name                       = "SSH"
        priority                   = 1001
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }

    security_rule {
        name                       = "HTTPS"
        priority                   = 1002
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "443"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }

}

# Create network interface
resource "azurerm_network_interface" "myterraformnic" {
    name                      = "myNIC"
    location                  = "westus"
    resource_group_name       = "${azurerm_resource_group.CloudGuard.name}"
    network_security_group_id = "${azurerm_network_security_group.CPnsg.id}"

    ip_configuration {
        name                          = "myNicConfiguration"
        subnet_id                     = "${azurerm_subnet.subnet.id}"
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id          = "${azurerm_public_ip.publicip.id}"
    }

}


# Create virtual machine
resource "azurerm_virtual_machine" "myterraformvm" {
    name                  = "CloudGuard"
    location              = "westus"
    resource_group_name   = "${azurerm_resource_group.CloudGuard.name}"
    network_interface_ids = ["${azurerm_network_interface.myterraformnic.id}"]
    vm_size               = "Standard_B2ms"

    plan {
        name = "sg-ngtx"
        publisher = "checkpoint"
        product = "check-point-cg-r8020-blink-v2"
        }

    storage_os_disk {
        name              = "myOsDisk"
        caching           = "ReadWrite"
        create_option     = "FromImage"
        managed_disk_type = "Premium_LRS"
    }

    storage_image_reference {
        publisher = "Checkpoint"
        offer     = "check-point-cg-r8020-blink-v2"
        sku       = "sg-ngtx"
        version   = "latest"
    }

    os_profile {
        computer_name  = "CloudGuard"
        admin_username = "admin2"
        admin_password = "1qaz!QAZ1qaz!QAZ"
        custom_data =  "#!/bin/bash\nblink_config -s 'gateway_cluster_member=false&ftw_sic_key=vpn123&upload_info=true&download_info=true&reboot_if_required=true'"

    }
    
    os_profile_linux_config {
        disable_password_authentication = false
    }

    tags = {
        device = "Check Point CloudGuard"
    }
}

output "PublicIP" {
  value = "${data.azurerm_public_ip.publicip.ip_address}"
}