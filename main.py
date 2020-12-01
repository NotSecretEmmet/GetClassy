import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pychromecast as pyccast
from pychromecast.controllers.youtube import YouTubeController


def chromecast_fire():
    ''' Attempts to connect to chromecast and play/cast the fireplace
    video. If it cannot find the provided CAST_NAME, False is returned,
    prompting the program to open it in the browser. If successfull, 
    returns True '''
    ccast, browser = pyccast.get_listed_chromecasts([CAST_NAME])
    if not ccast:
        print('Chromecast "{}" not discovered'.format(CAST_NAME))
        return False
    else:
        cast = ccast[0]
        cast.wait()
        yt = YouTubeController()
        cast.register_handler(yt)
        yt.play_video(FIRE_VIDEO_ID)
        pyccast.discovery.stop_discovery(browser)
        return True

def setup_driver():
    ''' Sets up the webdriver using the ChromeDriveManager to install
    chromedriver if missing. Also adds options to remove the 'chrome is 
    being automated blahblah' banner. '''
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "excludeSwitches", 
        ["enable-automation"]
        )
    options.add_experimental_option(
        "useAutomationExtension", 
        False
        ) 
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), 
        options=options
        )
    return driver

def play_rain():
    ''' Navigates to the infinte rain url, locates the play
    button, and after it becomes clickable, clicks it. '''
    driver.get(RAIN_URL)
    try:
        play_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="pButton"]'))
        )
        play_btn.click()
    except:
        sys.exit('Error in clicking the play rain button')
        driver.quit()
    
def play_jazz():
    ''' Open the smooth jazz loop video in a new
    chrome tab and plays it '''
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(JAZZ_URL)
    switch_to_iframe()
    play_video()

def play_fire():
    ''' Opens the fireplace video in a new tab, plays it,
    and maximizes to fullscreen.  '''
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[2])
    driver.get(FIRE_URL)
    switch_to_iframe()
    play_video()
    full_screen_video() 

def switch_to_iframe():
    ''' Locates and switches to the iframe containing the
    embedded youtube video.  '''
    try:
        frame = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
            '//iframe[starts-with(@src, "https://www.youtube.com/embed")]')))
        driver.switch_to.frame(frame)
    except:
        driver.quit()
        sys.exit('Error in locating embedded youtube player')

def play_video():
    ''' Locates the video play button and clicks it. '''
    try:
        play_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, 
                '//button[@aria-label="Play"]'))
            )
        play_btn.click()    
    except:
        driver.quit()
        sys.exit('Error clicking the play button.')

def full_screen_video():
    ''' Locates the full screen video button and clicks it.'''
    try:
        full_screen_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                '.ytp-fullscreen-button'))
            )
        full_screen_btn.click()    
    except:
        driver.quit()
        sys.exit('Error in clicking the full screen button')

if __name__ == "__main__":

    FIRE_VIDEO_ID = 'DIx3aMRDUL4'
    CAST_NAME = 'Cellar TV'
    RAIN_URL = 'https://www.rainymood.com/'
    JAZZ_URL = 'https://endlessvideo.com/watch?v=HMnrl0tmd3k'
    FIRE_URL = 'https://endlessvideo.com/watch?v=' + FIRE_VIDEO_ID
    
    if CAST_NAME:
        fire_cast = chromecast_fire()
    driver = setup_driver()
    play_rain()
    play_jazz()
    if fire_cast:
        driver.minimize_window()
    else:
        play_fire()
