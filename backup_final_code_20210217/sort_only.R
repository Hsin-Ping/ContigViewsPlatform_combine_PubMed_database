library(rapportools) ###for is.empty()
f_info=file.info("blastp_result.txt")
f_size=f_info$size ###calculate filesize
if(f_size!=0){   ###if_have_blastp_result
data = read.delim("blastp_result.txt", header=FALSE, col.names = c("qaccver","saccver","description","staxids","evalue","pident","bitscore","score"))
###grab_replicates
rm=which(duplicated(data$saccver))

###whem_have_replicates_situation
if(is.empty(rm)==FALSE){
  data=data[-rm,]
}
###grab_besthits_with_different_species
spe=unique(data$staxids)
r_by_spe=c()
for(i in spe){
  p=subset(data,staxids==i)
  pp=p[1,]
  r_by_spe=rbind(r_by_spe,pp)
}
###sort_data_by_bitscore
sort_r_by_spe=r_by_spe[sort(-r_by_spe$bitscore),]
##grab_best_three_data_information
best_3=sort_r_by_spe[1:3,c(2,3,5,6,7)]
best_3=best_3[complete.cases(best_3),]
write.table(best_3,"best3hits.txt",col.names=F,row.names=F,quote=F,sep="\t")
###grab_saccver_and_cbind_them
hits_all=c()
for(i in sort_r_by_spe$saccver){
  hit=i
  hits_all=cbind(hits_all,i)
     }
###grab_first_three_and_deal_with_the_situation_when_it_blast_to_less_then_3_species
hh=c()
if(length(hits_all)>3){
  hits3=hits_all[,1:3]
  for(i in hits3){
    h=i
    hh=paste(hh,h)
  }
}else{
  hits3=hits_all
  for(i in hits3){
    h=i
    hh=paste(hh,h)
  }
}

###rm_the_blank_at_head_and_tail
final=gsub("^\\s|\\s$","",hh)
print(final)}else{ 
system("touch best3hits.txt") ###and_if_noblastp_result_create_a_best3hits.txt_for_web_rebpage.phtml
print("") ###give_a_empty_for_scp_to_114.py_to_run_edirect_program
}
