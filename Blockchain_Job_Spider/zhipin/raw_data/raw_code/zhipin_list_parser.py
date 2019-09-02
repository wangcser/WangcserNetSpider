from bs4 import BeautifulSoup
import pandas as pd


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


if __name__ == "__main__":

    for i in range(1, 11):
        list_parser(p=i)

