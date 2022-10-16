# I AM. (Girls Hoo Hack 2022 Submission)
## Video Demo
https://www.youtube.com/watch?v=GzZlqD4cn9c
## Inspiration
Test anxiety and imposter syndrome are rampant among female STEM students, leading to lower performance on assessments; studies by the University of Colorado Boulder, show that grade gaps form between women and their peers (Kost, et al., 2009). Test anxiety and imposter syndrome threaten student identities and their sense of belonging. Self-affirmations are positive statements, such as “I will be successful”. Statements like this improve sense of belonging and help to alleviate test anxiety. Studies have shown that positive self-affirmations help to alleviate this stress, and lead to better test scores overall (Sherman, 2013). This project aims to provide female students with affirmations before tests, to increase feelings of belonging and reduce test anxiety.

## What it does
I AM. supports students with affirmations and provides feedback to teachers about student mood. To begin, professors input their classes and test dates into the app. The site will then send out text messages with an affirmation and survey to student users before each test, giving them a research-backed boost of confidence. The survey asks users to measure their confidence going into a test, and it tracks their confidence levels over time for different courses. Finally, after their test, users receive another survey, allowing them to self-reflect on their performance. Teachers will be able to see all this data and evaluate the effectiveness of their teaching and their testing.

## How we built it
We created "I AM." with Django and Bootstrap. We chose this framework because of familiarity and elegant database interactions without sacrificing performance. We were also able to use a template which had Google login, which integrated nicely with gathering phone numbers to send to users. 

Django also allowed us to unify the frontend and backend, further eliminating any potential development bottlenecks. Because of Django's strong database model system, we were able to start development by thinking of database models and working from there.

## Challenges we ran into
- Utilizing research to back the idea behind the project. Utilizing educational and psychological research to support the idea behind the project and help reduce the grade gap.  
- Getting the analytics page done in time - we ended up having to compromise by showing dummy data.

## Accomplishments that we're proud of
- Successfully utilizing Twilio to send text messages to users to increase engagement with professor's surveys.
- Having a modern, responsive frontend
- Successfully creating the project and presentation in a concurrent manner

## What we learned
We learned how to integrate Twilio in to our website and use it to send text messages. 
## What's next for I AM. 
There are a number of ways this project could be expanded to broaden its reach and add functionality. The first of these is adding an email option so that users without phones can still connect with their classes and receive affirmations. The next improvement to increase impact and frequency of use would be to add multiple types of assignments. This would allow teachers to add not only tests, but also homeworks, projects, labs, etc. to send more affirmations and ultimately have a better understanding of their effect on the class. On the student side, a web interface could be developed that lists all the students’ upcoming assignments and allows them to provide feedback with only a click.

## Project Members:
- Marcus Mann, UVA BSCS, 2023 (https://marcusmann.dev)
- Claire Thilenius (https://sites.google.com/view/cthilenius/research?authuser=0)
- Pierson Shamaiengar (https://www.linkedin.com/in/pierson-shamaiengar-13682a1b4/)

## Resources 
Kost, L. E., Pollock, S. J., & Finkelstein, N. D. (2009, January 8). Characterizing the gender gap in introductory physics. Physical Review Physics Education Research. Retrieved October 16, 2022, from https://journals.aps.org/prper/abstract/10.1103/PhysRevSTPER.5.010101 

Sherman, D. K. (2013). Self‐affirmation: Understanding the effects. Social and Personality Psychology Compass, 7(11), 834-845.