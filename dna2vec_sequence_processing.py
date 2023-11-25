import itertools
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

def sentence2word(str_set):
    word_seq=[]
    for sr in str_set:
        tmp=[]
        for i in range(len(sr)-5):
            if('N' in sr[i:i+6]):
                tmp.append('null')
            else:
                tmp.append(sr[i:i+6])
        word_seq.append(' '.join(tmp))
    return word_seq

def word2num(wordseq,tokenizer,MAX_LEN):
    sequences = tokenizer.texts_to_sequences(wordseq)
    numseq = pad_sequences(sequences, maxlen=MAX_LEN)
    return numseq

def sentence2num(str_set,tokenizer,MAX_LEN):
    wordseq=sentence2word(str_set)
    numseq=word2num(wordseq,tokenizer,MAX_LEN)
    return numseq

def get_tokenizer():
    f= ['a','c','g','t']
    c = itertools.product(f,f,f,f,f,f)
    res=[]
    for i in c:
        temp=i[0]+i[1]+i[2]+i[3]+i[4]+i[5]
        res.append(temp)
    res=np.array(res)
    NB_WORDS = 4097
    tokenizer = Tokenizer(num_words=NB_WORDS)
    tokenizer.fit_on_texts(res)
    acgt_index = tokenizer.word_index
    acgt_index['null']=0
    return tokenizer

def get_data(enhancers,promoters):
    tokenizer=get_tokenizer()
    MAX_LEN=3000
    X_en=sentence2num(enhancers,tokenizer,MAX_LEN)
    MAX_LEN=2000
    X_pr=sentence2num(promoters,tokenizer,MAX_LEN)

    return X_en,X_pr


def getSubSeqs(org_seq,org_seq_len, step ,sub_seq_len):
    sub_seqs=[]
    # print(org_seq_len)
    for x in range (0,org_seq_len,step):
        # if x+sub_seq_len > org_seq_len:
        #     break
        kmer= org_seq[x:x+sub_seq_len]
        # print(x,":",x+sub_seq_len)
        # print(len(kmer))
        kmers = " ".join(kmer)
        sub_seqs.append(kmers)
    # print(sub_seqs)
    # print(len(sub_seqs))
    return sub_seqs

# In[ ]:


names = ['GM12878', 'HUVEC', 'HeLa-S3', 'IMR90', 'K562', 'NHEK']
name=names[1]
train_dir='./data/%s/train/'%name
test_dir='./data/%s/test/'%name
Data_dir='./data/%s/'%name

print ('Experiment on %s dataset' % name)

print ('Loading seq data...')
enhancers_tra=open(train_dir+'%s_enhancer.fasta'%name,'r').read().splitlines()[1::2]
promoters_tra=open(train_dir+'%s_promoter.fasta'%name,'r').read().splitlines()[1::2]
y_tra=np.loadtxt(train_dir+'%s_label.txt'%name)

enhancers_tes=open(test_dir+'%s_enhancer_test.fasta'%name,'r').read().splitlines()[1::2]
promoters_tes=open(test_dir+'%s_promoter_test.fasta'%name,'r').read().splitlines()[1::2]
y_tes=np.loadtxt(test_dir+'%s_label_test.txt'%name)

print('平衡训练集')
print('pos_samples:'+str(int(sum(y_tra))))
print('neg_samples:'+str(len(y_tra)-int(sum(y_tra))))

print('测试集')
print('pos_samples:'+str(int(sum(y_tes))))
print('neg_samples:'+str(len(y_tes)-int(sum(y_tes))))

X_en_tra,X_pr_tra=get_data(enhancers_tra,promoters_tra)
X_en_tes,X_pr_tes=get_data(enhancers_tes,promoters_tes)

np.savez(Data_dir+'%s_train.npz'%name,X_en_tra=X_en_tra,X_pr_tra=X_pr_tra,y_tra=y_tra)
np.savez(Data_dir+'%s_test.npz'%name,X_en_tes=X_en_tes,X_pr_tes=X_pr_tes,y_tes=y_tes)

