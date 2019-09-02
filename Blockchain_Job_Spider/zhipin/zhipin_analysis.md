# Web Analysis

## BOSS ZHIPIN

###Init

entrance page: 
```
https://www.zhipin.com/?sid=sem_pz_bdpc_dasou_title
```
search result page:
```
https://www.zhipin.com/job_detail/?query=%E5%8C%BA%E5%9D%97%E9%93%BE&scity=101270100&industry=&position=
```
this is a get request. 
- get body is www.zhipin.com/job_detail/
- get params is query, scity, industry, position

    - scity use to chose your job cities.
    - positions use to chose your job type.
    - industry use to chose your job industry.
    - %E5%8C%BA%E5%9D%97%E9%93%BE is code for blockchain

for blockchain, the GET request for all locations is:

```html
https://www.zhipin.com/job_detail/?query=%E5%8C%BA%E5%9D%97%E9%93%BE&scity=100010000&industry=&position=
```

### List Page

1. we can use this url to get the job list:
  ```
  https://www.zhipin.com/c100010000/?query=%E5%8C%BA%E5%9D%97%E9%93%BE&page=1&ka=page-1
  ```
  - page = index
  - kapage = page-index
2. each list has 31 job items, each item has url like this:
	```
  https://www.zhipin.com/job_detail/1913e38066dd3c8e1Hd40t--FVE~.html?ka=search_list_1
	```
3. use the last url fetch the job pages.

### Job Page

this website use static page for job details. there are some useful info.:

Part 1

- Position Name
- Salary
- City
- Working Address
- Working Years
- Education

Part 2

- Job Description
- company Introduction

Part 3

- Business Information
  - Corporate Representative
  - Registered Capital
  - Founding time
  - Form of business enterprise
  - Management State