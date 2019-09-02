from bs4 import BeautifulSoup
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def job_parser(jid):

    print(jid)
    file = './raw_data/page/' + jid + '.html'
    with open(file, 'r', encoding='utf-8') as f:
        raw = f.read()
    soup = BeautifulSoup(raw, 'html.parser')

    # info details
    base_info_div = soup.find('div', attrs={'class': 'info-primary'})
    job_name = base_info_div.h1.text

    salary_obj = base_info_div.find('span', attrs={'class': 'salary'})
    salary = salary_obj.text.strip()

    demand_obj = base_info_div.p
    demand = demand_obj.text.strip()

    # job details
    job_div = soup.find_all('div', attrs={'class': 'job-sec'})

    job_des_div = job_div[0]
    job_des_obj = job_des_div.div
    job_des = job_des_obj.text.strip()  # job description

    com_info_div = job_div[1]
    com_info_obj = com_info_div.div
    com_info = com_info_obj.text.strip()     # company information

    if len(job_div) is 6:
        busi_info_div = job_div[4]
        job_loca_div = job_div[5]

    elif len(job_div) is 5:
        busi_info_div = job_div[3]
        job_loca_div = job_div[4]
    elif len(job_div) is 4:
        busi_info_div = job_div[2]
        job_loca_div = job_div[3]
    else:
        logger.warning('Warning exists')
    return

    # business information
    com_name = busi_info_div.div.text       # company information

    com_li = busi_info_div.find_all('li')

    ceo_li = com_li[0]
    ceo = ceo_li.text.split('：')[-1]

    fund_li = com_li[1]
    fund = fund_li.text.split('：')[-1]

    year_li = com_li[2]
    year = year_li.text.split('：')[-1]

    com_type_li = com_li[3]
    com_type = com_type_li.text.split('：')[-1]

    state_li = com_li[4]
    state = state_li.text.split('：')[-1]

    # job location
    location = job_loca_div.find('div',
                                 attrs={'class': 'location-address'}).text

    # df
    zhipin_job = {
        "name": job_name,
        "salary": salary,
        "demand": demand,
        "job_des": job_des,
        # "com_info": com_info,
        # "com_name": com_name,
        # "ceo": ceo,
        # "fund": fund,
        # "year": year,
        # "com_type": com_type,
        # "state": state,
        "location": location
    }

    logger.info('job parser success.')
    return zhipin_job


def to_csv(job_list):
    # job_attrs = [
    #     "name", "salary", "demand", "job_des", "com_info",
    #     "com_name", "ceo", "fund", "year", "com_type", "state", "location"
    # ]
    job_attrs = [
        "name", "salary", "demand", "job_des", "location"
    ]
    df = pd.DataFrame(job_list, columns=job_attrs)
    df.to_csv('./job_data.csv', index=False)


def list_parser(p):
    # load list page
    file = "./raw_data/list/" + str(p) + ".html"
    with open(file, 'r', encoding='utf-8') as f:
        raw = f.read()
    soup = BeautifulSoup(raw, 'html.parser')
    job_list_obj = soup.find_all('div', attrs={'class': 'job-primary'})

    job_list = []
    for job_obj in job_list_obj:
        # title
        title = job_obj.find('div', attrs={'class': 'job-title'}).text
        # salary
        salary = job_obj.find('span', attrs={'class': 'red'}).text
        # jid
        jid_obj = job_obj.find('a')
        jid = jid_obj.attrs['data-jid']
        ka = jid_obj.attrs['ka']

        url = 'https://www.zhipin.com/job_detail/' + jid + '.html?ka=' + ka

        # company
        company = job_obj.find('div', attrs={'class': 'info-company'}).a.text
        # info publis
        pub_time = job_obj.find('div', attrs={'class': 'info-publis'}).p.text

        # store url.
        # job = Job(index, title, salary, url, company, pub_time)
        job = {
            "jid": jid,
            "ka": ka,
            # "url": url,
            "title": title,
            "salary": salary,
            "company": company,
            "pub_time": pub_time
        }
        job_list.append(job)

    # job_attrs = ["url", "jid", "ka", "title", "salary", "company",
    #              "pub_time"]

    job_attrs = ["jid", "ka", "title", "salary", "company",
                 "pub_time"]
    df = pd.DataFrame(job_list, columns=job_attrs)

    df.to_csv('./raw_data/list/job_list.csv', index=False, mode='a',
              header=False, encoding='utf-8')

    logger.info('list parser success.')
