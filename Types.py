from File_read_and_org import *
# code.
class R:
    dic_R = {"add": "100000", "and": "100100", "sub": "100010", "nor": "100111", "or": "100101", "slt": "101010"}
    R_opcode = "000000"
    R_shimt = "00000"

    def __init__(self, instruction, rs, rt, rd):
        self.funct = self.dic_R[instruction]
        self.rs = registers[rs]
        self.rt = registers[rt]
        self.rd = registers[rd]

    def convert(self):
        self.out = self.R_opcode
        self.out += self.rs
        self.out += self.rt
        self.out += self.rd
        self.out += self.R_shimt
        self.out += self.funct
        return self.out


output_r = {}

def convert_R_J_type():
    for address_R, line_R in ls_r.items():
        eline = line_R.replace(', ', ' ')
        nline = eline.replace("\n", "")
        splitted_R = nline.split(" ")
        instruction_ = splitted_R[0]
        rd_ = splitted_R[1]
        rs_ = splitted_R[2]
        rt_ = splitted_R[3]
        translate = R(instruction_, rs_, rt_, rd_)
        output_r[address_R] = translate.convert()

    for address_J, line_J in ls_j.items():
        splitted_J = line_J.split(" ")
        nnsplitted_J = splitted_J[1].replace("\n", "")
        nnsplitted_J += ":"
        Binary_J = "000010"  # J Opcode.
        Binary_J += str(bin(lable_text[nnsplitted_J])[2:].zfill(26))
        output_r[address_J] = Binary_J
    return output_r


out_dic = {}
op_dic = {"addi": "001000",
          "lw": "100011",
          "sw": "101011",
          "bne": "000101",
          "beq": "000100"}


class i_instructions:
    def translate(self):
        for key, x in ls_i.items():
            split_instruction = x.split(" ")
            if (split_instruction[0] == "addi"):
                split_code = split_instruction[1].split(",")
                self.str_op = op_dic.get(split_instruction[0])
                self.str_reg1 = registers.get(split_code[0])
                self.str_reg2 = registers.get(split_code[1])
                self.str_add_imd = bin(int(split_code[2]))[2:].zfill(16)  # [2:].zfill(16)
                our_format = self.str_op + self.str_reg1 + self.str_reg2 + self.str_add_imd

            elif (split_instruction[0] == "lw" or split_instruction[0] == "sw"):
                split_code = split_instruction[1].split(",")
                self.str_op = op_dic.get(split_instruction[0])
                self.str_reg1 = registers.get(split_code[0])
                split_offset = split_code[1].split("(")

                if (split_offset[0].isdigit()):
                    self.str_add_imd = bin(int(split_offset[0]))[2:].zfill(16)  # [2:].zfill(16)

                else:
                    split_offset[0] += ":"
                    obj = data_of_code()
                    obj = lable_data.get(split_offset[0])
                    self.str_add_imd = bin(obj.address*4)[2:].zfill(16)
                another_register = split_offset[1].replace(")", "")
                self.str_reg2 = registers.get(another_register)
                our_format = self.str_op + self.str_reg2 + self.str_reg1 + self.str_add_imd

            elif (split_instruction[0] == "beq" or split_instruction[0] == "bne"):
                split_code = split_instruction[1].split(",")
                self.str_op = op_dic.get(split_instruction[0])
                self.str_reg1 = registers.get(split_code[0])
                self.str_reg2 = registers.get(split_code[1])
                nkey = key+1  # current location +1
                nsplitc = split_code[2].replace("\n", "")
                nsplitc += ":"
                v = lable_text[nsplitc]  # target location
                if (v >= nkey):
                    self.str_add_imd = bin(v - nkey)[2:].zfill(16)
                else:
                    self.str_add_imd = bin((eval("0b" + str(
                        int(bin(v - nkey)[3:].zfill(16).replace("0", "2").replace("1", "0").replace("2", "1")))) + eval(
                        "0b1")))[2:].zfill(16)
                our_format = self.str_op + self.str_reg1 + self.str_reg2 + self.str_add_imd

            out_dic[key] = our_format
        return out_dic


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