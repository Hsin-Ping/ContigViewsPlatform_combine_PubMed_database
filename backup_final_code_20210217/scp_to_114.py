import os
import sys
import paramiko
import time
#get_time_stamp_file
params=sys.argv[1]
#build ssh object
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#IP_path_sshpass
IP_120="root@140.112.165.120:"
path_120="/nfs/data1/NGStools/cache/BlastToLandmark/"
path_114="/temp_folder/"
pwd="sshpass -p 'server@ntutrag' scp -r "
#connect to server
ssh.connect(hostname = '140.112.105.114',port = 22,username='root',password='server@ntutrag')
#scp_folder_from_120_to_114
stdin, stdout, stderr =ssh.exec_command(pwd+IP_120+path_120+params+" "+path_114)
stdout.read()
#rm_folder_in_120
os.system("rm -rf "+path_120+params)
b_start=time.time()
#do_blastp_and_sort_blastp_result_in_114
stdin, stdout, stderr =ssh.exec_command("cd "+path_114+params+"/ && blastp -db /data/db/landmark/landmark -query pep_for_blastp.fasta -max_target_seqs 30 -num_threads 5 -evalue 1e-10 -outfmt '6 qaccver saccver stitle staxids evalue pident bitscore score' -out blastp_result.txt && Rscript ../sort_only.R")
#rm_all_blank_in_ouput
data = stdout.read().strip()
print "blastp_time: "+str(time.time()-b_start)
#split_data_by_"] "_and_get_second_element_and_save_as_besthits
besthits=data.split("] ")[1]
##print "Best hits: "+besthits
#paht_of_edirect_command
e_path="/tools/edirect/"
#do_edirect_in_114_and_save_result_as_ref.txt
e_start=time.time()
stdin, stdout, stderr =ssh.exec_command("cd "+path_114+params+" && "+e_path+"epost -db gene -id "+besthits+" -format acc | "+e_path+"elink -target pubmed | "+e_path+"esummary | "+e_path+"xtract -pattern DocumentSummary -element Id PubDate Title > ref.txt &")
stdout.read()
print "edirect_time: "+str(time.time()-e_start)
#scp_folder_in_114_back_to_120_then_rm_folder_in_114
stdin, stdout, stderr =ssh.exec_command(pwd+path_114+params+" "+IP_120+path_120+" && rm -rf "+path_114+params)
stdout.read()
ssh.close()
#count_paper_number
cc=os.popen("wc -l "+path_120+params+"/ref.txt")
counts=cc.read().split(" ")[0]
print "Total count of paper: "+counts


