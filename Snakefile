from csv import DictReader
from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider

HTTP = HTTPRemoteProvider()

wildcard_constraints:
    acc="[A-Z]{2}[0-9]+"

with open("from-paper/genbank_accessions.txt") as f_in:
    GB_ACCESSIONS = [line.strip() for line in f_in]

with open("metadata/zenodo.csv") as f_in:
    ZENODO_URLS = [row["URL"] for row in DictReader(f_in)]

GBF = expand("from-genbank/{acc}.gbf", acc=GB_ACCESSIONS)

rule gbf_to_csv:
    """Aggregate the separate GBF files into one CSV, one row per CDS."""
    output: "output/genes.csv"
    input: GBF
    shell: "python scripts/gbf_to_csv_cds.py {output} {input}"

rule download_gbf:
    """Download one GBF text file per GenBank accession."""
    output: "from-genbank/{acc}.gbf"
    shell: "python scripts/download_genbank.py {wildcards.acc} gb > {output}"

rule download_zenodo_all:
    input: expand("from-zenodo/{file}", file=[re.sub(".*/", "", url) for url in ZENODO_URLS])

rule download_zenodo:
    """Download a file from the Zenodo dataset."""
    output: "from-zenodo/{file}"
    input: HTTP.remote("https://zenodo.org/record/3634899/files/{file}")
    shell: "cp {input} {output}"
