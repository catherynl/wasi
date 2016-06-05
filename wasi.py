import csv

age_yr = input("Age in years: ")
age_mo = input("+ months: ")
vc_raw = input("Raw vocab score: ")
mr_raw = input("Raw matrix score: ")

if not (10 <= age_yr <= 14 and 0 <= age_mo <= 11 and 0 <= vc_raw <= 53 and 0 <= mr_raw <= 30): 
    raise Exception('Invalid input')

print "Computing results..."

'''Compute T score for vocab section'''

vc_t_scores = []

vc_file = open('vc.csv', 'r')
vc_reader = csv.reader(vc_file)
years = map(int, vc_reader.next()[1:])
begin_month = map(int, vc_reader.next()[1:])
end_month = map(int, vc_reader.next()[1:])
headers = zip(years, begin_month, end_month)
indices = dict()

for i in range(len(headers)):
    indices[headers[i]] = i

for row in vc_reader:
    vc_t_scores.append(map(int, row[1:]))
vc_file.close()

index = 0
for age in indices:
    if age_yr == age[0] and age_mo >= age[1] and age_mo <= age[2]:
        index = indices[age]

vc_t_score = vc_t_scores[vc_raw][index]
print "Vocab T score:", vc_t_score

'''Compute T score for matrix section'''

mr_t_scores = []

mr_file = open('mr.csv', 'r')
mr_reader = csv.reader(mr_file)
for i in range(3): # skip first three rows
    mr_reader.next()
    indices[headers[i]] = i

for row in mr_reader:
    mr_t_scores.append(map(int, row[1:]))
mr_file.close()

mr_t_score = mr_t_scores[mr_raw][index]
print "Matrix T score:", mr_t_score

'''Compute overall T score and WASI IQ'''
sum_t_score = vc_t_score + mr_t_score
print "T score sum: ", sum_t_score

iq_scores = dict()
percentiles = dict()

iq_file = open('iq.csv', 'r')
iq_reader = csv.reader(iq_file)
header = iq_reader.next()

for t, iq, perc in iq_reader:
    # print t, iq, float(perc)
    iq_scores[int(t)] = int(iq)
    percentiles[int(t)] = float(perc)
iq_file.close()

print "IQ equivalent: ", iq_scores[sum_t_score]
print "Percentile: %.1f" % percentiles[sum_t_score] + "%"

