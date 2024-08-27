# Suika Clone

A basic Suika game clone made using Python and Pygame.

## Roadmap

    1. Allow the user to drop fruits
     a. The fruit follows the cursor at a fixed-y position.
     b. When the left-mouse button is pressed the fruit falls down.
    
    2. Constrain the play area
     a. Create a "box" that restricts where fruit can be dropped and be moved to.
     b. The rectangle borders are collideable and have infinite mass, no fruit should be able to pass through it.
     c. Large fruit are able to roll off the edge of the container.
    
    3. Physics
     a. Fruits not yet dropped have no physics and simply follow the x-position of the cursor.
     b. Upon a mouse press the fruit's physics is enabled, it initally should have no external velocity other than gravity.
     c. Fruits are able to collide with each other, the larger the fruit the larger the mass.

    4. Fruit Merges
    
    5. Scoring

    6. GUI & Art