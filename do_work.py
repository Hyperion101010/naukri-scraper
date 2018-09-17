import pandas as pd
import os

print ('Take time to understand the sraper first there are two modes\n1)1st is to run this scraper for entire known categories\n2)to for your input categories')
print ('\nYou specify the directory where to store the scraped data \n the directory where the scraper program is stored')
print ('for now it fetches only 3000,due to time constraint but in real it can fetch every job available for the category(just change limit in code)\n')
"""
os.chdir('/home/hyperion/Desktop/')
data = pd.read_excel('job_excel_list.xlsx')
os.chdir('/home/hyperion/Desktop')
"""
select = int(input('\n enter the mode 1 or 2:'))
if select == 1:
    print ('\nenter the  path where to store fetched file:\n')
    store_dir = str(input())
    data = pd.read_excel('job_excel_list.xlsx')
    #os.chdir(curr_path)
    from scraper_file.scraper import run_scraper
    new_data = [j for j in data[0]]
    for i in range(len(new_data)):
        print ('performing task',new_data[i],'\n')
        m_list = run_scraper(new_data[i].lower())
        print ('fetched %d jobs\n' % len(m_list))
        print('done job fetching for :%s' % (new_data[i]))
        curr_path = os.getcwd()
        os.chdir(store_dir)
        print('now storing data')
        main_list=[k for k in m_list if k!=None]
        data1 = pd.DataFrame(main_list)
        writer = pd.ExcelWriter('%s.xlsx' % (new_data[i]), engine='xlsxwriter')
        data1.to_excel(writer)
        print('done for: %s' % new_data[i])
        writer.save()
        writer.close()
        os.chdir(curr_path)
else:
    print ('\nenter the category for which you want to fetch jobs(it must be present on naukri.com):\n')
    curr_path = os.getcwd()
    cat = str(input())
    print ('\nwhere you want to strore fetched data:\n')
    store_dir = str(input())
    from scraper_file.scraper import run_scraper
    print ('performing task',cat)
    m_list = run_scraper(cat.lower())
    print ('fetched %d jobs\n' % len(m_list))
    print('done job fetching for %s' % (cat))
    os.chdir(store_dir)
    print('now storing data')
    main_list=[k for k in m_list if k!=None]
    data1 = pd.DataFrame(main_list)
    writer = pd.ExcelWriter('%s.xlsx' % (cat), engine='xlsxwriter')
    data1.to_excel(writer)
    print('done for %s' % cat)
    writer.save()
    writer.close()
