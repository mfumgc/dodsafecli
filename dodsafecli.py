import requests, urllib3, getpass, argparse

"""
DoD Safe CLI script provides a means to download files from DoD Safe over CLI 
notifications@frauenhoffer.us                                                          
                                                                                              
ToDo:                                                                                         
- Add list_contents of DoD Safe. i.e. response.text | grep fid $uniq_uid                      
- Error handleing for bad requests. Invalid password,recip,or claim                           
"""                                                                                           


print("""\
  _____        _____     _____        __        _____ _      _____ 
 |  __ \      |  __ \   / ____|      / _|      / ____| |    |_   _|
 | |  | | ___ | |  | | | (___   __ _| |_ ___  | |    | |      | |  
 | |  | |/ _ \| |  | |  \___ \ / _` |  _/ _ \ | |    | |      | |  
 | |__| | (_) | |__| |  ____) | (_| | ||  __/ | |____| |____ _| |_ 
 |_____/ \___/|_____/  |_____/ \__,_|_| \___|  \_____|______|_____|
 v0.3                                                                  
                                                                   
    
    """)

# Parse for arguments
parser = argparse.ArgumentParser(description="Dod_CLI Helper    . You will need the requests lib. pip3 install requests --user ",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--claim_ID", help="Claim ID")
parser.add_argument("-c", "--recip_Code", help="Recipient Code")
parser.add_argument("-u", "--User", help="User", default='guest')
parser.add_argument("-p", "--claim_Pass", help="Claim Password")
parser.add_argument("-f", "--output_File", help="Ouput File", default='download.zip')
parser.add_argument("-e", "--Encrypted", help="Encryption Passphrase", action="store_true")
parser.add_argument("-v", "--Verbose", help="Print Cookie Trail", action="store_false")
args = parser.parse_args()

# Troubleshoot args
#config = vars(args)
#print(config)
#print(args.claim_ID)

# Set arguments to vars
claimID = args.claim_ID
recipCode = args.recip_Code
claimPass = args.claim_Pass
outfile = args.output_File
session = requests.Session()

# Surpress warnings
urllib3.disable_warnings()

# Setup Initial Headers
headers = {
    'Host': 'safe.apps.mil',
    'Connection': 'close',
    'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Establish session for cookies, use default headers 
response = session.get('https://safe.apps.mil/pickup.php?claimID='+claimID+'&recipCode='+recipCode, headers=headers, verify=False)
cookies = session.cookies

# Print cookies along the way 
if args.Verbose == False:
    for cookie in cookies:
        print('domain = ' + cookie.domain)
        print('name = ' + cookie.name)
        print('value = ' + cookie.value)
        print('')

headers = {
    'Host': 'safe.apps.mil',
    'Connection': 'close',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'null',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9'
}

if args.Encrypted == False:
    print("Downloading...")
    data = 'auth=&claimPasscode='+claimPass+'&fid=all&n=&isSelectedFiles=false'
    dl = session.post('https://safe.apps.mil/download.php?claimID='+claimID+'&recipCode='+recipCode, data=data, cookies=cookies, headers=headers, verify=False, stream=True, allow_redirects=True)

elif args.Encrypted == True:
    print("Downloading...")
    passphrase = getpass.getpass(prompt='Enter encryption passphrase: ', stream=None)
    data = 'auth=&claimPasscode='+claimPass+'&fid=all&n='+passphrase+'&isSelectedFiles=false'
    dl = session.post('https://safe.apps.mil/download.php?claimID='+claimID+'&recipCode='+recipCode, data=data, cookies=cookies, headers=headers, verify=False, stream=True, allow_redirects=True)
else:
    exit()

# Print response
if args.Verbose == False:
    print('HTTP Response Code: ', dl.status_code)
    print('HTTP Headers: ', dl.headers)

fd = open(outfile, 'wb')
fd.write(dl.content)
fd.close()
