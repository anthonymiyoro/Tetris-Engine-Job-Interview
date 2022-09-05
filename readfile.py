# input_list = []

# with open('inputs.txt', "r", encoding='utf8') as f:
#     for line in f:
#         clean_line = (line.strip())
#         print (clean_line)
#         input_list = input_list.append(clean_line)
#         print(input_list)
        
# print(input_list)
file1 = open('inputs.txt', 'r')
Lines = file1.readlines()

for idx, item in enumerate(Lines): # Remove \n
   if '\n' in item:
       item = (item.strip())
       Lines[idx] = item

print (Lines)