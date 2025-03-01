case $1 in
	
	"brute")
		echo -e -n "\nBrute Force Tester"
		echo -e -n "\nWhat username would you like to target?   "
		read username
		echo -e -n "\nHow many threads would you like to use?   "
		read threadcount
		python3 forceLogin.py -method=brute -username=$username -threads=$threadcount
		;;
	"hard")
		echo -n -e "\nBrute Force Tester - Hard Mode"
		echo -n -e "\nWhat username would you like to target?   "
		read username
		echo -n -e "\nHow many threads would you like to use?   "
		read threadcount
		python3 forceLogin.py -method=hard -username=$username -threads=$threadcount
		;;
	"dict")
		echo -n "Dictionary Attack"
		echo -n "What username would you like to target?   "
		read username
		python3 forceLogin.py -method=dict -username=$username
		;;
	"sql")
		echo -n "SQL Attack"
		python3 sqlAuto.py
		;;
	"search")
		echo -n "Search Query Injection"
		python3 searchQuery.py
		;;
	"basket-add")
		echo -n "Basket Insertion"
		python3 SelAdditionalItem/AdditionalItemInBasket.py
		;;
	"basket-view")
		echo -n "View another's basket"
		python3 SelViewOtherBasket/SelViewOtherBasket.py
		;;
esac
