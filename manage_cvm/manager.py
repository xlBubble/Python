# -*- coding: utf-8 -*-
import sys
import json
import create
import clean

#get params from command line

def get_comm(params):
    if len(params) != 2:
        print ("error:invalid params. usage: manange <create|clean>")
        exit (-1)
    if params[1] != "create" and params[1] != "clean":
        print ("error:invalid params. usage: manange <create|clean>")
        exit(-1)
    else:
        comm = params[1]
        return comm

def func():
    li = {"eqgq":"gqg","3j8fqh":"hi-hq9"}
    return li

#main()
def main():
    comm = get_comm(sys.argv)
    if comm == "create":
        create_info = create.create_main()
        #create_info = func()
        with open("cvm_list.txt", 'w') as f:
            json.dump(create_info, f)
    if comm == "clean":
        with open("cvm_list.txt", "r") as f:
            get_info = json.load(f)
        clean.clean_main(get_info)

if __name__ == "__main__":
        main()
