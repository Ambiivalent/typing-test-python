import time, random, pygame, pygame.midi
#------------------------------------------------------------------------------------------------------------------------------------------------------
# CONSTANT DECLARATION
WHITE, BLACK, BLUE, GRAY, RED = (255,255,255), (0,0,0), (65,197,245), (50,50,50), (255,0,0)
#------------------------------------------------------------------------------------------------------------------------------------------------------
# FUNCTION DEFINITIONS
def inputBox():
    """
    Creates an input box with text and creates blinking cursor
    Returns: Input box Surface Object and Cursor Rectangle
    """
    img = font.render(text, True, BLUE)
    text_box_rect = img.get_rect()
    text_box_rect.center = 500//2 , 450
    cursor = pygame.Rect(text_box_rect.topright, (5, text_box_rect.height))
    cursor.topleft = text_box_rect.topright

    return img, text_box_rect, cursor
#------------------------------------------------------------------------------------------------------------------------------------------------------
def showWord(words):
    """
    Creates a new word to appear on screen, randomly generated from a .txt file
    Returns: word Rectangles and Surface Objects
    """
    currentWord = words[random.randint(0,len(words))]
    img = font.render(currentWord, True, GRAY)
    text_rect = img.get_rect()
    text_rect.center = 500//2 , 100
    return img, text_rect, currentWord

def get_wpm(time, count):
    """
    Calculates the WPM and creates the drawing
    Returns: WPM Surface Object and WPM Rectangle
    """
    wpm = font.render(f"WPM:{round((count/5) / (time / 60000),2)}", True, WHITE)
    wpm_rect = wpm.get_rect()
    wpm_rect.center = 500//2, 500//2
    return wpm, wpm_rect

def show_total():
    """
    Creates drawings for total word count and accuracy. Accuracy is calculated inside the function
    Function also blits onto surface
    """
    words = font.render(f"TOTAL: {wordCount}", True, WHITE)
    words_rect = wpm.get_rect()
    words_rect.center = 500//2 , 100

    accuracy = font.render(f"ACCURACY: {round(((correctCount / charCount) * 100),2)}", True, RED)
    accuracy_rect = accuracy.get_rect()
    accuracy_rect.center = 500//2 ,450

    display.blit(words,words_rect)
    display.blit(accuracy, accuracy_rect)

def get_accuracy(text, currentWord):
    """
    Calculates if characters betwween text and the current word are matching
    Returns true if a match is found, false otherwise
    """
    try:
        if text[-1] == currentWord[len(text) - 1]: return True
        return False
    except: return False
#------------------------------------------------------------------------------------------------------------------------------------------------------
# GRAB ALL WORDS IN FILE
list_of_words = []
file = open("listOfWords.txt", "r")
for words in file:
    list_of_words.append(words[:-1])                                                                                          # GRAB ALL WORDS MINUS \n
file.close()
#------------------------------------------------------------------------------------------------------------------------------------------------------
# INITALIZE LIBRARIES
pygame.init()                                                                                           
pygame.midi.init()
#------------------------------------------------------------------------------------------------------------------------------------------------------
# CREATE DISPLAY, CLOCK, FONT AND SOUND
display = pygame.display.set_mode((500,500))
fx = pygame.midi.Output(0)
clock = pygame.time.Clock()   
font = pygame.font.SysFont(None, 48)
fx.set_instrument(113)

pygame.display.set_caption("TYPING TEST")
#------------------------------------------------------------------------------------------------------------------------------------------------------
# STARTING VARIABLES
playing = True                                                                                                                 # STATE OF GAME
solved = True                                                                                                                  # STATE OF WORD
text = ""                                                                                                                      # INPUT TEXT

time_state = False                                                                                                             # CHECK IF TIMER IS ON
start_timer = 0                                                                                                                # TIMER WHEN GAME START
wordCount = 0                                                                                                                  # WORDS COMPLETED
charCount = 0                                                                                                                  # CHARACTERS TYPED
correctCount = 0                                                                                                               # CORRECT CHARACTERS TYPED  
#------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN LOOP
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(text) > 0: text = text[:-1]                                                                              # REMOVES LAST CHARACTER
            else:
                if event.key == pygame.K_LSHIFT: break                                                                          # IGNORE SHIFT KEY
                text += event.unicode                                                                                           # ADD INPUT TO TEXT
                charCount += 1                                                        
                if get_accuracy(text, currentWord): correctCount += 1                                                           # CHECK ACCURACY
            time_state = True                                                                                                   # TIME BEGIN ONCE KEY PRESS
            if start_timer == 0: start_timer = pygame.time.get_ticks()                                                          # GET TIME OFFSET

    if time_state:                                                                                                              # CHECK IF TIME IS PASSING
        passed_time = pygame.time.get_ticks() - start_timer
        if passed_time != 0:                                                                                                    # GET WPM AND DISPLAY
            wpm, wpm_rect = get_wpm(passed_time, charCount)
            display.blit(wpm, wpm_rect)

    img, text_box_rect, cursor = inputBox()                                                                                     # GET INPUT BOX

    if solved:
        imgWord, text_rect, currentWord = showWord(list_of_words)                                                               # GET NEW WORD
        solved = False

    if text == currentWord:
        fx.note_on(64,127)
        solved = True
        wordCount += 1
        text = ""                                                                                                               # RESET INPUT
    
    if wordCount == 10: playing = False                                                                                         # BREAK CASE

    display.blit(imgWord, text_rect)
    display.blit(img, text_box_rect)
    if time.time() % 1 > 0.5:
        pygame.draw.rect(display, BLUE, cursor)                                                                                 # BLINKING CURSOR EFFECT

    pygame.display.flip()
    clock.tick(60)
    display.fill(BLACK)
#------------------------------------------------------------------------------------------------------------------------------------------------------
# END SCREEN
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: break
    display.blit(wpm, wpm_rect)                                                                                                 # SHOWCASE FINAL RESULTS
    show_total()

    pygame.display.flip()

#------------------------------------------------------------------------------------------------------------------------------------------------------

