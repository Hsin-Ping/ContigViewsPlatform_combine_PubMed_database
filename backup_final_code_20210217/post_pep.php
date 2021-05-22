<?php
 $result=$_POST['all_data_t'];
#time_stamp
 $params=microtime(true);
 $temp_folder="/nfs/data1/NGStools/cache/BlastToLandmark/".$params;
#creat_a_folder_named_by_time_stamp 
 $mkdir=mkdir($temp_folder,0777,true);
 $file=fopen($temp_folder."/"."pep_for_blastp.fasta","w+");
#write_fasta_into_file 
 fwrite($file,$result);
 fclose($file);
#call_scp_to_114.py
 $path="python scp_to_114.py ";
 #echo "Done."."\n";
 passthru($path.$params);
 echo "Total use time: ".(microtime(true)-$params)."\n";
#print_time_stamp_for_javascript
 echo "params:$params";
?>
