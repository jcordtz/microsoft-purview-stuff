echo
echo "Delete a collection in Purview"
echo "=============================="
echo

# creating default values
parent_collection_no_def=1

source init_purview.sh

echo "-------------------------------------------------------------------------"
echo
echo "This script will create a file that can be used to delete assets in a collection"
echo "It does not do the delete, this has to be done running the created file"
echo
echo "Note - after the script created has been (modified and) run the collection it self need to be delete"
echo "       from the Purview Portal"
echo
echo "Getting Purview Account"

if [ "$PURVIEW_NAME" == "" ]; then
   echo "The parameter PURVIEW_NAME must be set"
   echo 
   echo "Have you run \". ./init_purview.sh\""
   echo
   echo "Setup aborted"
   exit -1
fi

if [ "$AZURE_CLIENT_ID" == "" ]; then
   echo "The parameter AZURE_CLIENT_ID must be set"
   echo 
   echo "Have you run \". ./init_purview.sh\""
   echo
   echo "Setup aborted"
   exit -1
fi

if [ "$AZURE_CLIENT_SECRET" == "" ]; then
   echo "The parameter AZURE_CLIENT_SECRET must be set"
   echo 
   echo "Have you run \". ./init_purview.sh\""
   echo
   echo "Setup aborted"
   exit -1
fi


if [ "$AZURE_TENANT_ID" == "" ]; then
   echo "The parameter AZURE_TENANT_ID must be set"
   echo 
   echo "Have you run \". ./init_purview.sh\""
   echo
   echo "Setup aborted"
   exit -1
fi

friendlyName=""
friendlyName=`pv account getAccount | grep friendly | sed -e "s/.*Name.:..//" -e "s/.,//"`


if [ "$friendlyName" == "" ]; then
   echo "The purview account cannot be found"
   echo
   echo "Setup aborted"
   exit -1
fi

echo
echo
echo "Using Purview account               -  $PURVIEW_NAME"
echo "with colletion master/friendly name -  $PURVIEW_NAME/$friendlyName"
echo

read -p "Is this the right Purview account Y/[N] " continue

if [ "$continue" != "Y" ]; then
	echo "Please change the init parameters to reflect the right Purview Account"
	echo
	echo "Setup aborted"
	exit -3
fi

echo
echo "Getting list of collections in Purview account $PURVIEW_NAME"
echo

> collections_list

coll_no=1

pv account getCollections |
while read line 
do
     collection_name=`echo $line | grep "friendlyName" | sed -e "s/.*friendlyName.*: \"//" -e "s/.,//"`
     collection_id=`echo $line | grep "name" | sed -e "s/.*name.*: \"//" -e "s/.,//"`

     if [ "$collection_name" != "" ]; then
        save_collection_name=$collection_name
     fi

     if [ "$collection_id" != "" ]; then
	     echo " $coll_no - $save_collection_name ($collection_id)" >> collections_list
        ((coll_no++))
     fi
done

echo "Enter desired values for the following parameter - default in []:"
echo

echo "Available collections:"
cat collections_list
echo

echo "Enter number for collection [1]: " 
read parent_collection_no

parent_collection_no=${parent_collection_no:-$parent_collection_no_def}

parent_collection=`grep "^ $parent_collection_no - " collections_list | sed -e "s/.* - //" -e "s/(.*)//"`

if [ "$parent_collection" == "" ]; then
   echo "The collection with number $parent_collection_no does not exist"
   echo
   echo "Setup aborted"
   exit -1
fi

parent_collection_id=`grep "$parent_collection" collections_list | sed -e "s/.*(//" -e "s/)//"`

if [ "$parent_collection_id" == "" ]; then
   echo "The collection with number $parent_collection_no does not exist"
   echo
   echo "Setup aborted"
   exit -1
fi

echo
echo
echo "Parameters entered"
echo "------------------"
echo "Parent collection: $parent_collection ($parent_collection_id)"
echo

read -p "Do you want to create a delete file with the above parameter Y/[N] " continue

if [ "$continue" != "Y" ]; then
	echo
	echo "Setup aborted"
        echo $NC
	exit -3
fi

echo 

if [ ! -d work ]; then
   mkdir work 

   if [ $? -ne 0 ]; then
      echo "Unable to create work directory"
      echo
      echo "Program aborted"
      exit -3
   fi
fi 


echo "Gathering assets within the collection $parent_collection"
echo

offset=0
max_size=100
file="work/del_assets_raw.tmp"

> work/del_assets_list.tmp

while true 
do
    echo "Getting set of assets with offset $offset"

    pv search query --keywords "$parent_collection_id" --offset $offset --limit 1000 > work/del_assets_raw.tmp

    # file_size=$(stat -c%s "$file") # Linux
    file_size=$(stat -f%z "$file") # MacOS
    

    if (( file_size < max_size )); then
       rm work/del_assets_raw.tmp
       break
    fi
    
    cat work/del_assets_raw.tmp >> work/del_assets_list.tmp

    offset=$((offset + 1000))

done


echo
echo
echo "Creating delete file for the collection $parent_collection named \"work/delete_${parent_collection_id}.sh"\"
echo
grep "\"id\"" work/del_assets_list.tmp | sed -e "s/.*\"id\".*: \"//" -e "s/\".*/\"/" -e "s/^/pv entity delete --guid \"/" > work/delete_${parent_collection_id}.sh 
echo
echo "File generated"
echo
