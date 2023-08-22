
import os
import re
from concurrent.futures import ThreadPoolExecutor
import time


def classify_variant(INFO,REF,ALT):
    length_difference = abs(len(REF) - len(ALT))
    time.sleep(1)
    if length_difference % 3 == 0:
        return f"{INFO};CLASSIFICATION=BENGIN;"

        # BENGIN
    else:
        # PATHOGENIC
        return f"{INFO};CLASSIFICATION=PATHOGENIC;"

def create_file(name,header,line):
    # Directory where you want to create the files
    output_directory = "classified_samples"

    # Create the directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    header = "\n".join(header)
    formatted_name = name.replace("./.:.:.:.:.:.:.", "")
    formatted_name = re.sub(r'[:/\\]', ' ', formatted_name)

    file_path = os.path.join(output_directory, f"{formatted_name}_classified.vcf")

    if os.path.exists(file_path):
        with open(file_path, "a") as file:
            file.write(line+"\n")
    else:
        with open(file_path, "w") as file:
            file.write(header+"\n")
            file.write(line+"\n")
    pass  


def process_vcf_line(line, header_lines, REF_index, ALT_index, father_index, mother_index, proband_index, INFO_index):
    fields = line.strip().split('\t')     
    sample=f"{fields[father_index]} {fields[mother_index]} {fields[proband_index]}"
    new_info = classify_variant(fields[INFO_index],fields[REF_index],fields[ALT_index])
    fields[INFO_index]=new_info
    new_line="\t".join(fields)
    create_file(sample,header_lines,new_line)
                            

def main():
    data_started = False
    folder_path = "filtered_samples"

    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):

        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    header_lines=[]
                    for line in file:
                        if line.startswith("#CHROM"):
                            header_lines.append(line)
                            header = line.strip().split('\t')
                            REF_index=header.index("REF")
                            ALT_index=header.index("ALT")
                            father_index = header.index("father")
                            mother_index = header.index("mother")
                            proband_index = header.index("proband")
                            INFO_index=header.index("INFO")
                            break
                        elif line.startswith('#'):
                            header_lines.append(line)
                    for line in file:
                        # Create a ThreadPoolExecutor to process lines in parallel
                            with ThreadPoolExecutor(max_workers=3) as executor:
                                executor.submit(process_vcf_line, line, header_lines, REF_index, ALT_index, father_index, mother_index, proband_index, INFO_index)

if __name__ == "__main__":
    main()