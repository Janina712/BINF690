# Sequence Module to be inherited by fasta and fastq modules
class Sequence():
    """
    Sequence base class
    """
    def __init__(self, id, seq, info=None, quality=None):
        self.id = id
        self.seq = seq
        self.info = info
        self.quality = quality

    def organize_Seq(id, seq, info=None, quality=None):
        bits = id.split(" ")  # split by spaces
        seq_id = bits[0][1:]  # ID is everything from @ to first space
        seq_header = " ".join(bits[1:])  # join for full sequence header
        if info is None:
            fasta = {}
            fasta[seq_id] = {"seq_id": seq_id, "seq_header": seq_header, "seq": seq}
            return fasta
        else:
            fastq = {}
            fastq[seq_id] = {"seq_id": seq_id, "seq_header": seq_header, "seq": seq, "info": info, "quality": quality}
            return fastq

    def get_GC_content(read_file):
        percent_gc = []
        percent_gc_avg = 0
        for k in range(0, len(read_file)):
            id = list(read_file[k].keys())[0]
            seq = read_file[k][id]['seq']
            seq = str(seq)
            percent_gc_current = (seq.count("G") + seq.count("C")) / (len(seq) / 100)
            percent_gc.append(percent_gc_current)
        percent_gc_avg = sum(percent_gc)/len(read_file)
        return percent_gc, percent_gc_avg

    def get_Seq_length(read_file):
        lengths = [] 
        for k in range(0, len(read_file)):
            id = list(read_file[k].keys())[0]
            seq = read_file[k][id]['seq']
            seq = str(seq)
            length = len(seq)
            lengths.append(length)
        return lengths

