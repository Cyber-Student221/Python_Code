import tkinter as tk
from tkinter import ttk
from ipaddress import IPv4Address, IPv4Network, AddressValueError, summarize_address_range
import math

class SubnetCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.title("Variable Length Subnet Calculator")
        self.geometry("800x600")

        # Configure rows and columns to fit the window size
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # IP address label and entry
        self.ip_label = ttk.Label(self, text="IP address:")
        self.ip_label.grid(row=0, column=0, pady=5, padx=5)

        self.ip_entry = ttk.Entry(self)
        self.ip_entry.grid(row=0, column=1, pady=5, padx=5)

        # CIDR prefix label and combobox
        self.prefix_label = ttk.Label(self, text="CIDR:")
        self.prefix_label.grid(row=0, column=2, pady=5, padx=5)

        self.prefix_combo = ttk.Combobox(self, values=list(range(1, 31)), state="readonly")
        self.prefix_combo.set(24)
        self.prefix_combo.grid(row=0, column=3, pady=5, padx=5)

        # Validate IP button and available addresses label
        self.validate_button = ttk.Button(self, text="Validate IP", command=self.validate_ip)
        self.validate_button.grid(row=0, column=4, pady=5, padx=5)

        self.available_addresses_label = ttk.Label(self, text="")
        self.available_addresses_label.grid(row=0, column=5, pady=5, padx=5)

        # Number of subnets label and entry
        self.subnets_label = ttk.Label(self, text="Number of subnets:")
        self.subnets_label.grid(row=1, column=0, pady=5, padx=5)

        self.subnets_entry = ttk.Entry(self, state="disabled")
        self.subnets_entry.grid(row=1, column=1, pady=5, padx=5)

        # Create subnets button
        self.create_subnets_button = ttk.Button(self, text="Create Subnets", command=self.create_subnets, state="disabled")
        self.create_subnets_button.grid(row=1, column=2, pady=5, padx=5)

        # Hosts labels and entries, subnet name labels and entries
        self.hosts_labels = []
        self.hosts_entries = []
        self.subnet_name_labels = []
        self.subnet_name_entries = []

        # Calculate button
        self.calculate_button = ttk.Button(self, text="Calculate", command=self.calculate, state="disabled")
        self.calculate_button.grid(row=1, column=4, pady=5, padx=5)

        # Subnet treeview and scrollbar
        self.subnet_treeview = ttk.Treeview(self, columns=("subnet_name", "needed_size", "allocated_size", "subnet_address", "subnet_mask", "broadcast_address", "assignable_range"), show="headings")
        self.subnet_treeview.heading("subnet_name", text="Subnet Name")
        self.subnet_treeview.heading("needed_size", text="Needed Size")
        self.subnet_treeview.heading("allocated_size", text="Allocated Size")
        self.subnet_treeview.heading("subnet_address", text="Subnet Address")
        self.subnet_treeview.heading("subnet_mask", text="Subnet Mask (CIDR)")
        self.subnet_treeview.heading("broadcast_address", text="Broadcast Address")
        self.subnet_treeview.heading("assignable_range", text="Assignable IP Range")
        self.subnet_treeview.column("subnet_name", anchor="center")
        self.subnet_treeview.column("needed_size", anchor="center")
        self.subnet_treeview.column("allocated_size", anchor="center")
        self.subnet_treeview.column("subnet_address", anchor="center")
        self.subnet_treeview.column("subnet_mask", anchor="center")
        self.subnet_treeview.column("broadcast_address", anchor="center")
        self.subnet_treeview.column("assignable_range", anchor="center")
        self.subnet_treeview.grid(row=3, column=0, pady=5, padx=5, columnspan=6, sticky="nsew")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.subnet_treeview.yview)
        self.scrollbar.grid(row=3, column=6, pady=5, padx=5, sticky="ns")
        self.subnet_treeview.configure(yscrollcommand=self.scrollbar.set)
        
    def validate_ip(self):
        # Get the IP address and CIDR prefix from the GUI widgets
        ip_str = self.ip_entry.get()
        prefix = self.prefix_combo.get()

        try:
            # Check if the IP address is valid using the IPv4Address class from the ipaddress module
            IPv4Address(ip_str)
            
            # Calculate the network address and number of available IP addresses using the IPv4Network class
            network = IPv4Network(ip_str + f"/{prefix}", strict=False)
            self.available_addresses_label["text"] = f"Available addresses: {network.num_addresses}"

            # Enable the "Create Subnets" button and the "Number of subnets" entry
            self.subnets_entry.config(state="normal")
            self.create_subnets_button.config(state="normal")

        except AddressValueError:
            # Display an error message if the IP address is not valid
            self.error_message()

    def error_message(self):
        # Create a new Toplevel window to display the error message
        error_window = tk.Toplevel(self)
        error_window.title("Error")
        
        # Create a label with the error message text and pack it into the window
        error_label = ttk.Label(error_window, text="Invalid IP address.")
        error_label.pack(pady=5, padx=5)
        
        # Create a button to dismiss the error window and pack it into the window
        error_ok_button = ttk.Button(error_window, text="OK", command=error_window.destroy)
        error_ok_button.pack(pady=5, padx=5)

    def calculate(self):
        # Clear any existing data from the subnet treeview
        self.subnet_treeview.delete(*self.subnet_treeview.get_children())
        
        # Get the IP address, number of subnets, and CIDR prefix from the GUI widgets
        ip_str = self.ip_entry.get()
        subnets = int(self.subnets_combo.get())
        prefix = int(self.prefix_combo.get())

        try:
            # Create an IPv4Network object with the entered IP address and CIDR prefix
            network = IPv4Network(ip_str + f"/{prefix}", strict=False)
        except AddressValueError:
            # Display an error message if the IP address is not valid
            self.error_message()
            return

        # Divide the available IP addresses into subnets based on the requested number of hosts per subnet
        available_subnets = list(summarize_address_range(network.network_address, network.broadcast_address))
        allocated_subnets = []

        for i, needed_hosts in enumerate([int(entry.get()) for entry in self.hosts_entries]):
            # Calculate the required subnet size for the specified number of hosts
            required_subnet_size = 32 - math.ceil(math.log2(needed_hosts + 2))
            
            # Find the smallest available subnet that can accommodate the required number of hosts
            for subnet in available_subnets:
                if subnet.prefixlen <= required_subnet_size:
                    allocated_subnets.append(subnet)
                    available_subnets.remove(subnet)
                    break
            else:
                # Display a warning message if there are not enough available subnets to accommodate the requested number of hosts
                self.warning_message(needed_hosts)
                return

        # Populate the subnet treeview with information about the allocated subnets
        for i, subnet in enumerate(allocated_subnets):
            subnet_name = f"{i+1}"
            if i < len(self.subnet_name_entries) and self.subnet_name_entries[i].get():
                subnet_name = self.subnet_name_entries[i].get()
            needed_size = int(self.hosts_entries[i].get())
            allocated_size = subnet.num_addresses
            subnet_address = str(subnet.network_address)
            subnet_mask = f"/{subnet.prefixlen}"
            broadcast_address = str(subnet.broadcast_address)
            assignable_range = f"{subnet.network_address + 1} - {subnet.broadcast_address - 1}"
            self.subnet_treeview.insert("", "end", values=(subnet_name, needed_size, allocated_size, subnet_address, subnet_mask, broadcast_address, assignable_range))

    def warning_message(self, needed_hosts):
        # Create a new Toplevel window to display the warning message
        warning_window = tk.Toplevel(self)
        warning_window.title("Warning")
        
        # Create a label with the warning message text and pack it into the window
        warning_label = ttk.Label(warning_window, text=f"Not enough IP addresses to allocate {needed_hosts} hosts.")
        warning_label.pack(pady=5, padx=5)
        
        # Create a button to dismiss the warning window and pack it into the window
        warning_ok_button = ttk.Button(warning_window, text="OK", command=warning_window.destroy)
        warning_ok_button.pack(pady=5, padx=5)

    def error_message(self):
        # Create a new Toplevel window to display the error message
        error_window = tk.Toplevel(self)
        error_window.title("Error")
        
        # Create a label with the error message text and pack it into the window
        error_label = ttk.Label(error_window, text="Invalid IP address.")
        error_label.pack(pady=5, padx=5)
        
        # Create a button to dismiss the error window and pack it into the window
        error_ok_button = ttk.Button(error_window, text="OK", command=error_window.destroy)
        error_ok_button.pack(pady=5, padx=5)

    def create_subnets(self):
        # Get the number of subnets from the subnet entry box
        num_subnets = int(self.subnets_entry.get())

        # Get the current number of host entries
        current_num_entries = len(self.hosts_entries)

        # Create additional host entry fields as needed
        for i in range(current_num_entries, num_subnets):
            # Create a label for the subnet name entry field and grid it onto the GUI
            subnet_name_label = ttk.Label(self, text=f"Subnet {i+1} name:")
            subnet_name_label.grid(row=3 + i*2, column=0, pady=5, padx=5)
            self.subnet_name_labels.append(subnet_name_label)

            # Create a default subnet name using the alphabet
            subnet_name = chr(ord('A') + i % 26)
            subnet_name_entry = ttk.Entry(self)
            subnet_name_entry.insert(0, subnet_name)
            subnet_name_entry.grid(row=3 + i*2, column=1, pady=5, padx=5)
            self.subnet_name_entries.append(subnet_name_entry)

            # Create entry fields for the subnet name and hosts values and grid them onto the GUI
            host_label = ttk.Label(self, text=f"Hosts for subnet {i+1}:")
            host_label.grid(row=3 + i*2, column=2, pady=5, padx=5)
            self.hosts_labels.append(host_label)

            host_entry = ttk.Entry(self)
            host_entry.grid(row=3 + i*2, column=3, pady=5, padx=5)
            self.hosts_entries.append(host_entry)

        # Enable the "Calculate" button
        self.calculate_button.config(state="normal")

        # Remove any excess host entry fields
        for i in range(current_num_entries - num_subnets):
            subnet_name_label = self.subnet_name_labels.pop()
            subnet_name_label.destroy()

            host_label = self.hosts_labels.pop()
            host_label.destroy()

            host_entry = self.hosts_entries.pop()
            host_entry.destroy()

            subnet_name_entry = self.subnet_name_entries.pop()
            subnet_name_entry.destroy()





def main():
    app = SubnetCalculator()
    app.mainloop()

if __name__ == "__main__":
    main()