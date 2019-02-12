import sys
import numpy as np
words = []
window = int(sys.argv[2])
unique_word = {}
unique_word_window = {}
la = np.linalg

def get_start_end(i):
	for temp in range(i, -1 ,-1):
		if temp-1<0 or temp-1<(i-window):
			start = temp
			break
	else: 
		start = 0
	for temp in range(i, i+window+1):
		if temp+1>len(words) or temp+1>(i+window):
			end = temp
			break
	else: 
		end = len(words)
	if end+1<=len(words):
		end += 1
	return start, end

def padding():
	for i in range(0,window):
		words.append('#')
	
# ----------xx- Program Starts from Here -xx-----------
padding()
with open(str(sys.argv[1])) as f:
	words_temp = f.read().lower().split()
	for i in words_temp:
		words.append(i)

padding()
# Lists and Counts Unique Words
for word in words:
	if word not in unique_word.keys():
		unique_word_window[word] = []
		unique_word[word] = 1
	else:
		unique_word[word] += 1

sorted_words_index = sorted(unique_word.keys())
sorted_words = {}

for i in sorted_words_index:
	if i not in sorted_words.keys() and i!='#':
		sorted_words[i] = []
		for j in sorted_words_index:
			sorted_words[i].append(0)

for i in range(window, len(words)):
	start, end = get_start_end(i)
	for j in range(start, end):
		if i!=j and words[i]!='#':
			sorted_words[words[i]][sorted_words_index.index(words[j])] += 1	
print("\n")	

# Normalize
temp = []
for i in sorted_words.keys():
	sum1 = sum(sorted_words[i])
	temp = []
	for j in sorted_words[i]:
		temp.append(j/sum1)
	sorted_words[i] = temp

for i in sorted_words.keys():
	del(sorted_words[i][0])

# Transfer elements to a matrix
vectors = list(sorted_words.values())

U, s, Vh = la.svd(vectors, full_matrices=False)

U = np.round(U, 5)
word2vec = U[:(2*window), :]
word2vec = word2vec.T

print(word2vec)
print('\n')
with open("out.txt", "w+") as f:
	for vector in word2vec:
		f.write('\t'.join(map(str, vector)) + '\n')
print("An \'out.txt\' file has been created")