# Suika Clone

A basic Suika game clone made using Python, Pygame, and Pymunk.

## Roadmap

    1. Allow the user to drop fruits
     a. The fruit follows the cursor at a fixed-y position. [DONE]
     b. When the left-mouse button is pressed the fruit falls down. [DONE]
    
    2. Constrain the play area
     a. Create a "box" that restricts where fruit can be dropped and be moved to. [DONE]
     b. The rectangle borders are collideable and have infinite mass, no fruit should be able to pass through it. [DONE]
     c. Large fruit are able to roll off the edge of the container. [DONE]
    
    3. Physics
     a. Fruits not yet dropped have no physics and simply follow the x-position of the cursor. [DONE]
        - Have the cursor replicate the image of the fruit.
     b. Upon a mouse press the fruit's physics is enabled, it initally should have no external velocity other than gravity. [DONE]
     c. Fruits are able to collide with each other, the larger the fruit the larger the mass. [DONE]

    4. Fruit Merges
     a. Allow fruits to be merged into higher tiers. [DONE]
     b. New fruits spawn at the collision point of the two collided fruits.
    
    5. Scoring

    6. GUI & Art