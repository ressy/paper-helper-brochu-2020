#!/usr/bin/env python

"""Convert CDS info from GBF to CSV."""

import sys
import csv
from Bio import SeqIO

# id (looks like accession with version)
# name (looks like accession without version)
# gbf.annotations["accessions"][0] (also looks like accession?)
# description
# CDS features have a bunch of features including sometimes a note about the hinge region
# Looks like every GBF has one CDS feature.

def convert_gbf(fp_out, fps_in):
    """Convert CDS info from GBF to CSV.

    fp_out: single path to CSV output
    fps_in: list of paths for GBF input
    """
    rows = []
    for fp_in in fps_in:
        with open(fp_in) as f_in:
            for gbf in SeqIO.parse(f_in, "gb"):
                for feature in gbf.features:
                    if feature.type == "CDS":
                        cds_attrs = feature.qualifiers
                        break
                else:
                    feature = None
                    cds_attrs = {}
                get = lambda key: ";".join(cds_attrs.get(key, []))
                row = {
                    "Gene": get("gene"),
                    "Accession": gbf.id,
                    "Description": gbf.description,
                    "Note": get("note"),
                    "CodonStart": get("codon_start"),
                    "Product": get("product"),
                    "ProteinID": get("protein_id"),
                    "Seq": str(gbf.seq),
                    "SeqCDS": str(feature.extract(gbf.seq)),
                    "SeqAA": get("translation")}
                rows.append(row)
    with open(fp_out, "wt") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    convert_gbf(sys.argv[1], sys.argv[2:])
