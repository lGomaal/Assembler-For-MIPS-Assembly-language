list_R_name= ["add","and","sub","nor","or","slt"]
list_I_name= ["addi","lw","sw","beq","bne"]
j_type="j"
registers = {
    "$zero": "00000",
    "$at": "00001",
    "$v0": "00010",
    "$v1": "00011",
    "$a0": "00100",
    "$a1": "00101",
    "$a2": "00110",
    "$a3": "00111",
    "$t0": "01000",
    "$t1": "01001",
    "$t2": "01010",
    "$t3": "01011",
    "$t4": "01100",
    "$t5": "01101",
    "$t6": "01110",
    "$t7": "01111",
    "$s0": "10000",
    "$s1": "10001",
    "$s2": "10010",
    "$s3": "10011",
    "$s4": "10100",
    "$s5": "10101",
    "$s6": "10110",
    "$s7": "10111",
    "$t8": "11000",
    "$t9": "11001",
    "$k0": "11010",
    "$k1": "11011",
    "$gp": "11100",
    "$sp": "11101",
    "$fp": "11110",
    "$ra": "11111"
}
ls_r = {}
ls_i={}
ls_j={}
lable_text={}
lable_data = {}
ls_data=[]
translated_data_lines=[]

class data_of_code:
    def __init__(self):
        self.address =-1
        self.type=""
        self.values=[]

def split (line):
    ls_of_sapratied_line=[]
    cheak_char=False
    copy_String=""
    for i in range (0,len(line)):
        if line[i]=="#" or line[i]=="\n":
            break
        if line[i]==' ':
            if cheak_char==True:
                ls_of_sapratied_line.append(copy_String)
                copy_String=""
                cheak_char=False
            else:
                cheak_char=False
                continue
        else:
            cheak_char=True
            copy_String+=line[i]
    if cheak_char==True:
        ls_of_sapratied_line.append(copy_String)
    return  ls_of_sapratied_line


def read_file():
    data = False
    text = False
    counter_data = 0
    counter_text = 0
    with open('Code.txt', 'r') as file:
        for line in file:
            if line[0]=='#':
                continue
            inst_ls = split(line)
            #print(inst_ls)
            if len(inst_ls)==0:
                continue
            st = inst_ls[0]
            if st == ".data":
                data=True
                continue
            if st == ".text":
                data=False
                text=True
                continue
            if text ==True:
                if st[-1]==':':
                    lable_text[st]=counter_text
                    if list_R_name.__contains__(inst_ls[1]):
                        instruc = inst_ls[1] + " " + inst_ls[2] + " " + inst_ls[3]+" "+inst_ls[4]
                        #print(instruc)
                        ls_r[counter_text]=instruc
                    elif list_I_name.__contains__(inst_ls[1]):
                        if inst_ls[3].__contains__('('):
                            instruc = inst_ls[1] + " " + inst_ls[2] + inst_ls[3]
                        else:
                            instruc = inst_ls[1] + " " + inst_ls[2] +inst_ls[3]+inst_ls[4]
                        ls_i[counter_text]=instruc
                    elif j_type == inst_ls[1]:
                        instruc = inst_ls[1] + " " + inst_ls[2]
                        #print(inst_ls[2])
                        ls_j[counter_text] = instruc
                else:
                    if list_R_name.__contains__(inst_ls[0]):
                        instruc = inst_ls[0] + " " + inst_ls[1] + " " + inst_ls[2] + " " + inst_ls[3]
                        ls_r[counter_text] = instruc
                    elif list_I_name.__contains__(inst_ls[0]):
                        if inst_ls[2].__contains__('('):
                            instruc = inst_ls[0] + " " + inst_ls[1] +inst_ls[2]
                        else:
                            instruc = inst_ls[0] + " " + inst_ls[1] +inst_ls[2]+inst_ls[3]
                        ls_i[counter_text] = instruc
                    elif j_type == inst_ls[0]:
                        instruc = inst_ls[0] + " " + inst_ls[1]
                        #print(inst_ls[1])
                        ls_j[counter_text] = instruc

                counter_text += 1
            if data == True:
                if st[-1]==':':
                    temp_da = data_of_code()
                    temp_val = inst_ls[2]
                    #print(inst_ls[1],inst_ls[2])
                    if inst_ls[1]==".space":
                        counter_data = counter_data + int(temp_val)
                        temp_da.address = counter_data- int(temp_val)
                        temp_da.type = inst_ls[1]
                        temp_da.values.append(int(temp_val))
                        lable_data[inst_ls[0]] = temp_da
                        continue
                    if inst_ls[1] ==".word":
                        ls_temp_val = temp_val.split(",")
                        if ls_temp_val.__len__()>1:
                            temp_da.address = counter_data
                            for i in range(0,len(ls_temp_val)):
                                temp_da.values.append(int(ls_temp_val[i]))
                                counter_data+=1
                            temp_da.type = inst_ls[1]
                            lable_data[inst_ls[0]] = temp_da
                        else:
                            temp_da.values.append(int(temp_val))
                            temp_da.address = counter_data
                            temp_da.type = inst_ls[1]
                            lable_data[inst_ls[0]] = temp_da
                            counter_data+=1
                            continue
    '''for s in ls_i:
        print(ls_i[s], s)
    for s in ls_r:
        print(ls_r[s], s)
    for s in ls_j:
        print(ls_j[s], s)
    for s in lable_text:
        print(s, lable_text[s])
    for s in lable_data:
        print(s, lable_data[s].address, lable_data[s].values, lable_data[s].type)'''




def memory_display ():
    count_data=0;
    for key_mem , val_mem in lable_data.items():
        if val_mem.type==".space":
            out=""
            size_of_space=val_mem.values[0]
            for i in range(size_of_space):
                for j in range (32):
                    out+="X"
                last=""
                last+="MEMORY"
                last+='('
                last+=str(count_data)
                last+=')'
                last+= " <= "+'"'+out+'"'
                last+=" ;"
                #print(last)
                translated_data_lines.append(last)
                out=""
                count_data+=1

        elif val_mem.type==".word":
            for val in val_mem.values:
                out=""
                val_bin =str(bin(val)[2:].zfill(32))
                out += "MEMORY"
                out += '('
                out += str(count_data)
                out += ')'
                out += " <= "+'"' + val_bin +'"'+ " ;"
                translated_data_lines.append(out)
                #print(out)
                count_data+=1
read_file()
memory_display()
