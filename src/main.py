import os
import pygame
from src.flappy_bird.entities.bird import Bird
from src.flappy_bird.entities.pipe import Pipe
from src.flappy_bird.entities.base import Base
import neat

ai_gaming = True
generation = 0

WIDTH = 500
HEIGHT = 800
BACKGROUND_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets/imgs', 'bg.png')))

pygame.font.init()
FONT_POINTS = pygame.font.SysFont('arial', 25)


def draw_screen(screen, birds, pipes, base, score):
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    text = FONT_POINTS.render(f"Pontuação: {score}", 1, (255, 255, 255))
    screen.blit(text, (WIDTH - 10 - text.get_width(), 10))

    if ai_gaming:
        text = FONT_POINTS.render(f"Geração: {generation}", 1, (255, 255, 255))
        screen.blit(text, (10, 10))

    base.draw(screen)
    pygame.display.update()


def main(genomes, config):
    global generation
    generation += 1

    if ai_gaming:
        networks = []
        genome_list = []
        birds = []

        for _, genome in genomes:
            # print(id_genome)
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            networks.append(network)
            genome.fitness = 0
            genome_list.append(genome)
            birds.append(Bird(230, 350))
            
    else:
        birds = [Bird(230, 350)]
    base = Base(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    score = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if not ai_gaming:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for bird in birds:
                            bird.jump()
                            
        index_pipe = 0
        
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > (
                pipes[0].x + pipes[0].PIPE_TOP.get_width()
                ):
                index_pipe = 1
        else:
            running = False
            break

        for i, bird in enumerate(birds):
            bird.move()
            genome_list[i].fitness += 0.1
            output = networks[i].activate((
                    bird.y, 
                    abs(bird.y - pipes[index_pipe].height), 
                    abs(bird.y - pipes[index_pipe].bottom_pos))
                )
            if output[0] > 0.5:
                bird.jump()
        base.move()

        add_pipe = False
        remove_pipes = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)
                    if ai_gaming:
                        genome_list[i].fitness -= 1
                        genome_list.pop(i)
                        networks.pop(i)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move()
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipes.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
            for genome in genome_list:
                genome.fitness += 5
        for pipe in remove_pipes:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > base.y or bird.y < 0:
                birds.pop(i)
                if ai_gaming:
                    genome_list.pop(i)
                    networks.pop(i)

        draw_screen(screen, birds, pipes, base, score)


def run(config_path: str):
    config = neat.Config(
        neat.DefaultGenome, 
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path)
    
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    
    if ai_gaming:
        population.run(main, 50)
    else: 
        main(None, None)

if __name__ == '__main__':
    # path = os.path.dirname(__file__)
    # config_path = os.path.join(path, 'config.txt')
    config_path = 'config.txt'
    run(config_path)
