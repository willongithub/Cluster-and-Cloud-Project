cd to current path (like xxx/Ansible)
run command "bash ansible.sh"
then everything is executed automatically

PLEASE NOTE!
Sometimes the script will go wrong when accessing remote computers at first time (they would ask you to type "yes" to confirm your authentication, which could make current execution fail). However, it is not a big problem. JUST run "bash ansible.sh" again after current spcript is done. The second turn of running script will set up the system successfully with no extra influence.

About IP:
This script uses fixed IP (4 vms given to our team). So if you want to use other vm (which means different IP), you should modify such files : hosts, vm.args, local.ini and connect.sh. However, nothing needs to be changed when using our vms.
