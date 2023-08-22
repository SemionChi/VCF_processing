# VCF Processing Project

This project focuses on processing Variant Call Format (VCF) files, which contain information about genetic variants (mutations) within genetic samples. The goal is to develop a codebase that reads a VCF file, performs various operations based on user-defined parameters, and produces split output files. The project emphasizes meeting specified requirements while offering opportunities for additional functionality.

## Table of Contents
- [Assignment Details](#assignment-details)
- [Usage](#usage)
- [Must-Have Requirements](#must-have-requirements)
- [Nice-to-Have Extra Requirements](#nice-to-have-extra-requirements)
- [Bonus Question](#bonus-question)

## Assignment Details

The assignment involves creating a code project that processes a VCF file by performing certain tasks based on provided parameters. The processed data is then separated into different output files. The code can utilize various technologies, languages, or external tools, as long as it meets the specified requirements.

## Usage

To use this project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/SemionChi/VCF_processing
   cd vcf_processing

2. Install the required dependencies (if applicable).
   ```bash
     pip install -r requirements.txt
     ```
3. Run the main script with the desired parameters:

   ```bash
   python main_.py --start <start_value> --end <end_value> --minDP <minDP_value> limit <limit_value>
   ```
   
     ex: 
       ```bash
        python main.py 8 --minDP 120
        ```
     
   limit variable does not require the arguments name, "--limit" is not required in the run command
  
4. Run the classification script:

   ```bash
   python classification.py
   ```

## Must-Have Requirements

- [x] 1. The code should accept three optional parameters (`start`, `end`, `minDP`) and one mandatory parameter (`limit`).
- [x] 2. The VCF content should be read from the specified AWS S3 path (`s3://resources.genoox.com/homeAssingment/demo_vcf_multisample.vcf.gz`).
- [x] 3. For each sample in the VCF:
   - Create a new VCF file named `<SAMPLE>_filtered.vcf`.
   - Include the original VCF header.
   - Include the VCF column line for the relevant sample.
   - Include variant lines that meet the criteria: POS between `start` and `end`, and DP > `minDP`.
   - Add a new subfield named `GENE` in the INFO column, obtained via the `fetch_variant_details` API.
   - Stop processing after reaching the `limit` lines or end of VCF file.

## Nice-to-Have Extra Requirements

- [x] 1. Process the input VCF without persisting it to disk (zipped or extracted).
- [x] 2. Implement caching for API responses to prevent redundant queries.
- [ ] 3. Provide a mechanism to resume processing from where it left off after a crash.


## Bonus Question

- [x] Develop a classification logic to categorize variants from `<SAMPLE>_filtered.vcf` files. Apply the following logic and save results to `<SAMPLE>_classified.vcf`:
- If the difference between the length of REF and ALT is not divisible by 3, classify the variant as PATHOGENIC.
- Otherwise, classify it as BENIGN.

Result example:
```bash
   #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	father	mother	proband

chr12	67147	.	CT	C	31.8	.	FS=0;MQ=34.22;MQRankSum=0.05;QD=1.51;ReadPosRankSum=0.854;SOR=0.693;FractionInformativeReads=1;DP=21;AF=0.5;AN=2;AC=1;GENE=FAM138D;CLASSIFICATION=PATHOGENIC;	GT:AD:AF:DP:GQ:PL:SB	./.:.:.:.:.:.:.	./.:.:.:.:.:.:.	0/1:18,3:0.143:21:72:72,0,1180:7,11,1,2
chr12	67149	.	T	A	43.55	.	FS=0;MQ=34.22;MQRankSum=-0.151;QD=2.07;ReadPosRankSum=0.854;SOR=0.693;FractionInformativeReads=1;DP=21;AF=0.5;AN=2;AC=1;GENE=FAM138D;CLASSIFICATION=BENGIN;	GT:AD:AF:DP:GQ:PL:SB	./.:.:.:.:.:.:.	./.:.:.:.:.:.:.	0/1:18,3:0.143:21:72:72,0,1180:7,11,1,2
```
