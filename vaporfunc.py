""" This file contains general functions used by vapor """

import numpy as np
import gzip
import random

def get_kmers(strings,k):
    """ Takes strings and returns a set of kmers """
    kmers = set()
    for string in strings:
        for i in range(len(string)-k+1):
            kmers.add(string[i:i+k])
    return kmers

def rev_comp(read):
    read = read.replace("T", "a")
    read = read.replace("A", "t")
    read = read.replace("C", "g")
    read = read.replace("G", "c")
    return read.upper()[::-1]

def parse_and_prefilter(fqs, dbkmers, threshold, k):
    """ Parses fastq files fqs, and filters them """
    c = 0
    M = float(len(dbkmers))
    seen = set()
    for fq in fqs:
        if fq.endswith(".gz"):
            f = gzip.open(fq,'rt')
        else:
            f = open(fq,'r')
        for line in f:
            if c == 1:
                tmpseq = line.strip()
                kcount = 0
                # Don't allow Ns in read
                # Don't allow reads < k
                if "N" not in tmpseq and len(tmpseq) >= k and tmpseq not in seen:
                    seen.add(tmpseq)
                    for i in range(0, len(tmpseq), k):
                        if tmpseq[i:i+k] in dbkmers:
                            kcount += 1
                    # Only allow reads with a given number of words in dbkmers
                    if k*kcount/M < threshold:
                        yield tmpseq
            c += 1                  
            if c == 4:
                c = 0
        f.close()

def parse_fasta_uniq(fasta, filter_Ns=True):
    """ Gets unique sequences from a fasta, with filtering of Ns"""
    tmph = ""
    tmps = ""
    hs = []
    ss = []
    sseen = set()
    with open(fasta) as f:
        for line in f:
            l = line.strip()
            if l[0] == ">":
                if tmps not in sseen:
                    if ((filter_Ns == True) and "N" not in tmps) or filter_Ns == False:
                        hs.append(tmph)
                        ss.append(tmps) 
                        sseen.add(tmps)
                tmph = l
                tmps = ""
            else:
                tmps += l
    hs.append(tmph)
    ss.append(tmps)
    return hs, ss 

def subsample(reads, n):
    """ Takes a sample of n from reads """
    if n >= len(reads):
        return reads
    else:
        return random.sample(reads, n)


