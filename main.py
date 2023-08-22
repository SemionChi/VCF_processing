import argparse
import requests
import gzip
import os
import re
from api_request import get_variant_gene
from io import BytesIO


def verify_DP(input_string, minDP):
    if minDP is None:
        return True
    else:
        pattern = "DP=([^;]+)"
        match = re.search(pattern, input_string)
        if match and int(match.group(1)) > minDP:
            return True
        else:
            return None


def is_between(value, lower_bound, upper_bound):
    if lower_bound is None and upper_bound is None:
        return True  # Both bounds are None, so there's no valid range.
    elif lower_bound is None:
        return value <= upper_bound
    elif upper_bound is None:
        return value >= lower_bound
    else:
        return lower_bound <= value <= upper_bound


def create_file(name, header, line):
    # Directory where you want to create the files
    output_directory = "filtered_samples"

    os.makedirs(output_directory, exist_ok=True)

    header = "\n".join(header)
    formatted_name = name.replace("./.:.:.:.:.:.:.", "")
    formatted_name = re.sub(r'[:/\\]', ' ', formatted_name)

    file_path = os.path.join(output_directory, f"{formatted_name}_filtered.vcf")

    if os.path.exists(file_path):
        with open(file_path, "a") as file:
            file.write(line + "\n")
    else:
        with open(file_path, "w") as file:
            file.write(header + "\n")
            file.write(line + "\n")
    pass


def parse_vcf_arguments():
    parser = argparse.ArgumentParser(description="Process a VCF file and split it into different output files.")

    # Mandatory parameter
    parser.add_argument("limit", type=int, help="Limit parameter (must be an int < 10)")

    # Optional parameters
    parser.add_argument("--start", type=int, help="Start parameter")
    parser.add_argument("--end", type=int, help="End parameter")
    parser.add_argument("--minDP", type=int, help="minDP parameter")

    args = parser.parse_args()

    # Validate limit parameter
    if args.limit >= 10 or args.limit < 0:
        parser.error("Limit must be an integer less than 10.")

    return args


def process_vcf_line(line, header_lines, CHROM_index, REF_index, ALT_index, father_index, mother_index, proband_index,
                     POS_index, INFO_index, start, end, minDP):
    fields = line.strip().split('\t')
    if is_between(int(fields[POS_index]), start, end):
        if verify_DP(fields[INFO_index], minDP):
            sample = f"{fields[father_index]} {fields[mother_index]} {fields[proband_index]}"
            new_info = f"{fields[INFO_index]};GENE={get_variant_gene(fields[CHROM_index], int(fields[POS_index]), fields[REF_index], fields[ALT_index], 'hg19')}"
            fields[INFO_index] = new_info
            new_line = "\t".join(fields)
            create_file(sample, header_lines, new_line)


def main():
    args = parse_vcf_arguments()

    print("Parsed parameters:")
    print(f"Limit: {args.limit}")
    print(f"Start: {args.start}")
    print(f"End: {args.end}")
    print(f"minDP: {args.minDP}")

    # URL of the gzipped VCF file
    url = "https://s3.amazonaws.com/resources.genoox.com/homeAssingment/demo_vcf_multisample.vcf.gz"
    response = requests.get(url, stream=True)

    header_lines = []
    if response.status_code == 200:
        # Create a stream to read the gzipped content
        compressed_stream = BytesIO(response.content)
        with gzip.GzipFile(fileobj=compressed_stream, mode='rb') as gzipped_file:

            for line in gzipped_file:
                line = line.decode('utf-8').rstrip()
                if line.startswith("#CHROM"):
                    header_lines.append(line)
                    header = line.strip().split('\t')
                    CHROM_index = header.index("#CHROM")
                    REF_index = header.index("REF")
                    ALT_index = header.index("ALT")
                    father_index = header.index("father")
                    mother_index = header.index("mother")
                    proband_index = header.index("proband")
                    POS_index = header.index("POS")
                    INFO_index = header.index("INFO")
                    break
                elif line.startswith('#'):
                    header_lines.append(line)
            for line in gzipped_file:
                line = line.decode('utf-8').rstrip()
                process_vcf_line(line, header_lines, CHROM_index, REF_index, ALT_index, father_index, mother_index,
                                 proband_index, POS_index, INFO_index, args.start, args.end, args.minDP)

    else:
        print("Failed to download the file:", response.status_code)

    print("Finished successfuly")


if __name__ == "__main__":
    main()
