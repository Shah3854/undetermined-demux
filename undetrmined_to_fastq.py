import gzip
import argparse
import os

def demultiplex(r1_file, r2_file, samplesheet, output_dir, log_file):
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Read sample sheet
    samples = {}
    with open(samplesheet, "r") as f:
        for line in f:
            sample_id, index = line.strip().split("\t")
            samples[index] = sample_id

    # Initialize output files and log tracking
    output_files = {}
    log_data = []
    
    for index, sample in samples.items():
        r1_out_path = os.path.join(output_dir, f"{sample}_R1.fastq.gz")
        r2_out_path = os.path.join(output_dir, f"{sample}_R2.fastq.gz")
        output_files[index] = (gzip.open(r1_out_path, "wt"), gzip.open(r2_out_path, "wt"))
    
    # Open input FASTQ files
    with gzip.open(r1_file, "rt") as r1, gzip.open(r2_file, "rt") as r2:
        total_reads = 0
        assigned_reads = {sample: 0 for sample in samples.values()}

        while True:
            # Read FASTQ blocks
            r1_header = r1.readline().strip()
            r1_seq = r1.readline().strip()
            r1_plus = r1.readline().strip()
            r1_qual = r1.readline().strip()

            r2_header = r2.readline().strip()
            r2_seq = r2.readline().strip()
            r2_plus = r2.readline().strip()
            r2_qual = r2.readline().strip()

            if not r1_header or not r2_header:
                break  # Stop at EOF

            total_reads += 1

            # Match against sample indexes
            for index, sample in samples.items():
                if index in r1_header and index in r2_header:
                    r1_out, r2_out = output_files[index]
                    r1_out.write(f"{r1_header}\n{r1_seq}\n{r1_plus}\n{r1_qual}\n")
                    r2_out.write(f"{r2_header}\n{r2_seq}\n{r2_plus}\n{r2_qual}\n")
                    assigned_reads[sample] += 1
                    break  # Stop checking once matched

            # Live progress every 100,000 reads
            if total_reads % 100000 == 0:
                print(f"Processed {total_reads} reads...")

        print("\nDemultiplexing complete!\n")
        print(f"Total Reads Processed: {total_reads}\n")

    # Close output files
    for r1_out, r2_out in output_files.values():
        r1_out.close()
        r2_out.close()

    # Write logs
    with open(log_file, "w") as log:
        log.write("Sample_ID\tAssigned_Reads\n")
        for sample, count in assigned_reads.items():
            log.write(f"{sample}\t{count}\n")
            print(f"Sample {sample}: {count} reads assigned.")

    print(f"\nLogs saved to: {log_file}")

# Argument parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demultiplex undetermined FASTQ files.")
    parser.add_argument("-uR1", required=True, help="Path to Undetermined R1 FASTQ.gz file")
    parser.add_argument("-uR2", required=True, help="Path to Undetermined R2 FASTQ.gz file")
    parser.add_argument("-s", required=True, help="Path to samplesheet TSV file")
    parser.add_argument("-o", required=True, help="Output directory for demultiplexed FASTQ files")
    parser.add_argument("-l", required=True, help="Log file path")

    args = parser.parse_args()
    
    # Run demultiplexing
    demultiplex(args.uR1, args.uR2, args.s, args.o, args.l)
