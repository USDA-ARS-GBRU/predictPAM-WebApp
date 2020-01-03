tempdir='/var/folders/52/rbrrfj5d369c35kd2xrktf3m0000gq/T/pamPredict_r_rlvys3'
gnbank = "Pseudomonas_aeruginosa_PAO1_107.gbk"
pamseq='ATCGA'
strand = 'forward'
threads = 1
targetlength = 25
get_fastas(gnbank, tempdir)
map_out = map_pam(tempdir, pamseq,threads,strand)
target_out = get_target(tempdir, map_out, targetlength, strand)
parse_target_out = parse_target(target_out,strand,seqlengthtopam=12)
dict(list(parse_target_out.items())[0:5])
fpt= filter_parse_target(parse_target_out, threads=1, levendistance=2)

rms_list=[]
for key_val in parse_target_out.keys():
    rms_list.append(parse_target_out[key_val]['remainingseq'])
    
# initialize a new index
ref_index = create_index(rms_list)

# Find knn of 1 for each remaning seq
filter_parse_dict={}
filter_parse_dict2={}
n=1
for keys, value in parse_target_out.items():
    query_string = value['remainingseq']
    ids, distances = ref_index.knnQuery(query_string, k=2) ## k =number of k nearest neighbours (knn)
    if distances[1] > levendistance:
        filter_parse_dict[keys] = value



dict(list(target_out.items())[0:5])
# noet with dict 46 of target sequence were removed or less, non-unique [9673-9627
# parse key then create 12 bp and remanining part, also take care of strand specifictity
def parse_target(dictobject):
    newdict={}
    for items in dictobject.items():
        if items[1]['strand']=="+":
            close12 = items[0][-12:]
            remainingseq = items[0][:-12]
            items[1]['target'] = items[0] # move target sequence as value
            items[1]['remainingseq'] = remainingseq
            newdict[close12] = items[1] ## will retain only target with unique close12 bp
        if strand == "-":
            close12 = target_key[:12]
            remainingseq = target_key[12:]
            items[1]['target'] = items[0]
            items[1]['remainingseq'] = remainingseq
            newdict[close12] = items[1]
    return newdict
    
parse_target_out = parse_target(target_out)

dict(list(parse_target_out.items())[0:5])


## get unique in close12
import pickle
import numpy
import nmslib

def create_index(strings):
    index = nmslib.init(space='leven',
                            dtype=nmslib.DistType.INT,
                            data_type=nmslib.DataType.OBJECT_AS_STRING,
                            method='small_world_rand')
    index.addDataPointBatch(strings)
    index.createIndex(print_progress=True)
    return index
    
# initialize a new index
ref_index = create_index(list(parse_target_out.keys()))

ids, distances = ref_index.knnQuery(list(parse_target_out.keys())[0], k=1)


##
test_dict={}
for k, v in parse_target_out.items():
    ids, distances = ref_index.knnQuery(k, k=1) ## k =number of k nearest neighbours (knn)
    check_values= list(range(0, EDIT_DISTANCE + 1)) ## Levenshtein Distance greater than 2 is selected, less than 2 is considered as too similar -- maximizing specificity of target
    if distances not in check_values:
        test_dict[k] = v
    
    
    check = np.isin(distances, value) # if any element of value in the array, then True else False
    sum_check = np.sum(check) # If non present, all are false, hence sum == zero, else sum >=1
    if sum_check == 0 :
        test_dict[k] = v
        
dict(list(test_dict.items())[0:5])
    

aa = pd.DataFrame.from_dict(test_dict,orient='index')
aa = aa.head()
aa.reset_index(inplace=True)
bb=aa[['seqid', 'target_sp', 'target_ep', 'pam_seq', 'pam_start_ps',
'strand', 'target', 'remainingseq','index']]
bb.columns = ['seqid', 'target_sp', 'target_ep', 'pam_seq', 'pam_start_ps',
'strand', 'target', 'remainingseq','close12']
cc = bb.to_csv(index=False,sep='\t',header=False)
mapbed = BedTool(dict_to_pd_reorder_tab.splitlines())
n=1
for f in mapbed:
    print(n)
    n= n+1


    
    
aa = pd.DataFrame.from_dict(test_dict,orient='index')
aa.reset_index(inplace=True)
bb=aa[['seqid', 'target_sp', 'target_ep', 'pam_seq', 'pam_start_ps',
'strand', 'target', 'remainingseq','index']]
bb.columns = ['seqid', 'target_sp', 'target_ep', 'pam_seq', 'pam_start_ps',
'strand', 'target', 'remainingseq','close12']
bb.set_index("seqid", inplace=True)


aa.set_index("seqid", inplace=True)
bb=aa[['seqid ', 'target_sp', 'target_ep', 'pam_seq', 'pam_start_ps',
'strand', 'target', 'remainingseq','index']]
bb.columns = ['seqid ', 'target_sp', 'target_ep', 'pam_seq', 'pam_start_ps',
'strand', 'target', 'remainingseq','close12']
featurefile = os.path.join(tempdir, "features.txt")
mapbed = BedTool(bb.splitlines())
downstream = mapbed .closest(featurefile , d=True, fd=True, D="a", t="first")



genebank_file = SeqIO.parse(gnbank,"genbank")
for gene_record in genebank_file:
    for (item, f) in enumerate(gene_record.features):
        print(item)
        print(">>>>>>>>>>>>>>>>>>>>>>>>",f)
        
genebank_file = SeqIO.parse(gnbank,"genbank")
n=1
test={}
type_of_record = set()
for gene_record in genebank_file:
    for gene_feature in gene_record.features:
         type = gene_feature.type
         start = gene_feature.location.start.position
         stop = gene_feature.location.end.position
         test[n] = {"type":type , "start":start, "stop":stop}
         type_of_record.add(type)
         n=n+1

aa =  pd.DataFrame.from_dict(test,orient='index')
aa.to_csv("test.csv")



for gene_record in genebank_file:
    for gene_feature in gene_record.features:
        print(x)


        
        if gene_feature.type == 'gene':
            start = gene_feature.location.start.position
            stop = gene_feature.location.end.position
            accession = gene_record.id
            
def features_to_dataframe(recs):
    """Get genome records from a biopython features object into a dataframe
      returns a dataframe with a row for each cds/entry
      """
genebank_file = SeqIO.parse(gnbank,"genbank")
genome = genebank_file
#preprocess features
allfeat = []
test1={}
featureall=['location','type','id','qualifier','locus_tag','name']
featurekeys=('id','type','name','qualifier')
for gene_record in genebank_file:
        for (item, f) in enumerate(gene_record.features):
            print(item, f)
            x = f.__dict__
            q = f.qualifiers
            x.update(q)
            test1[item] = x
            d = {}
            d['start'] = f.location.start
            d['end'] = f.location.end
            d['strand'] = f.location.strand
            for i in featurekeys:
                if i in x:
                    if type(x[i]) is list:
                        d[i] = x[i][0]
                    else:
                        d[i] = x[i]
            allfeat.append(d)
            import pandas as pd
        df = pd.DataFrame(allfeat,columns=featurekeys)
        df['length'] = df.translation.astype('str').str.len()
        #print (df)
        df = check_tags(df)
        if cds == True:
            df = get_cds(df)
            df['order'] = range(1,len(df)+1)
        #print (df)
        if len(df) == 0:
            print ('ERROR: genbank file return empty data, check that the file contains protein sequences '\
                   'in the translation qualifier of each protein feature.' )
        return df
    
def embl_to_dataframe(infile, cds=False):
    recs = list(SeqIO.parse(infile,'embl'))
    df = features_to_dataframe(recs, cds)
    return df


k =11383
for k in test1.keys():
    entry = test1[k]
    


td = ['nepal']
x.update(td)

d[k].append(v)
    
dictionary['q'].append(5)
x['type'].append("trsr")
x.setdefault('type', []).append(td)




n=1
for keys, value in parse_dict.items():
    ids, distances = ref_index.knnQuery(keys, k=1)
    if distances > 2:
        print(ids, distances)
        print(n)
        n=n+1




    
    
    
d = {k:v for (k,v) in parse_dict.items() if v['remainingseq']}
    
    
    
    
    
    dist_tuple= ref_index.knnQueryBatch(rms_list,k=1,num_threads=threads)
    result = [i for i in dist_tuple if i[1] < 2]
    # query tuple for speed
    aa = list(parse_dict.values())
    # d = {k:v for (k,v) in d.items() if v > 2}
    d = {k: v for (k, v) in dist_tuple.iteritems() if v[0] < 5 and v[1] < 5}
    
    for rec in dist_tuple:
        # Retrive rec with Leven distance greater than user define eds (Levenshtein edit distance)
        if rec[1] > levendistance:
            result = [i for i in dist_tuple if i[1] > 3]
    
    
    for keys, value in parse_dict.items():
        ids, distances = ref_index.knnQuery(keys, k=1) ## k =number of k nearest neighbours (knn)

        ## Do this with less than operator
        check_values= list(range(0, EDIT_DISTANCE + 1)) ## Levenshtein Distance greater than 2 is selected, less than or equal to 2 is considered as too similar -- maximizing specificity of target
        # here distance is sort in ascending order
        if distances not in check_values:
            filter_parse_dict[keys] = value
    return filter_parse_dict
