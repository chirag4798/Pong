import pandas as pd
import turtle
import random
import pickle

# Variables.
WIDTH = 800
HEIGHT = 600
BGCOLOR = 'black'
FGCOLOR = 'white'
score_A = 0
score_B = 0
clearance = 50
paddle_width = 5
paddle_length = 1
gamma = 0.8

# Paddle
def paddle_a_up():
    '''This Function moves the paddle A up.'''
    paddle_a.sety(paddle_a.ycor() + 20)

def paddle_a_down():
    '''This Function moves the paddle A down.'''
    paddle_a.sety(paddle_a.ycor() - 20)

# Game Window.
window = turtle.Screen()
window.title('PONG - by Chirag')
window.bgcolor(BGCOLOR)
window.setup(width=WIDTH, height=HEIGHT)
window.tracer(0)

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape('square')
paddle_a.color(FGCOLOR)
paddle_a.shapesize(stretch_wid=paddle_width, stretch_len=paddle_length)
paddle_a.penup()
paddle_a.goto(-1*(WIDTH/2 - clearance), 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape('square')
paddle_b.color(FGCOLOR)
paddle_b.shapesize(stretch_wid=paddle_width, stretch_len=paddle_length)
paddle_b.penup()
paddle_b.goto((WIDTH/2 - clearance), 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape('circle')
ball.color(FGCOLOR)
ball.penup()
ball.goto(0, 0)
dx = 1
dy = 1

# Scoreboard
pen1 = turtle.Turtle()
pen1.speed(0)
pen1.color(FGCOLOR)
pen1.penup()
pen1.hideturtle()
pen1.goto(0, 260)
pen1.write("Player A: 0    AI: 0", align='center', font=('Courier', 24, 'bold'))

#Instructions
pen2 = turtle.Turtle()
pen2.speed(0)
pen2.color(FGCOLOR)
pen2.penup()
pen2.hideturtle()  
pen2.goto(0, 230)
pen2.write('You are Player A: Use W / S to move the paddle up / down', align='center', font=('Courier', 10, 'bold'))

# Keyboard Binding
window.listen()
window.onkeypress(paddle_a_up, key='w')
window.onkeypress(paddle_a_down, key='s')


# Load Model
with open("model.pkl", "rb") as model:
    dt = pickle.load(model)
X_new = 0
    
# Main game loop.
while True:
    window.update()
    # Move the ball
    ball.setx(ball.xcor() + dx)
    ball.sety(ball.ycor() + dy)
    # Border Checking for Ball
    if ball.ycor() > (HEIGHT/2) - (2*paddle_width):
        ball.sety((HEIGHT/2) - (2*paddle_width))
        dy *= -1

    if ball.ycor() < -1*((HEIGHT/2) - (2*paddle_width)):
        ball.sety(-1*((HEIGHT/2) - (2*paddle_width)))
        dy *= -1

    if ball.xcor() > ((WIDTH/2) - (2*paddle_width)):
        ball.goto(0, 0)
        dx *= -1
        score_A += 1
        pen1.clear()
        pen1.write("Player A: {}    AI: {}".format(score_A, score_B), align='center', font=('Courier', 24, 'bold'))

    if ball.xcor() < -1*((WIDTH/2) - (2*paddle_width)):
        ball.goto(0, 0)
        dx *= -1
        score_B += 1
        pen1.clear()
        pen1.write("Player A: {}    AI: {}".format(score_A, score_B), align='center', font=('Courier', 24, 'bold'))

    # Border Checking for Paddle:
    if paddle_a.ycor() > (HEIGHT/2) - clearance:
        paddle_a.sety((HEIGHT/2) - clearance)

    if paddle_a.ycor() < -1*((HEIGHT/2) - clearance):
        paddle_a.sety(-1*((HEIGHT/2) - clearance))

    if paddle_b.ycor() > (HEIGHT/2) - clearance:
        paddle_b.sety((HEIGHT/2) - clearance)

    if paddle_b.ycor() < -1*((HEIGHT/2) - clearance):
        paddle_b.sety(-1*((HEIGHT/2) - clearance)) 

    #Collisons
    if (ball.xcor() > (WIDTH/2 - (clearance + (2*paddle_width)))) and (ball.xcor() < (WIDTH/2 - clearance)) and (ball.ycor() < (paddle_b.ycor() + clearance)) and (ball.ycor() > (paddle_b.ycor() - clearance)):
        ball.setx((WIDTH/2 - (clearance + (2*paddle_width))))
        dx *= -1

    if (ball.xcor() < -1*(WIDTH/2 - (clearance + (2*paddle_width)))) and (ball.xcor() > -1*(WIDTH/2 - clearance)) and (ball.ycor() < (paddle_a.ycor() + clearance)) and (ball.ycor() > (paddle_a.ycor() - clearance)):
        ball.setx(-1*(WIDTH/2 - (clearance + (2*paddle_width))))
        dx *= -1
    
    # AI 
    X_dash = [[ball.xcor(), ball.ycor(), dx, dy]]
    X_new = (1-gamma)*X_new + gamma*dt.predict(X_dash)[0] 
    if (ball.xcor() > 0) and dx > 0 and (abs(ball.ycor() - paddle_b.ycor()) > 25) :   
        paddle_b.sety(X_new)