import webbrowser
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def find_web_driver():
    """
    """
    webbrowser = None

    try:
        webdriver.Chrome()
    except:
        pass
    else:
        webbrowser = webdriver.Chrome()
    
    try:
        webdriver.Edge()
    except:
        pass
    else:
        webbrowser = webdriver.Edge()

    try:
        webdriver.Firefox()
    except:
        pass
    else:
        webbrowser = webdriver.Firefox()

    try:
        webdriver.ChromiumEdge()
    except:
        pass
    else:
        webbrowser = webdriver.ChromiumEdge()

    try:
        webdriver.Safari()
    except:
        pass
    else:
        webbrowser = webdriver.Safari()

    try:
        webdriver.Ie()
    except:
        pass
    else:
        webbrowser = webdriver.Ie()

    if webbrowser is not None:
        return webbrowser
    else:
        return None