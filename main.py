import time
import sys
from random import randrange
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import edgedriver_autoinstaller
import warnings
warnings.filterwarnings('ignore')


def findopj(pattern: str, delay: int = 10, inputDriver=False, listmode=False):
    global driver
    if inputDriver:
        driver = inputDriver

    try:
        if not listmode:
            m = EC.visibility_of_element_located((By.XPATH, pattern))
        else:
            m = EC.visibility_of_all_elements_located((By.XPATH, pattern))

        return WebDriverWait(driver, delay).until(
            m
        )

    except UnexpectedAlertPresentException:
        sleepTime(2)
        return False
    except TimeoutException:
        return False


def get_update_msg():
    findChatmsgList = findopj(
        f'//span[text()="{userName}"]/./../span/div[text()="/dice"]/../../../div/div/span/time/../..', listmode=True)
    if findChatmsgList:
        return findChatmsgList[-1].text
    else:
        return False


def amountCutting(st):
    if st.split()[-2] == '!':
        return int(st.split()[-3].replace(',', ''))
    else:
        return int(st.split()[-2].replace(',', ''))


def get_result():
    while True:
        sleepTime(1)
        r = get_update_msg()
        if r:
            r = r.lower()
            if 'won' in r:
                return 1, amountCutting(r)
            elif 'lost' in r:
                return 0, amountCutting(r)
            elif 'draw' in r:
                return 2, amountCutting(r)
        else:
            print("Some error rise")
            sys.exit()


def conProblemCheck():
    for _ in range(300):
        checkProblem = findopj(connectionProblem, delay=1)
        if not checkProblem:
            return
        print(f"Connection Problem rise {_}")
        sleepTime(1)

    sys.exit()


def daliyWeekly():
    if randrange(2):
        findTextBoxt = findopj(inputbox)
        if findTextBoxt:
            if randrange(2):
                findTextBoxt.send_keys(
                    f'/work {Keys.ENTER}' if randrange(2) else f'!work {Keys.ENTER}')
                findTextBoxt.send_keys(Keys.ENTER)
            if randrange(2):
                findTextBoxt.send_keys(
                    f'/daily {Keys.ENTER}' if randrange(2) else f'!daily {Keys.ENTER}')
                findTextBoxt.send_keys(Keys.ENTER)


def sleepTime(wait):
    if wait > 1:
        for _ in reversed(range(1, wait+1)):
            msg = 'wating {number:0{width}d}s'.format(width=2, number=_)
            print("\r", end='')
            print(msg, end='', flush=True)
            time.sleep(1)
        print("\r" + (' '*(len(msg)+5)), end='')
        print(' ', end='')
    else:
        time.sleep(wait)


if __name__ == "__main__":
    # pattern
    inputbox = '//div[@aria-label="Message #🎡︱nunatico"]'
    connectionProblem = "//div[text()='Connection problems? Let us know!']"
    userNameP = '//div[@data-text-variant="text-sm/normal"]/div[@data-text-variant="text-sm/normal"]'
    setAmountBoxP = '//div[text()="Throw two dice to gain coins"]'

    options = Options()
    if not '--hold' in sys.argv:
        if '--headless' in sys.argv:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')

        listbets = list(
            map(int, input('Set your list of bets [100, 200, 400, 1000]: ').split()))
        if not listbets:
            listbets = [100, 200, 400, 1000]

        setGameTry = input("How manny game you want to [50] : ")
        if not setGameTry:
            setGameTry = 50

        failTry = input("Fail try again [1]: ")
        if not failTry:
            failTry = 1
        else:
            failTry = int(failTry)

        limitMode = input("Is any limit [1000]: ")
        if not limitMode:
            limitMode = 1000
        else:
            limitMode = int(limitMode)

    options.add_argument(
        f'--user-data-dir={os.getcwd()}//edgeProfile')
    options.add_argument('log-level=3')
    options.add_argument("--disable-extensions")

    edgedriver_autoinstaller.install(os.getcwd())

    driver = webdriver.Edge(options=options)
    landing = f"https://discord.com/channels/823944237686849586/971491705239003186"
    driver.get(landing)
    sleepTime(1)
    if '--hold' in sys.argv:
        input("Hold mode is on. Type any key to release : ")

    findUserName = findopj(
        userNameP)
    if findUserName:
        userName = findUserName.text
        print("Your userName: " + userName)
    else:
        userName = input("We cann't find your username Enter your userName: ")
    os.system(f'title {userName}')

    daliyWeekly()

    total = 0
    w = 0
    l = 0
    itime = 0
    dtime = 0
    for mm in range(failTry):
        for t in range(int(setGameTry)):
            print(f"\nGame No: {t}")
            if itime <= 4 and t % 3 == 0:
                listbets = [p+20 for p in listbets]
                print(f"Increasing bets list {listbets}")
                itime += 1
            to = 0
            l = 0
            completedLost = True
            while to < len(listbets):
                if dtime <= 4 and l == 2:
                    listbets = [p-40 for p in listbets]
                    print(f"Decreasing bets list {listbets}")
                    if sum(n < 0 for n in listbets) != 0:
                        print("Nagative value found")
                        sys.exit()
                    dtime += 1
                conProblemCheck()
                findTextBoxt = findopj(
                    inputbox)
                if findTextBoxt:
                    findTextBoxt.send_keys('/dice')
                    findAmountsetBox = findopj(
                        setAmountBoxP)
                    if findAmountsetBox:
                        findAmountsetBox.click()
                        findTextBoxt = findopj(
                            inputbox)
                        if findTextBoxt:
                            sendBits = randrange(listbets[to]-5, listbets[to])
                            findTextBoxt.send_keys(
                                f'{sendBits if limitMode >= sendBits else limitMode}\n')
                            sleepTime(randrange(6, 8))
                            result = get_result()
                            if result[0] == 1:
                                print('won', end='')
                                total += result[1]
                                w += 1
                            elif result[0] == 2:
                                print('draw', end='')
                            else:
                                print('lost', end='')
                                total -= result[1]
                                l += 1
                            print(f' {result[1]}')
                            os.system(f'title {total} {userName}')

                            sleepTime(randrange(60, 65))

                            if result[0] == 1:
                                completedLost = False
                                break
                            elif result[0] == 2:
                                continue

                            to += 1
            if l <= 2:
                itime = 0
                dtime = 0
            if completedLost:
                if failTry == mm+1:
                    driver.close()
                print(f"You lost all of dice {mm+1}")
                break
