# undetermined-demux

## Overview
**undetermined-demux** is a Python tool for demultiplexing undetermined FASTQ files based on a sample sheet. It extracts reads matching sample indexes and saves them into separate FASTQ files for each sample.

## Features
- Handles paired-end FASTQ files (R1 and R2)
- Reads a sample sheet with sample names and indexes
- Writes output files in a specified directory
- Provides real-time terminal logging
- Compressed output in `.fastq.gz` format

## Requirements
- Python 3
- gzip (Python standard library)

## Installation
Clone the repository:
```bash
git clone https://github.com/Shah3854/undetermined-demux.git
cd undetermined-demux
```

## Usage
Run the script with the following command:
```bash
python undetermined_to_fastq.py -uR1 <Undetermined_R1.fastq.gz> -uR2 <Undetermined_R2.fastq.gz> -s <samplesheet.tsv> -o <output_directory>
```

### Arguments:
| Argument | Description |
|----------|-------------|
| `-uR1` | Path to the Undetermined R1 FASTQ file |
| `-uR2` | Path to the Undetermined R2 FASTQ file |
| `-s` | Path to the sample sheet (TSV format) |
| `-o` | Output directory for demultiplexed files |

### Example:
```bash
python undetermined_to_fastq.py -uR1 /path/to/Undetermined_S0_R1_001.fastq.gz \
                                -uR2 /path/to/Undetermined_S0_R2_001.fastq.gz \
                                -s /path/to/samplesheet.tsv \
                                -o /path/to/output_directory
```

## Sample Sheet Format
The sample sheet should be a tab-separated file (`.tsv`) with the following format:
```
Sample_1   TAAGGCGAAT+ATAGAGAGGT
Sample_2   CGTACTAGAT+ATAGAGAGGT
```

## Output
Demultiplexed FASTQ files are saved in the specified output directory with the following naming format:
```
output_directory/
    Sample_1.R1.fastq.gz
    Sample_1.R2.fastq.gz
    Sample_2.R1.fastq.gz
    Sample_2.R2.fastq.gz
```

## Logging
The script provides real-time logging in the terminal, displaying processed samples and matches.

## License
MIT License
