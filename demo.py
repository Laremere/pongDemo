import random


import pyglet
from collections import defaultdict


paddleImg = pyglet.resource.image('paddle.bmp')
ballImg = pyglet.resource.image('ball.bmp')
hitSound = pyglet.resource.media('hit.wav', streaming=False)


def clamp(v, low, high):
	if v < low:
		return low
	if v > high:
		return high
	return v

class Paddle(object):
	def __init__(self, x, keyUp, keyDown):
		self.y = 250
		self.x = x
		self.height = 100
		self.width = 20
		self.keyUp = keyUp
		self.keyDown = keyDown

	def update(self, state):
		speed = 200
		if state.keys[self.keyUp]:
			self.y += speed * state.dt
		if state.keys[self.keyDown]:
			self.y -= speed * state.dt
		self.y = clamp(self.y, 0, state.height - self.height)

	def draw(self):
		paddleImg.blit(self.x, self.y)

class Ball(object):
	def __init__(self):
		self.respawnTime = 2
		self.height = 20
		self.width = 20
		self.dx = 0
		self.dy = 0
		self.x = 0
		self.y = 0
		self.ScoreLeft = 0
		self.ScoreRight = 0
		self.ScoreLabel = label = pyglet.text.Label(text = '0 - 0', 
                          font_name='Times New Roman',
                          font_size=36,
                          anchor_x="center",
                          anchor_y="center",
                          x=400, y=550)

	def update(self, state):
		if self.respawnTime > 0:
			self.x = (state.width / 2) - (self.width / 2)
			self.y = (state.height / 2) - (self.height / 2)
			self.dx = 0
			self.dy = 0
			self.respawnTime -= state.dt
			if self.respawnTime <= 0:
				self.dx = random.choice([-1,1])
				self.dy = random.choice([-1,1])

		if len(state.checkCollision(self)):
			if self.x < state.width / 2:
				if self.dx < 0:
					hitSound.play()
					self.dx *= -1.1
					self.dy *= 1.1
			else:
				if self.dx > 0:
					hitSound.play()
					self.dx *= -1.1
					self.dy *= 1.1

		speed = 200
		self.x += self.dx * state.dt * speed
		self.y += self.dy * state.dt * speed


		if self.y < 0:
			hitSound.play()	
			self.dy = 1
		if self.y > state.height - self.height:
			hitSound.play()	
			self.dy = -1

		if self.x < -1 * self.width:
			self.ScoreRight += 1
			self.ScoreLabel.text = str(self.ScoreLeft) + " - " + str(self.ScoreRight)
			self.respawnTime = 2
		if self.x > state.width:
			self.ScoreLeft += 1
			self.ScoreLabel.text = str(self.ScoreLeft) + " - " + str(self.ScoreRight)
			self.respawnTime = 2



	def draw(self):
		ballImg.blit(self.x, self.y)
		self.ScoreLabel.draw()


class Game(object):
	def __init__(self):
		self.state = State()
		self.window = pyglet.window.Window(self.state.width, self.state.height)
		self.window.push_handlers(self)
		pyglet.clock.schedule(self.update)

	def on_key_press(self, symbol, modifiers):
		self.state.keys[symbol] = True

	def on_key_release(self, symbol, modifiers):
		self.state.keys[symbol] = False

	def update(self, dt):
		self.state.dt = dt
		for entity in self.state.entities:
			entity.update(self.state)

	def on_draw(self):
		self.window.clear()
		for entity in self.state.entities:
			entity.draw()



class State(object):
	def __init__(self):
		self.width = 800
		self.height = 600
		self.keys = defaultdict(lambda: False)
		keys = pyglet.window.key
		self.entities = [Paddle(0, keys.W, keys.S), Paddle(self.width - 20, keys.UP, keys.DOWN), Ball()]

	def checkCollision(self, item):
		return [e for e in self.entities if \
			not e is item and \
			item.x < e.x + e.width and \
			item.x + item.width > e.x and \
			item.y < e.y + e.height and \
			item.y + item.height > e.y]

game = Game()
pyglet.app.run()