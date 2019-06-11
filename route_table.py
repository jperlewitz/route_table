import argparse
import pickle


parser = argparse.ArgumentParser()
parser.add_argument("-a","--add",action='store_true',help="Add new route to route table")
parser.add_argument("-c","--check",action='store_true',help="Check if route is in route table")
args = parser.parse_args()


class Node:
    def __init__(self):
        self.right = None
	self.left = None


class routeObj:
    def __init__(self):
        self.root = Node()

    def _convert_ip_bin(self,prefix,mask):
        # Vars
        binarystr = ""
        # Convert IP addr to a contiguous binary str
        for oct in prefix.split("."):
            binarystr += format(int(oct),"08b")
        binarystr = binarystr[:int(mask)]
        return binarystr


    def add_new_route(self,route):
	# Vars
        node = self.root
        binarystr = ""
        mask = route.split("/")[1]
        prefix = route.split("/")[0]
        binarystr = self._convert_ip_bin(prefix,mask)

        # Update binary tree
        for i in range(len(binarystr)):
            if binarystr[i] == "1":
                if node.right == None:
                    node.right = Node()
                    node.right.bit= "1"
                node = node.right
            elif binarystr[i] == "0":
                if node.left == None:
                    node.left = Node()
                    node.left.bit= "0"
                node = node.left
      

    def find_longest_match(self,prefix):
        """
        In Table: 11000000.10101000.00001010.01
        Lookup:   11000000.10101000.00001010.10
	No Match
        """

        # Vars
        binarystr = self._convert_ip_bin(prefix,"32")
        node = self.root
        longest_match = ""

        for i in range(len(binarystr)):
            binchar = binarystr[i]
            if binchar == "1" and node.right != None:
                longest_match += "1"
                node = node.right
                continue
            elif binchar == "1" and node.left != None:
                return "Route not in table"
            elif binchar == "0" and node.left != None:
                longest_match += "0"
                node = node.left
                continue
            elif binchar== "0" and node.right != None:
                return "Route not in table"
            else:
                if i < 32:
                    longest_match += "0"*(32-i)
                longest_match = self._convert_bin_ip(longest_match)
                return "Longest IP match: {}/{}".format(longest_match,i)


    def _convert_bin_ip(self,binstr):
        ip = "{}.{}.{}.{}".format(str(int(binstr[:8],2)),
				  str(int(binstr[8:16],2)),
				  str(int(binstr[16:24],2)),
				  str(int(binstr[24:32],2)))
        return ip


def main():
	"""
	"""
	# Create route table obj
	# routeTable = routeObj()
	# Load saved route table
	routeTable = RW_mem("","read")

	# Add new route to table
	if args.add:
		while True:
			new_route = raw_input("Enter route with CIDR mask: ")
			routeTable.add_new_route(new_route)
			print "Route {} has been added to the table".format(new_route)
			print "\n"
			user_choice = get_user_choice("Would you like to add another route?")
			if user_choice == "1":
				continue
			else:
				break
		# Save route table with new addition(s)
		RW_mem(routeTable,"write")
	elif args.check:       
		ip_prefix = raw_input("Enter route to check: ")
		message = routeTable.find_longest_match(ip_prefix)
		print message
	print "Exiting Route Table"


def RW_mem(obj,action):
	"""
		Use JSON to serialize object to memory to save state
	"""

	if action == "write":
		with open('RouteTable', 'w') as outfile:  
			pickle.dump(obj, outfile)
			return
	elif action == "read":
		with open('RouteTable', 'r') as outfile:  
			obj =  pickle.load(outfile)
			return obj
		

def get_user_choice(message):
	"""
	"""
	while True:
		user_choice = raw_input("{}\n1) Yes\n2) No\nEnter Choice: ".format(message))
		if user_choice == "1" or user_choice == "2":
			return user_choice
		else:
			pass


if __name__ == '__main__':
	main()
