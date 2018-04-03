'''
由于服务器对JS的限制，该模块用于本地运行获取cookie，拿到cookie后copy到user_grade_spider中即可。
'''

import time
from selenium import webdriver


def get_cookie():

    # 以下三种浏览器获取的cookie 都可模拟登陆状态
    # 使用phantomjs调试，该内核不进行页面渲染，理论上更快,但是初始化比较慢，优点是不需要打开窗口 time:8s
    # driver = webdriver.PhantomJS()
    # 使用edge调试，edge是浏览器中运行最快的 time: 3s
    driver = webdriver.Edge()
    # driver = webdriver.Firefox()

    # 登录信息
    login_url = "http://login.jiayuan.com"
    user_name = "18689966108"
    pass_word = " ju18689966108"
    cookie_url = "http://www.jiayuan.com/143312003" # 随机选取的用户，目的是获取该条件下的cookie
    cook = {

    }

    # 打开登录页
    driver.get(login_url)

    # 登录成功返回cookie，登录失败返回错误信息，等待重新获取，或者抛出异常（目前异常未知）
    try:
        # 模拟用户登录
        driver.find_element_by_id("login_email").clear()
        driver.find_element_by_id("login_email").send_keys(user_name)
        driver.find_element_by_id("login_password").clear()
        driver.find_element_by_id("login_password").send_keys(pass_word)
        driver.find_element_by_id("login_btn").submit()

        time.sleep(2) # 操作缓冲，防止运行过快获取cookie失败

        driver.get(cookie_url)

        time.sleep(2)

        # 获取cookie,返回的是list，需要处理为str
        cookies = driver.get_cookies()
        # 关闭浏览器实例
        driver.quit()

        for cookie in cookies:
            coo_key = cookie['name']
            coo_val = cookie['value']
            cook[coo_key] = coo_val
    except:
        cookie_str = "COOKIE ERROR"


    return cook

if __name__ == '__main__':
    cookie_dict = get_cookie()
    print(cookie_dict)