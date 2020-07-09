import socket, struct
import pandas
import ipaddress
import DNS
import csv
from tqdm import tqdm
import asyncio
import sys
import aiofiles, aiohttp
import aiodns


ip_domain_list = []

def do_work():

        
    country_code = input("Please Enter Country Code :  ")

    ip2loc_df = pandas.read_csv('ip_location_db.csv')

    ip_add_list = get_ip_range(country_code, ip2loc_df)

    asyncio.run(do_reverse_dns(ip_add_list))



    
async def do_reverse_dns(ip_add_list):

    print_function("do_reverse_lookup()")
    
    test_counter = 0

    list_len = len(ip_add_list)

    num_to_update = list_len/100
    task_list = []

    with tqdm(total = list_len) as pbar:

        
        for ip in ip_add_list:
            
            task = asyncio.create_task(get_domain(ip))
            task_list.append(task)
            
            pbar.update(1)
        await asyncio.gather(*task_list)
                
    ip_domain_df = pandas.DataFrame(ip_domain_list)
    ip_domain_df.to_csv('ip_domain.csv')

    
async def get_domain(ip):

    print(f'Started working on {ip}')
    try:
        domain_name = await DNS.revlookup(ip)
    except DNS.Base.ServerError:
        #print(f'error occured for ip ----> {ip}')                      
        domain_name = ''
    except DNS.Base.TimeoutError:
        #print(f'timeout occured for ip -----> {ip}')                   
        domain_name = ''

    if domain_name:
        test_counter += 1
        print(f'name resolved for {ip} to {domain_name}')              
        ip_domain_list.append((ip, domain_name))

        if test_counter < 10 and '.net' not in domain_name:
            print(ip, domain_name, test_counter)

    
def get_ip_range(cnt_code, ip2loc_df):

    print_function("get_ip_range")
    
    range_tuple_list = []
    ip_add_list = []
    
    #TODO add progress bar
    for index, row in ip2loc_df.iterrows() :
        country_code = row[2]

        if country_code == cnt_code:
            #src_add = socket.inet_ntoa(struct.pack('!L', int(row[0])))
            #dst_add = socket.inet_ntoa(struct.pack('!L', int(row[1])))

            src_add = int(row[0])
            dst_add = int(row[1])
            
            range_tuple_list.append((src_add, dst_add))

    for item in range_tuple_list:
        for ip_int in range(item[0], item[1]):
            ip_add_list.append(str(ipaddress.IPv4Address(ip_int)))

    #to save time in testing phase
    '''
    with open('ip_add_list.csv', 'a') as file:
        csv_wr = csv.writer(file)
        for ip in ip_add_list:
            csv_wr.writerow(ip)
    '''
    
    print(f'Number of calculate ips ----> {len(ip_add_list)}  ')
    
    return ip_add_list

def print_function(val):
    print(f'\n\nRunning ----> {val}\n')

if __name__ == '__main__':
    do_work()
    
