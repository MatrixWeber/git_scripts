#!/bin/bash  
   
workspace_dirs=( 
    '/home/z002wydr/workspace/pluscontrol'
    '/home/z002wydr/workspace/pluscontrol_master'
    '/home/z002wydr/workspace/pluscontrol_master_merge'
    '/home/z002wydr/workspace/pluscontrol_feature'
    '/home/z002wydr/workspace/pluscontrol_bugfix'
    '/home/z002wydr/workspace/pluscontrol_devel'
)  
  
for dir in "${workspace_dirs[@]}"; do  
    if [ -d "$dir" ]; then  
        echo "fetch --all $dir"  
        cd "$dir"  
        git fetch --all  
    else  
        echo "Directory: '$dir' not available. Continue."  
    fi  
done  
