import atexit
import sys
import sqlite3

import DTO
from Repository import *


def main(args):
    # the repository singleton
    repo = Repository(args)
    atexit.register(repo._close)
    repo.create_tables()  # create all tables needed
    with open(args[1]) as config:
        lines = config.readlines()
    numOfHats, numOfSuppliers = (lines[0].split(','))  # get number of hats and suppliers
    numOfSuppliers = numOfSuppliers.rstrip()

    for i in range(int(numOfHats)):  # create hats
        s = lines[i + 1].rstrip()
        line = s.split(',')
        print(line)
        repo.hats.insert(DTO.Hat(line[0], line[1], line[2], line[3]))

    for i in range(int(numOfSuppliers)):  # create suppliers
        s = lines[i + int(numOfHats) + 1].rstrip()
        line = s.split(',')
        repo.suppliers.insert(DTO.Supplier(line[0], line[1]))

    with open(args[2]) as orders:
        lines = orders.readlines()
        for i in range(len(lines)):
            s = lines[i].rstrip()
            line = s.split(',')
            location = line[0]
            this_topping = line[1]
            supp_id = repo.hats.find_supplier_with_lowest_id(topping=this_topping)
            allHats = repo.hats.find(topping=this_topping)
            thisHat = None
            for a in allHats:
                if a[2] == supp_id:
                    repo.hats.update({'quantity': max(0, a[3]-1)}, {'topping': this_topping, 'supplier': supp_id})
                    thisHat = a
                if a[3] == 1:
                    repo.hats.delete(id=a[0])
            repo.orders.insert(DTO.Order(i+1, location, thisHat[0]))
            supp_name = repo.suppliers.find(id=supp_id)[0][1]
            output = open(args[3], "a")
            output.write(this_topping + ',' + supp_name + ',' + location + '\n')


if __name__ == '__main__':
    main(sys.argv)
