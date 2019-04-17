from Types import *

output = convert_R_J_type()
object = i_instructions()
I_output = object.translate()
output.update(I_output)

translated_text_lines = []

for i in range(0, output.__len__()):
    line = "MEMORY("
    line += str(i)
    line += ") := "
    line += '"'
    line += output[i]
    line += '" ;'
    #print(line)
    translated_text_lines.append(line)

#write on the file
with open('DataSegmant.txt', 'w') as file:
     file.write("#Translation of Data Segment" + "\n")
     for line in translated_data_lines:
         file.write(line + "\n")
with open('CodeSegmant.txt', 'w') as file:
    file.write("#Translation of Code Segment" + "\n")
    for line in translated_text_lines:
        file.write(line + "\n")