import sys, pygame
import math

class gameSpace(object):
	def __init__(self):
		self.size = width, height = 800, 800
		self.color = 0,0,0
		self.screen = pygame.display.set_mode(self.size)
		self.screen.fill(self.color)
		#self.ship = ship(self)
		#self.earth = earth(self)
		#self.blaster= blaster(self)
		self.clock = pygame.time.Clock()
		
	def run(self):
		self.color= 255,0,0
		while 1:
			self.clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					#self.ship.move(event)
					if event.key == pygame.K_g:
						self.color= 0,255,0
					if event.key == pygame.K_b:
						self.color = 0,0,255
					if event.key == pygame.K_r:
						self.color = 255,0,0
					if event.key == pygame.K_p:
						self.color = 254, 143, 194
					if event.key == pygame.K_y:
						self.color = 255, 255, 0
				if event.type == pygame.MOUSEBUTTONDOWN:
					#print(pygame.mouse.get_pos())
					#print("mouse pressed")	
					pygame.draw.circle(self.screen,self.color, pygame.mouse.get_pos(), 5, 2)	
				
			#self.ship.tick()
			#self.earth.tick(self)
			#self.blaster.tick(self)
			#self.screen.fill(self.color)
			#self.screen.blit(self.ship.image, self.ship.rect)
			#self.screen.blit(self.earth.image, self.earth.rect)
			#if self.blaster.render == 1: self.screen.blit(self.blaster.image, self.blaster.rect)
			
			pygame.display.flip()

class ship(pygame.sprite.Sprite):
	def __init__(self,gs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("deathstar.png")
		self.rect = self.image.get_rect()
		self.originalimage = pygame.image.load("deathstar.png")
		self.rect.x=250
		self.rect.y=250
		gs.screen.blit(self.image,self.rect)
		
	def tick(self):
		xc, yc = self.rect.center
		x,y = pygame.mouse.get_pos()
		xdisp = x-xc
		ydisp = y-yc
		if xdisp==0: xdisp=1
		self.image= pygame.transform.rotate(self.originalimage,360-math.degrees(math.atan(float(ydisp)/float(xdisp)))) 	
		
	def move(self,event):
		if event.key == pygame.K_UP:
			self.rect = self.rect.move([0,-10])
		if event.key == pygame.K_DOWN:
			self.rect = self.rect.move([0,10])
		if event.key == pygame.K_LEFT:
			self.rect = self.rect.move([-10,0])
		if event.key == pygame.K_RIGHT:
			self.rect = self.rect.move([10,0])
class earth(pygame.sprite.Sprite):
	def __init__(self, gs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("globe.png")
		self.rect = self.image.get_rect()
		self.originalimage = pygame.image.load("globe.png")
		self.rect.x=400
		self.rect.y=400
		self.hit=0
		gs.screen.blit(self.image,self.rect)
	def tick(self,gs):
		if self.rect.colliderect(gs.blaster.rect) and gs.blaster.render==1: 
			print("hit")
			self.image=pygame.image.load("globe_red100.png")
			gs.blaster.render=0
			self.hit=self.hit+1
		if self.hit>5:
			self.image = pygame.transform.scale(self.image, (int(self.rect.width*.970),int(self.rect.height*.970)))
			self.rect = self.image.get_rect()
			self.rect.x=400
			self.rect.y=400
			if int(self.rect.width*.90)<5:
				print("You won!")
				self.hit=0
				#sys.exit()

class blaster(pygame.sprite.Sprite):
	def __init__(self,gs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("blaster2.jpg")
		self.rect = self.image.get_rect()
		self.image = pygame.transform.scale(self.image, (int(self.rect.width*.25),int(self.rect.height*.25)))
		self.originalimage= self.image
		self.rect= self.image.get_rect()
		self.render=0
		self.shipx=gs.ship.rect.x
		self.shipy=gs.ship.rect.y
		self.y=4000
		self.x=4000
	def move(self,gs):
		if self.render==0:
			self.x,self.y = pygame.mouse.get_pos()
			self.shipx= gs.ship.rect.x
			self.shipy= gs.ship.rect.y
			self.rect.x=gs.ship.rect.x
			self.rect.y=gs.ship.rect.y
			self.render=1
			
		if self.rect.x<800 and self.rect.x>0 and self.rect.y>0 and self.rect.y<800:
			self.rect.x=self.rect.x+10*math.atan(float(self.y-self.shipy)/float(self.x-self.shipx))+1
			self.rect.y=self.rect.y+10*math.atan(float(self.y-self.shipy)/float(self.x-self.shipx))+1
		else:
			self.render=0
		
	def tick(self,gs):
		if self.render==1:
			self.move(gs)
		
		

class colorIndex(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
	

if __name__ == "__main__":
	gs = gameSpace()
	#s=ship(gs)
	gs.run()
	#s = ship(gs)
	
	
		
