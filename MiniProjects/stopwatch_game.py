# template for "Stopwatch: The Game"

# define global variables
import simplegui

WIDTH = 200
HEIGHT = 200
ticks = 0					# current time
good_stop = 0				# score counter
tried_stop = 0				# attempts counter
just_stopped = False		# scoring flag

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tenths = str(t % 10)	# stores tenths in string
    t = t // 10				# removes tenths from time
    secs = str(t % 60)		# stores seconds in string
    if len(secs) == 1:		# ensures secs is 2 digits
        secs = '0' + secs
    mins = str(t // 60)		# stores min in string
    return mins + ":" + secs + "." + tenths


# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global just_stopped
    timer.start()
    just_stopped = True		# turn on scoring flag

def stop():
    global good_stop, tried_stop, just_stopped
    timer.stop()
    if just_stopped == True:# if its the first stop
        if ticks % 10 == 0:	# score if tick ends in 'x.0'
            good_stop += 1
        tried_stop += 1		# count the attempt
    just_stopped = False	# turn off scoring flag

def reset():
    global ticks, good_stop, tried_stop
    timer.stop()
    ticks, good_stop, tried_stop = 0, 0, 0

# define event handler for timer with 0.1 sec interval
def tick():
    global ticks
    ticks += 1				# tick timer

# define draw handler
def draw(canvas):
    string_time = format(ticks)
    time_width = frame.get_canvas_textwidth(string_time, 20, 'monospace')
    canvas.draw_text(string_time,
                     [WIDTH/2 - time_width/2, HEIGHT/2],
                     20, 'blue', 'monospace')
    string_score = str(good_stop) + '/' + str(tried_stop)
    score_width = frame.get_canvas_textwidth(string_score, 20, 'monospace')
    canvas.draw_text(string_score,
                     [WIDTH - score_width, 20],
                     20, 'blue', 'monospace')

# create frame
frame = simplegui.create_frame('Stopwatch Game', WIDTH, HEIGHT)
timer = simplegui.create_timer(100, tick)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button('Start', start)
frame.add_button('Stop', stop)
frame.add_label('')
frame.add_button('Reset', reset)

# start frame
frame.start()

# Please remember to review the grading rubric
